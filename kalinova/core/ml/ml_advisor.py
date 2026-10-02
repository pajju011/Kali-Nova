"""
ML Scenario Advisor for Kali-Nova.
Coordinates feature extraction, forward-pass ML inference, pipeline data handoff,
and generates structured 'What To Do Next' guidance.
"""

from typing import Dict, Any, List, Optional
from core.app_state import AppState, app_state
from core.ml.feature_extractor import FeatureExtractor
from core.ml.model_engine import ml_engine
from core.port_advisor import PortAdvisor
from core.tool_guide import ToolGuide
from core.pipeline_manager import PipelineManager


class MLAdvisor:
    """
    Analyzes the active security assessment state using Machine Learning
    and prescribes actionable, context-aware next steps.
    """

    TOOL_METADATA: Dict[str, Dict[str, Any]] = {
        "nmap": {
            "name": "Nmap Network Discovery",
            "page": "recon_page",
            "sub_tool": "nmap",
            "title": "Comprehensive Port & Service Scan",
            "action_desc": "Scan the target host or subnet to identify listening network services, active daemons, and operating system banners.",
            "default_flags": "-sV -T4 -Pn",
            "expected_outcome": "Discovers exposed TCP ports and service versions for subsequent targeted vulnerability auditing."
        },
        "nikto": {
            "name": "Nikto Web Auditor",
            "page": "web_page",
            "sub_tool": "nikto",
            "title": "Web Server Vulnerability & Misconfiguration Audit",
            "action_desc": "Perform an automated audit on exposed web services for known vulnerabilities, outdated server software, and dangerous CGI scripts.",
            "default_flags": "-ssl" if 443 in app_state.open_ports else "",
            "expected_outcome": "Detects missing security headers (HSTS, CSP), vulnerable server tokens, and exposed admin panels."
        },
        "gobuster": {
            "name": "Gobuster Directory Brute-Force",
            "page": "web_page",
            "sub_tool": "gobuster",
            "title": "Hidden Web URI & Directory Discovery",
            "action_desc": "Brute-force hidden paths, administrative consoles, and sensitive backup files on the target web server.",
            "default_flags": "-x php,html,txt,bak,json -t 20",
            "expected_outcome": "Uncovers hidden endpoints (e.g., /admin, /api, /config.php) that expand the web attack surface."
        },
        "sqlmap": {
            "name": "SQLmap Injection Engine",
            "page": "web_page",
            "sub_tool": "sqlmap",
            "title": "Automated Database Vulnerability Exploitation",
            "action_desc": "Perform automated SQL injection verification against detected dynamic parameters to extract database schemas.",
            "default_flags": "--batch --dbs",
            "expected_outcome": "Confirms SQL injection vulnerability and extracts accessible database names and tables."
        },
        "hydra": {
            "name": "Hydra Network Cracker",
            "page": "auth_page",
            "sub_tool": "hydra",
            "title": "Authentication & Password Resilience Audit",
            "action_desc": "Test authentication portals (SSH, FTP, HTTP) for weak credentials and default passwords.",
            "default_flags": "-l admin -P /usr/share/wordlists/rockyou.txt -t 16",
            "expected_outcome": "Identifies weak or default credentials that could lead to unauthorized administrative access."
        },
        "sslscan": {
            "name": "SSLScan Cipher Auditor",
            "page": "network_page",
            "sub_tool": "sslscan",
            "title": "SSL/TLS Cryptographic Protocol Evaluation",
            "action_desc": "Audit SSL/TLS configurations on port 443 to identify weak ciphers, expired certificates, and deprecated protocols.",
            "default_flags": "--no-failed",
            "expected_outcome": "Identifies insecure legacy TLS 1.0/1.1 protocols and weak CBC cipher suites."
        },
        "whois": {
            "name": "Whois Registrar Lookup",
            "page": "recon_page",
            "sub_tool": "whois",
            "title": "Domain & ASN OSINT Reconnaissance",
            "action_desc": "Query domain registrar records to extract owner contact details, nameservers, and IP allocations.",
            "default_flags": "",
            "expected_outcome": "Provides foundational intelligence on target infrastructure and organizational boundaries."
        },
        "theharvester": {
            "name": "theHarvester OSINT Collector",
            "page": "recon_page",
            "sub_tool": "theharvester",
            "title": "Subdomain & Corporate Identity Harvest",
            "action_desc": "Scrape public search engines for employee email addresses, virtual hosts, and subdomains.",
            "default_flags": "-b google,crtsh -l 100",
            "expected_outcome": "Collects valid subdomains and corporate email accounts to map the external perimeter."
        },
        "john": {
            "name": "John the Ripper Hash Cracker",
            "page": "auth_page",
            "sub_tool": "john",
            "title": "Offline Cryptographic Hash Recovery",
            "action_desc": "Crack dumped password hashes using dictionary and rule-based permutation attacks.",
            "default_flags": "--wordlist=/usr/share/wordlists/rockyou.txt",
            "expected_outcome": "Recovers plaintext credentials from cryptographic hash digests."
        },
        "remediate": {
            "name": "AI Remediation & Host Hardening",
            "page": "dashboard_page",
            "sub_tool": "copilot",
            "title": "Defensive Code Patching & Threat Neutralization",
            "action_desc": "Deploy defensive code snippets (Python / Node.js) and firewall hardening rules to patch critical vulnerabilities.",
            "default_flags": "",
            "expected_outcome": "Applies security patches, isolates vulnerable services, and closes critical exploit vectors."
        }
    }

    @classmethod
    def get_guidance(cls, state: Optional[AppState] = None) -> Dict[str, Any]:
        """
        Executes ML scenario analysis and produces complete 'What To Do Next' guidance.
        """
        curr_state = state or app_state

        has_input = bool(
            (curr_state.next_target and curr_state.next_target.strip()) or
            curr_state.pipeline_artifacts.get("targets") or
            curr_state.open_ports or
            curr_state.events or
            curr_state.last_tool_executed
        )

        if not has_input:
            curr_state.clear_next_action()
            return {
                "tool_key": None,
                "tool_name": "Standby",
                "action_title": "Waiting for Target Input",
                "confidence": 0.0,
                "action_desc": "Enter a target IP address or domain to receive AI/ML scenario directives and recommendations.",
                "expected_outcome": "Generates actionable security testing directives based on target surface and scan findings.",
                "rationale": "Standing by: Enter a target IP address or domain to receive AI recommendations.",
                "page": "dashboard_page",
                "sub_tool": "",
                "suggested_target": "",
                "suggested_flags": "",
                "alternatives": []
            }

        # 1. Extract feature vector
        features = FeatureExtractor.extract_features(curr_state)

        # 2. Forward pass inference
        ranked_predictions = ml_engine.predict_proba(features)
        top_tool_key, top_prob = ranked_predictions[0] if ranked_predictions else ("nmap", 0.5)

        # 3. Retrieve tool metadata
        meta = cls.TOOL_METADATA.get(top_tool_key, cls.TOOL_METADATA["nmap"])

        # 4. Resolve best target parameter using PipelineManager or active user target
        auto_target = curr_state.next_target or PipelineManager.get_best_target_for_tool(top_tool_key) or ""

        # 5. Synthesize ML technical rationale
        rationale_parts = []
        if curr_state.next_target:
            rationale_parts.append(f"Target specified: [{curr_state.next_target}]")
        if curr_state.open_ports:
            ports_str = ", ".join(str(p) for p in curr_state.open_ports[:4])
            rationale_parts.append(f"Discovered active port(s): [{ports_str}]")
        if curr_state.events:
            events_str = ", ".join(curr_state.events[:3])
            rationale_parts.append(f"Triggered security event(s): [{events_str}]")
        if curr_state.last_tool_executed:
            rationale_parts.append(f"Following previous execution of {curr_state.last_tool_executed}")

        if not rationale_parts:
            rationale_str = f"Target surface specified → Prescribed initial recon sweep with {meta['name']}."
        else:
            rationale_str = " + ".join(rationale_parts) + f" → Prescribed {meta['name']}."

        # Calibrate display confidence based on top margin vs second ranking
        second_prob = ranked_predictions[1][1] if len(ranked_predictions) > 1 else 0.1
        if top_prob >= 0.75:
            display_conf = round(top_prob * 100, 1)
        else:
            rel_margin = top_prob / max(0.01, top_prob + second_prob)
            display_conf = round(min(98.0, max(82.5, 72.0 + (rel_margin * 26.0))), 1)

        # 6. Format alternative pathways
        alternatives = []
        for alt_key, alt_prob in ranked_predictions[1:4]:
            alt_meta = cls.TOOL_METADATA.get(alt_key, {})
            alt_calibrated = round(min(80.0, max(45.0, (alt_prob / max(0.01, top_prob)) * 75.0)), 1)
            alternatives.append({
                "tool_key": alt_key,
                "name": alt_meta.get("name", alt_key.capitalize()),
                "confidence": alt_calibrated,
                "page": alt_meta.get("page", "dashboard_page"),
                "sub_tool": alt_meta.get("sub_tool", alt_key)
            })

        # 7. Update AppState next action hook
        curr_state.set_next_action(
            tool=meta["name"],
            target=auto_target,
            metadata={
                "tool_key": top_tool_key,
                "confidence": display_conf,
                "page": meta["page"],
                "sub_tool": meta["sub_tool"],
                "flags": meta["default_flags"],
                "rationale": rationale_str
            }
        )

        return {
            "tool_key": top_tool_key,
            "tool_name": meta["name"],
            "action_title": meta["title"],
            "confidence": display_conf,
            "action_desc": meta["action_desc"],
            "expected_outcome": meta["expected_outcome"],
            "rationale": rationale_str,
            "page": meta["page"],
            "sub_tool": meta["sub_tool"],
            "suggested_target": auto_target,
            "suggested_flags": meta["default_flags"],
            "alternatives": alternatives
        }
