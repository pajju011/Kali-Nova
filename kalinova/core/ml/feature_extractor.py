"""
Feature Extractor for ML Scenario State Representation in Kali-Nova.
Transforms AppState (ports, events, scan history, risk rating) into normalized feature vectors.
"""

from typing import List, Dict, Any, Optional
from core.app_state import AppState, app_state


class FeatureExtractor:
    """
    Encodes security assessment state into a standardized numerical feature vector.
    """

    FEATURE_PORTS = [21, 22, 23, 25, 53, 80, 110, 139, 443, 445, 1433, 1521, 3306, 3389, 5432, 6379, 8000, 8080, 8443, 27017]
    FEATURE_EVENTS = [
        "SQL_INJECTION",
        "BRUTE_FORCE",
        "DIR_ENUM",
        "EMAIL_ENUM",
        "SECRET_LEAK",
        "SUBDOMAIN_ENUM",
        "PORT_SCAN_COMPLETE",
        "SSL_WEAKNESS"
    ]
    FEATURE_TOOLS = [
        "none",
        "whois",
        "theharvester",
        "nmap",
        "nikto",
        "gobuster",
        "sqlmap",
        "hydra",
        "sslscan",
        "john"
    ]

    CLASSES = [
        "nmap",
        "nikto",
        "gobuster",
        "sqlmap",
        "hydra",
        "sslscan",
        "whois",
        "theharvester",
        "john",
        "remediate"
    ]

    @classmethod
    def get_feature_names(cls) -> List[str]:
        """Returns ordered list of all feature column names."""
        names = []
        for p in cls.FEATURE_PORTS:
            names.append(f"port_{p}")
        for e in cls.FEATURE_EVENTS:
            names.append(f"event_{e}")
        for t in cls.FEATURE_TOOLS:
            names.append(f"last_tool_{t}")
        names.extend([
            "risk_score_norm",
            "global_risk_level",
            "open_ports_count_norm",
            "has_web_urls",
            "has_fuzzed_endpoints",
            "has_hashes"
        ])
        return names

    @classmethod
    def extract_features(cls, state: Optional[AppState] = None) -> List[float]:
        """
        Extracts a normalized numerical vector of floats from the given AppState.
        """
        current = state if state is not None else app_state
        vector: List[float] = []

        # 1. Port Multi-Hot Vector (20 dimensions)
        open_set = set(current.open_ports)
        for p in cls.FEATURE_PORTS:
            vector.append(1.0 if p in open_set else 0.0)

        # 2. Event Multi-Hot Vector (8 dimensions)
        events_set = set(current.events)
        for ev in cls.FEATURE_EVENTS:
            vector.append(1.0 if ev in events_set else 0.0)

        # 3. Last Tool One-Hot Vector (10 dimensions)
        last_t = (current.last_tool_executed or "none").lower()
        for t in cls.FEATURE_TOOLS:
            vector.append(1.0 if last_t == t else 0.0)

        # 4. Scenario Risk & Artifact Context Features (6 dimensions)
        # Normalized risk score (0 to 20 scaled to 0.0 - 1.0)
        risk_norm = min(1.0, max(0.0, current.risk_score / 20.0))
        vector.append(risk_norm)

        # Global risk level (0=LOW, 1=MEDIUM, 2=HIGH)
        risk_levels = {"LOW": 0.0, "MEDIUM": 0.5, "HIGH": 1.0}
        vector.append(risk_levels.get(current.global_risk, 0.0))

        # Open ports count normalized
        ports_cnt_norm = min(1.0, len(current.open_ports) / 10.0)
        vector.append(ports_cnt_norm)

        # Pipeline artifact presence
        artifacts = current.pipeline_artifacts
        vector.append(1.0 if artifacts.get("web_urls") else 0.0)
        vector.append(1.0 if artifacts.get("fuzzed_endpoints") else 0.0)
        vector.append(1.0 if artifacts.get("hashes") else 0.0)

        return vector
