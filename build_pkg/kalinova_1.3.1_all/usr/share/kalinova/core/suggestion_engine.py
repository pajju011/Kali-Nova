"""
Automated Next-Action & Scenario Suggestion Engine for Kali-Nova.
Combines ML forward-pass inference with heuristic rules to generate actionable security recommendations.
"""

from typing import List
from core.app_state import app_state
from core.ml.ml_advisor import MLAdvisor
from core.port_advisor import PortAdvisor


class SuggestionEngine:
    """
    Evaluates current scan state, port exposure, and security events
    to generate structured next actions and diagnostic suggestions.
    """

    @staticmethod
    def generate() -> str:
        """
        Executes ML scenario analysis, updates AppState with the prescribed action,
        and constructs formatted suggestions text.
        """
        suggestions: List[str] = []

        try:
            # 1. Query ML Guidance
            guidance = MLAdvisor.get_guidance()
            tool_name = guidance.get("tool_name", "Security Tool")
            confidence = guidance.get("confidence", 85.0)
            action_title = guidance.get("action_title", "Recommended Action")
            rationale = guidance.get("rationale", "")
            expected = guidance.get("expected_outcome", "")

            # Format primary ML recommendation
            ml_header = f"🤖 [ML Recommender - {confidence}% Confidence]"
            ml_body = f"• Next Step: {action_title} ({tool_name})\n• Rationale: {rationale}\n• Expected Outcome: {expected}"
            suggestions.append(f"{ml_header}\n{ml_body}")

        except Exception as e:
            # Fallback to rule-based suggestion if ML module encounters error
            suggestions.append(f"⚠️ [ML Engine Fallback]: Rule-based mode active ({str(e)})")

        # 2. Port-Based Strategic Findings
        if app_state.open_ports:
            port_findings = PortAdvisor.analyze_ports(app_state.open_ports)
            port_lines = []
            for item in port_findings[:3]:
                port_lines.append(f"• Port {item['port']} ({item['service']}) [{item['risk']} Risk]: {item['vulnerability']} → Use {item['recommended_tool']}")
            if port_lines:
                suggestions.append("🔍 [Port Intelligence]:\n" + "\n".join(port_lines))

        # 3. Security Event Alerts
        event_lines = []
        for event in app_state.events:
            if event == "SQL_INJECTION":
                event_lines.append("• 💉 SQL Injection detected → Run SQLmap database enumeration.")
            elif event == "BRUTE_FORCE":
                event_lines.append("• 🔑 Brute force activity detected → Strengthen lockout policy & test with Hydra.")
            elif event == "DIR_ENUM":
                event_lines.append("• 📁 Hidden directories discovered → Perform deep fuzzing with Gobuster/Wfuzz.")
            elif event == "EMAIL_ENUM":
                event_lines.append("• 📧 Email addresses leaked → Potential phishing entry vector.")
            elif event == "SECRET_LEAK":
                event_lines.append("• 🚨 API keys/secrets leaked in source assets → Revoke tokens immediately.")
            elif event == "SUBDOMAIN_ENUM":
                event_lines.append("• 🌐 Subdomains identified → Scan external perimeter with Nmap.")

        if event_lines:
            suggestions.append("⚡ [Event Alerts]:\n" + "\n".join(event_lines))

        # 4. Overall Risk Summary
        if app_state.risk_score >= 9:
            suggestions.append("🚨 [Risk Rating: HIGH] Immediate remediation and patch deployment required.")
        elif app_state.risk_score >= 4:
            suggestions.append("⚠️ [Risk Rating: MEDIUM] Further targeted exploitation and service auditing advised.")

        # Default fallback
        if not suggestions:
            suggestions.append("No active vulnerabilities detected. System appears stable. Launch Recon or Nmap to begin.")

        final_text = "\n\n".join(suggestions)
        app_state.suggestion = final_text
        return final_text