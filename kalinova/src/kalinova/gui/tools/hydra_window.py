"""
HydraWindow — GUI window for Hydra brute-force attacks.
"""

from PyQt6.QtWidgets import (
    QGroupBox, QFormLayout, QLineEdit, QCheckBox,
    QComboBox, QSpinBox, QPushButton, QHBoxLayout,
    QFileDialog
)

from kalinova.gui.tools.base_tool_window import BaseToolWindow
from kalinova.parsers.hydra_parser import HydraParser
from kalinova.parsers.base_parser import BaseParser


class HydraWindow(BaseToolWindow):
    """Hydra brute-force attack configuration window."""

    def _build_input_form(self) -> QGroupBox:
        group = QGroupBox("Hydra Brute-Force Configuration")
        layout = QFormLayout(group)
        layout.setSpacing(12)

        # Target
        self._target_input = QLineEdit()
        self._target_input.setPlaceholderText("e.g., 192.168.1.1")
        layout.addRow("Target (IP/Host):", self._target_input)

        # Service
        self._service_combo = QComboBox()
        self._service_combo.addItems([
            "ssh", "ftp", "http-get", "http-post-form",
            "rdp", "smb", "mysql", "postgresql",
            "vnc", "telnet", "smtp", "pop3", "imap",
        ])
        self._service_combo.setEditable(True)
        layout.addRow("Service/Protocol:", self._service_combo)

        # Port
        self._port_input = QSpinBox()
        self._port_input.setRange(1, 65535)
        self._port_input.setValue(22)
        self._port_input.setToolTip("Leave at default — Hydra auto-detects port for most services")
        layout.addRow("Port (optional):", self._port_input)

        # Username
        self._username_input = QLineEdit()
        self._username_input.setPlaceholderText("e.g., admin, root")
        layout.addRow("Single Username:", self._username_input)

        # Username file
        user_file_layout = QHBoxLayout()
        self._username_file_input = QLineEdit()
        self._username_file_input.setPlaceholderText(
            "/path/to/usernames.txt (alternative to single username)"
        )
        user_file_layout.addWidget(self._username_file_input)

        browse_user_btn = QPushButton("Browse")
        browse_user_btn.setMaximumWidth(80)
        browse_user_btn.clicked.connect(self._browse_username_file)
        user_file_layout.addWidget(browse_user_btn)

        layout.addRow("Username File:", user_file_layout)

        # Password file
        pass_file_layout = QHBoxLayout()
        self._password_file_input = QLineEdit()
        self._password_file_input.setPlaceholderText(
            "/usr/share/wordlists/rockyou.txt"
        )
        pass_file_layout.addWidget(self._password_file_input)

        browse_pass_btn = QPushButton("Browse")
        browse_pass_btn.setMaximumWidth(80)
        browse_pass_btn.clicked.connect(self._browse_password_file)
        pass_file_layout.addWidget(browse_pass_btn)

        layout.addRow("Password File:", pass_file_layout)

        # Threads
        self._threads_input = QSpinBox()
        self._threads_input.setRange(1, 64)
        self._threads_input.setValue(16)
        layout.addRow("Threads:", self._threads_input)

        # Verbose
        self._verbose_check = QCheckBox("Verbose Mode (-v)")
        layout.addRow("", self._verbose_check)

        # Extra args
        self._extra_args = QLineEdit()
        self._extra_args.setPlaceholderText("Any additional Hydra flags (optional)")
        layout.addRow("Extra Arguments:", self._extra_args)

        return group

    def _browse_username_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Username File", "", "Text Files (*.txt);;All Files (*)"
        )
        if path:
            self._username_file_input.setText(path)

    def _browse_password_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Password File", "/usr/share/wordlists/",
            "Text Files (*.txt);;All Files (*)"
        )
        if path:
            self._password_file_input.setText(path)

    def _collect_params(self) -> dict:
        return {
            "target": self._target_input.text(),
            "service": self._service_combo.currentText(),
            "port": self._port_input.value(),
            "username": self._username_input.text(),
            "username_file": self._username_file_input.text(),
            "password_file": self._password_file_input.text(),
            "threads": self._threads_input.value(),
            "verbose": self._verbose_check.isChecked(),
            "extra_args": self._extra_args.text(),
        }

    def _get_parser(self) -> BaseParser:
        return HydraParser()
