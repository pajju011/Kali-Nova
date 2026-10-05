import re
from core.app_state import app_state

class PortParser:

    @staticmethod
    def extract_ports(line):
        match = re.search(r"(\d+)/tcp\s+open", line)
        if match:
            port = int(match.group(1))
            if port not in app_state.open_ports:
                app_state.open_ports.append(port)