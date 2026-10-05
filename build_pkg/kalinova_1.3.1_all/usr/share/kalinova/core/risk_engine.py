from core.app_state import app_state


class RiskEngine:

    @staticmethod
    def calculate():

        score = 0

        # Port Based Risk
        for port in app_state.open_ports:
            score += 1

            if port == 22:  # SSH
                score += 2
            if port in [80, 443]:
                score += 1

        # Event Based Risk
        for event in app_state.events:
            if event == "SQL_INJECTION":
                score += 5
            elif event == "BRUTE_FORCE":
                score += 4
            elif event == "DIR_ENUM":
                score += 3
            elif event == "EMAIL_ENUM":
                score += 2
            elif event == "SECRET_LEAK":
                score += 5
            elif event == "SUBDOMAIN_ENUM":
                score += 2

        app_state.risk_score = score

        # Classification
        if score <= 3:
            app_state.global_risk = "LOW"
        elif score <= 8:
            app_state.global_risk = "MEDIUM"
        else:
            app_state.global_risk = "HIGH"