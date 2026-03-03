"""
NiktoWindow — GUI window for Nikto web vulnerability scans.
"""

from PyQt6.QtWidgets import (
    QGroupBox, QFormLayout, QLineEdit, QCheckBox, QSpinBox
)

from kalinova.gui.tools.base_tool_window import BaseToolWindow
from kalinova.parsers.nikto_parser import NiktoParser
from kalinova.parsers.base_parser import BaseParser


class NiktoWindow(BaseToolWindow):
    """Nikto web vulnerability scan window."""

    def _build_input_form(self) -> QGroupBox:
        group = QGroupBox("Nikto Scan Configuration")
        layout = QFormLayout(group)
        layout.setSpacing(12)

        # Target
        self._target_input = QLineEdit()
        self._target_input.setPlaceholderText("e.g., http://192.168.1.1 or example.com")
        layout.addRow("Target (URL/Host):", self._target_input)

        # Port
        self._port_input = QSpinBox()
        self._port_input.setRange(1, 65535)
        self._port_input.setValue(80)
        layout.addRow("Port:", self._port_input)

        # SSL
        self._ssl_check = QCheckBox("Use SSL/HTTPS (-ssl)")
        layout.addRow("", self._ssl_check)

        # Tuning
        self._tuning_input = QLineEdit()
        self._tuning_input.setPlaceholderText(
            "e.g., 1234567890abc (optional, see nikto docs)"
        )
        layout.addRow("Tuning:", self._tuning_input)

        # Timeout
        self._timeout_input = QSpinBox()
        self._timeout_input.setRange(1, 600)
        self._timeout_input.setValue(10)
        self._timeout_input.setSuffix(" seconds")
        layout.addRow("Timeout:", self._timeout_input)

        # Extra args
        self._extra_args = QLineEdit()
        self._extra_args.setPlaceholderText("Any additional Nikto flags (optional)")
        layout.addRow("Extra Arguments:", self._extra_args)

        return group

    def _collect_params(self) -> dict:
        return {
            "target": self._target_input.text(),
            "port": self._port_input.value(),
            "ssl": self._ssl_check.isChecked(),
            "tuning": self._tuning_input.text(),
            "timeout": self._timeout_input.value(),
            "extra_args": self._extra_args.text(),
        }

    def _get_parser(self) -> BaseParser:
        return NiktoParser()
