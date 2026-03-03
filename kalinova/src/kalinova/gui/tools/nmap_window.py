"""
NmapWindow — GUI window for Nmap scans.
"""

from PyQt6.QtWidgets import (
    QGroupBox, QFormLayout, QLineEdit, QComboBox,
    QCheckBox, QSpinBox, QLabel
)

from kalinova.gui.tools.base_tool_window import BaseToolWindow
from kalinova.parsers.nmap_parser import NmapParser
from kalinova.parsers.base_parser import BaseParser


class NmapWindow(BaseToolWindow):
    """Nmap scan configuration and execution window."""

    def _build_input_form(self) -> QGroupBox:
        group = QGroupBox("Nmap Scan Configuration")
        layout = QFormLayout(group)
        layout.setSpacing(12)

        # Target
        self._target_input = QLineEdit()
        self._target_input.setPlaceholderText("e.g., 192.168.1.1 or scanme.nmap.org")
        layout.addRow("Target (IP/Hostname):", self._target_input)

        # Scan type
        self._scan_type = QComboBox()
        self._scan_type.addItems([
            "TCP Connect (-sT)", "SYN Stealth (-sS)",
            "UDP (-sU)", "Ping Scan (-sn)",
            "ACK (-sA)", "FIN (-sF)", "XMAS (-sX)"
        ])
        layout.addRow("Scan Type:", self._scan_type)

        # Port range
        self._port_range = QLineEdit()
        self._port_range.setPlaceholderText("e.g., 1-1000 or 22,80,443 (leave empty for default)")
        layout.addRow("Port Range:", self._port_range)

        # Options
        self._service_detect = QCheckBox("Service/Version Detection (-sV)")
        layout.addRow("", self._service_detect)

        self._os_detect = QCheckBox("OS Detection (-O) — requires root")
        layout.addRow("", self._os_detect)

        self._aggressive = QCheckBox("Aggressive Scan (-A) — includes OS, version, scripts, traceroute")
        layout.addRow("", self._aggressive)

        # Timing
        self._timing = QSpinBox()
        self._timing.setRange(0, 5)
        self._timing.setValue(3)
        self._timing.setToolTip("0=Paranoid, 1=Sneaky, 2=Polite, 3=Normal, 4=Aggressive, 5=Insane")
        layout.addRow("Timing Template (0-5):", self._timing)

        # NSE Scripts
        self._scripts = QLineEdit()
        self._scripts.setPlaceholderText("e.g., vuln, safe, default (optional)")
        layout.addRow("NSE Scripts:", self._scripts)

        # Extra args
        self._extra_args = QLineEdit()
        self._extra_args.setPlaceholderText("Any additional Nmap flags (optional)")
        layout.addRow("Extra Arguments:", self._extra_args)

        return group

    def _collect_params(self) -> dict:
        scan_type_map = {
            0: "TCP", 1: "SYN", 2: "UDP", 3: "PING",
            4: "ACK", 5: "FIN", 6: "XMAS",
        }
        return {
            "target": self._target_input.text(),
            "scan_type": scan_type_map.get(self._scan_type.currentIndex(), "TCP"),
            "port_range": self._port_range.text(),
            "service_detection": self._service_detect.isChecked(),
            "os_detection": self._os_detect.isChecked(),
            "aggressive": self._aggressive.isChecked(),
            "timing": self._timing.value(),
            "scripts": self._scripts.text(),
            "extra_args": self._extra_args.text(),
        }

    def _get_parser(self) -> BaseParser:
        return NmapParser()
