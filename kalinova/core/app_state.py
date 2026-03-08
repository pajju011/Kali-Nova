class AppState:
    """
    Global state manager for Kalinova OS
    """

    def __init__(self):
        self.mode = "Beginner"   
        self.global_risk = "LOW"    
        self.current_session = "Session-1"
        self.logs = []
        self.suggestion = "No suggestions yet."
        self.open_ports = []

        # 🔥 Intelligence Tracking
        self.events = []
        self.risk_score = 0

        # 🤖 Workflow Automation
        self.next_tool = None
        self.next_target = None

    # ========================
    # Mode Management
    # ========================

    def set_mode(self, mode):
        self.mode = mode

    # ========================
    # Risk Management
    # ========================

    def set_risk(self, risk_level):
        self.global_risk = risk_level

    def set_risk_score(self, score):
        self.risk_score = score

    # ========================
    # Logging
    # ========================

    def add_log(self, message):
        self.logs.append(message)

    # ========================
    # Port Tracking
    # ========================

    def add_open_port(self, port):
        if port not in self.open_ports:
            self.open_ports.append(port)

    # ========================
    # Event Tracking
    # ========================

    def add_event(self, event):
        if event not in self.events:
            self.events.append(event)

    # ========================
    # 🤖 Workflow Automation
    # ========================

    def set_next_action(self, tool, target=None):
        self.next_tool = tool
        self.next_target = target

    def clear_next_action(self):
        self.next_tool = None
        self.next_target = None

    # ========================
    # Reset Scan
    # ========================

    def reset_scan(self):
        self.open_ports.clear()
        self.events.clear()
        self.risk_score = 0
        self.global_risk = "LOW"
        self.suggestion = "No suggestions yet."
        self.clear_next_action()


# Global instance
app_state = AppState()