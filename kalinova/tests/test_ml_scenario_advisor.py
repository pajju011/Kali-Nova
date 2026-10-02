"""
Unit & Integration Test Suite for ML Scenario Analysis, Port Advisor, Tool Guide,
Pipeline Manager, and 'What To Do Next' Recommendation System in Kali-Nova.
"""

import pytest
from core.app_state import app_state, AppState
from core.port_advisor import PortAdvisor
from core.tool_guide import ToolGuide
from core.pipeline_manager import PipelineManager
from core.ml.feature_extractor import FeatureExtractor
from core.ml.model_engine import ml_engine, MLModelEngine
from core.ml.ml_advisor import MLAdvisor
from core.suggestion_engine import SuggestionEngine


@pytest.fixture(autouse=True)
def reset_global_state():
    """Reset global app_state before each test."""
    app_state.reset_scan()
    yield
    app_state.reset_scan()


# ==========================================
# 1. PortAdvisor Tests
# ==========================================

def test_port_advisor_profiles():
    prof = PortAdvisor.get_profile("FAST_TRIAGE")
    assert "Top 20" in prof["name"]
    assert 80 in prof["ports"]
    assert 443 in prof["ports"]

    ports_str = PortAdvisor.get_ports_string("FAST_TRIAGE")
    assert "80" in ports_str
    assert "443" in ports_str

    full_prof = PortAdvisor.get_profile("FULL_AUDIT")
    assert PortAdvisor.get_ports_string("FULL_AUDIT") == "1-65535"


def test_port_advisor_analysis():
    findings = PortAdvisor.analyze_ports([22, 80, 3306])
    assert len(findings) == 3
    services = [f["service"] for f in findings]
    assert "SSH" in services
    assert "HTTP" in services
    assert "MySQL" in services


# ==========================================
# 2. ToolGuide Input Validation Tests
# ==========================================

def test_tool_guide_validation_nmap():
    valid_ip, badge, msg = ToolGuide.validate_input("nmap", "192.168.1.1")
    assert valid_ip is True
    assert badge == "VALID_HOST"

    valid_cidr, badge, msg = ToolGuide.validate_input("nmap", "10.0.0.0/24")
    assert valid_cidr is True

    valid_domain, badge, msg = ToolGuide.validate_input("nmap", "scanme.nmap.org")
    assert valid_domain is True

    invalid_input, badge, msg = ToolGuide.validate_input("nmap", "not a valid host @@@")
    assert invalid_input is False
    assert badge == "INVALID_FORMAT"


def test_tool_guide_validation_sqlmap():
    # URL with parameter
    valid_param, badge, msg = ToolGuide.validate_input("sqlmap", "http://target.com/item.php?id=1")
    assert valid_param is True
    assert badge == "VALID_PARAM_URL"

    # URL without parameter (shows warning)
    no_param, badge, msg = ToolGuide.validate_input("sqlmap", "http://target.com/index.html")
    assert no_param is True
    assert badge == "WARNING_NO_PARAM"

    # Invalid string
    invalid, badge, msg = ToolGuide.validate_input("sqlmap", "invalid_url_string")
    assert invalid is False


def test_tool_guide_validation_empty():
    valid, badge, msg = ToolGuide.validate_input("nmap", "   ")
    assert valid is False
    assert badge == "EMPTY"


# ==========================================
# 3. PipelineManager Artifact Extraction & Handoff Tests
# ==========================================

def test_pipeline_manager_extracts_urls_and_handoff():
    raw_nmap = """
    Starting Nmap 7.92
    Nmap scan report for 192.168.1.50
    PORT     STATE SERVICE
    80/tcp   open  http
    8080/tcp open  http-proxy
    """
    app_state.add_open_port(80)
    app_state.add_open_port(8080)
    PipelineManager.ingest_output("nmap", raw_nmap, target="192.168.1.50")

    assert "192.168.1.50" in app_state.pipeline_artifacts["targets"]
    assert "http://192.168.1.50" in app_state.pipeline_artifacts["web_urls"]
    assert "http://192.168.1.50:8080" in app_state.pipeline_artifacts["web_urls"]

    # Test handoff to Nikto
    nikto_target = PipelineManager.get_best_target_for_tool("nikto")
    assert nikto_target is not None
    assert "http://192.168.1.50" in nikto_target


