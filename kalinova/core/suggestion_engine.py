from core.app_state import app_state


class SuggestionEngine:

    @staticmethod
    def generate():

        suggestions = []

        # ========================
        # Port Based Suggestions + Workflow Hook
        # ========================

        for port in app_state.open_ports:

            if port == 22:
                suggestions.append("SSH detected → Consider Hydra brute-force test.")
                app_state.set_next_action("Hydra")

            if port in [80, 443]:
                suggestions.append("Web service detected → Run Nikto or SQLmap.")
                app_state.set_next_action("Nikto")

        # ========================
        # Event Based Suggestions
        # ========================

        for event in app_state.events:

            if event == "SQL_INJECTION":
                suggestions.append("SQL Injection found → Extract database with SQLmap.")

            elif event == "BRUTE_FORCE":
                suggestions.append("Brute force activity detected → Strengthen password policy.")

            elif event == "DIR_ENUM":
                suggestions.append("Hidden directories found → Check for sensitive files.")

            elif event == "EMAIL_ENUM":
                suggestions.append("Email addresses discovered → Possible phishing vector.")

        # ========================
        # Risk Based Suggestions
        # ========================

        if app_state.risk_score >= 9:
            suggestions.append("⚠ HIGH RISK → Immediate security review required.")

        elif app_state.risk_score >= 4:
            suggestions.append("⚠ MEDIUM RISK → Further investigation recommended.")

        # ========================
        # Default Case
        # ========================

        if not suggestions:
            suggestions.append("No major issues detected. System appears stable.")

        # Store final suggestion text
        app_state.suggestion = "\n".join(suggestions)