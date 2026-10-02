from typing import Dict, List, Any, Optional


class AppState:
    """
    Global state manager for Kalinova OS.
    Tracks active security session metrics, discovered open ports, security events,
    tool execution pipeline artifacts, and ML-driven next actions.
    """

    def __init__(self):
        self.mode = "Beginner"   
        self.global_risk = "LOW"    
        self.current_session = "Session-1"
        self.logs: List[str] = []
        self.suggestion = "No suggestions yet."
        self.open_ports: List[int] = []

        # 🔥 Intelligence Tracking
        self.events: List[str] = []
        self.risk_score: int = 0

        # 🤖 Workflow Automation & Next Step
        self.next_tool: Optional[str] = None
        self.next_target: Optional[str] = None
        self.next_action_metadata: Dict[str, Any] = {}

        # 🔄 Inter-Tool Pipeline Artifacts
        self.pipeline_artifacts: Dict[str, Any] = {
            "targets": [],              # List of target IPs / domains
            "subdomains": [],           # Discovered subdomains
            "web_urls": [],             # Discovered HTTP/HTTPS URLs with ports
            "fuzzed_endpoints": [],     # Discovered endpoints (e.g. /admin, /api.php?id=1)
            "emails": [],               # Discovered emails
            "hashes": [],               # Discovered password hashes
            "active_services": {}       # port -> service banner mapping
        }

        # 📜 Execution Sequence History
        self.execution_history: List[Dict[str, Any]] = []
        self.last_tool_executed: Optional[str] = None

    # ========================
    # Mode Management
    # ========================

    def set_mode(self, mode: str):
        self.mode = mode

    # ========================
    # Risk Management
    # ========================

    def set_risk(self, risk_level: str):
        self.global_risk = risk_level

    def set_risk_score(self, score: int):
        self.risk_score = score

    # ========================
    # Logging
    # ========================

    def add_log(self, message: str):
        self.logs.append(message)

    # ========================
    # Port Tracking
    # ========================

    def add_open_port(self, port: int, service: Optional[str] = None):
        if port not in self.open_ports:
            self.open_ports.append(port)
        if service:
            self.pipeline_artifacts["active_services"][port] = service

    # ========================
    # Event Tracking
    # ========================

    def add_event(self, event: str):
        if event not in self.events:
            self.events.append(event)

    # ========================
    # 🤖 Workflow Automation & ML Next Step
    # ========================

    def set_next_action(self, tool: str, target: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None):
        self.next_tool = tool
        self.next_target = target
        self.next_action_metadata = metadata or {}

    def clear_next_action(self):
        self.next_tool = None
        self.next_target = None
        self.next_action_metadata = {}

    # ========================
    # 🔄 Pipeline Artifact Management
    # ========================

    def add_pipeline_artifact(self, category: str, value: Any):
        """Add discovered entity (target, URL, subdomain, endpoint, hash) to pipeline state."""
        if category in self.pipeline_artifacts:
            if isinstance(self.pipeline_artifacts[category], list):
                if value not in self.pipeline_artifacts[category]:
                    self.pipeline_artifacts[category].append(value)
            elif isinstance(self.pipeline_artifacts[category], dict) and isinstance(value, dict):
                self.pipeline_artifacts[category].update(value)

    def record_tool_execution(self, tool_name: str, target: str, command: str):
        """Record a completed tool run into execution sequence history."""
        self.last_tool_executed = tool_name
        self.execution_history.append({
            "tool": tool_name,
            "target": target,
            "command": command
        })
        # Record primary target
        if target:
            self.add_pipeline_artifact("targets", target)

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
        self.pipeline_artifacts = {
            "targets": [],
            "subdomains": [],
            "web_urls": [],
            "fuzzed_endpoints": [],
            "emails": [],
            "hashes": [],
            "active_services": {}
        }
        self.execution_history.clear()
        self.last_tool_executed = None


# Global instance
app_state = AppState()