def test_pipeline_manager_extracts_endpoints_and_sqlmap_handoff():
    raw_gobuster = """
    ===============================================================
    Gobuster v3.1.0
    ===============================================================
    /admin (Status: 200)
    /login.php (Status: 200)
    /gallery.php?id=2 (Status: 200)
    """
    PipelineManager.ingest_output("gobuster", raw_gobuster, target="http://192.168.1.10")

    assert "/admin" in app_state.pipeline_artifacts["fuzzed_endpoints"]

    # Test handoff to Sqlmap
    sqlmap_target = PipelineManager.get_best_target_for_tool("sqlmap")
    assert sqlmap_target is not None


# ==========================================
# 4. FeatureExtractor & ML Model Engine Tests
# ==========================================

def test_feature_extractor_dimensions():
    feature_names = FeatureExtractor.get_feature_names()
    assert len(feature_names) == 44

    features = FeatureExtractor.extract_features(app_state)
    assert len(features) == 44
    assert all(isinstance(v, float) for v in features)


def test_feature_extractor_values():
    app_state.add_open_port(80)
    app_state.add_open_port(443)
    app_state.add_event("SQL_INJECTION")
    app_state.set_risk_score(10)
    app_state.set_risk("HIGH")
    app_state.last_tool_executed = "gobuster"

    features = FeatureExtractor.extract_features(app_state)
    names = FeatureExtractor.get_feature_names()

    port_80_idx = names.index("port_80")
    assert features[port_80_idx] == 1.0

    sqli_idx = names.index("event_SQL_INJECTION")
    assert features[sqli_idx] == 1.0

    tool_gobuster_idx = names.index("last_tool_gobuster")
    assert features[tool_gobuster_idx] == 1.0


def test_ml_model_engine_inference():
    assert ml_engine.is_loaded is True
    features = FeatureExtractor.extract_features(app_state)
    ranked = ml_engine.predict_proba(features)

    assert len(ranked) > 0
    top_class, top_prob = ranked[0]
    assert isinstance(top_class, str)
    assert 0.0 <= top_prob <= 1.0

    # Total probabilities should sum to approximately 1.0
    total_p = sum(p for _, p in ranked)
    assert abs(total_p - 1.0) < 0.01


# ==========================================
# 5. MLAdvisor & SuggestionEngine Integration Tests
# ==========================================

def test_ml_advisor_guidance_generation():
    app_state.add_open_port(80)
    app_state.add_event("SQL_INJECTION")
    app_state.last_tool_executed = "nikto"
    app_state.pipeline_artifacts["web_urls"] = ["http://192.168.1.10/login.php?id=1"]

    guidance = MLAdvisor.get_guidance()

    assert "tool_name" in guidance
    assert "action_title" in guidance
    assert "confidence" in guidance
    assert guidance["confidence"] > 0
    assert "rationale" in guidance
    assert "expected_outcome" in guidance
    assert len(guidance["alternatives"]) > 0

    # Check AppState next action hook is updated
    assert app_state.next_tool is not None


def test_suggestion_engine_integration():
    app_state.add_open_port(22)
    app_state.add_event("BRUTE_FORCE")
    app_state.set_risk_score(7)

    text = SuggestionEngine.generate()
    assert "[ML Recommender" in text
    assert "Port Intelligence" in text
    assert "Event Alerts" in text
    assert app_state.suggestion == text


def test_ml_advisor_standby_on_empty_input():
    app_state.reset_scan()
    guidance = MLAdvisor.get_guidance()
    assert guidance["tool_name"] == "Standby"
    assert guidance["action_title"] == "Waiting for Target Input"
    assert app_state.next_tool is None
