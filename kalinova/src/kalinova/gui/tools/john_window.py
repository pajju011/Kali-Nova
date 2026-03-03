"""
JohnWindow — GUI window for John the Ripper.
"""

from PyQt6.QtWidgets import (
    QGroupBox, QFormLayout, QLineEdit, QCheckBox,
    QComboBox, QPushButton, QHBoxLayout, QFileDialog
)

from kalinova.gui.tools.base_tool_window import BaseToolWindow
from kalinova.parsers.john_parser import JohnParser
from kalinova.parsers.base_parser import BaseParser


class JohnWindow(BaseToolWindow):
    """John the Ripper password cracking window."""

    def _build_input_form(self) -> QGroupBox:
        group = QGroupBox("John the Ripper Configuration")
        layout = QFormLayout(group)
        layout.setSpacing(12)

        # Hash file
        hash_layout = QHBoxLayout()
        self._hash_file_input = QLineEdit()
        self._hash_file_input.setPlaceholderText("/path/to/hashfile.txt")
        hash_layout.addWidget(self._hash_file_input)

        browse_hash_btn = QPushButton("Browse")
        browse_hash_btn.setMaximumWidth(80)
        browse_hash_btn.clicked.connect(self._browse_hash_file)
        hash_layout.addWidget(browse_hash_btn)

        layout.addRow("Hash File:", hash_layout)

        # Wordlist
        wordlist_layout = QHBoxLayout()
        self._wordlist_input = QLineEdit()
        self._wordlist_input.setPlaceholderText(
            "/usr/share/wordlists/rockyou.txt (optional)"
        )
        wordlist_layout.addWidget(self._wordlist_input)

        browse_wl_btn = QPushButton("Browse")
        browse_wl_btn.setMaximumWidth(80)
        browse_wl_btn.clicked.connect(self._browse_wordlist)
        wordlist_layout.addWidget(browse_wl_btn)

        layout.addRow("Wordlist:", wordlist_layout)

        # Hash format
        self._format_combo = QComboBox()
        self._format_combo.addItems([
            "Auto-Detect", "raw-md5", "raw-sha1", "raw-sha256",
            "raw-sha512", "bcrypt", "ntlm", "lm", "descrypt",
            "md5crypt", "sha256crypt", "sha512crypt"
        ])
        layout.addRow("Hash Format:", self._format_combo)

        # Rules
        self._rules_input = QLineEdit()
        self._rules_input.setPlaceholderText("e.g., Jumbo, Single (optional)")
        layout.addRow("Rules:", self._rules_input)

        # Options
        self._incremental_check = QCheckBox("Incremental Mode (brute-force)")
        layout.addRow("", self._incremental_check)

        self._show_check = QCheckBox("Show Already Cracked Passwords (--show)")
        layout.addRow("", self._show_check)

        # Extra args
        self._extra_args = QLineEdit()
        self._extra_args.setPlaceholderText("Any additional John flags (optional)")
        layout.addRow("Extra Arguments:", self._extra_args)

        return group

    def _browse_hash_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Hash File", "", "All Files (*)"
        )
        if path:
            self._hash_file_input.setText(path)

    def _browse_wordlist(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Wordlist", "/usr/share/wordlists/",
            "Text Files (*.txt);;All Files (*)"
        )
        if path:
            self._wordlist_input.setText(path)

    def _collect_params(self) -> dict:
        fmt = self._format_combo.currentText()
        if fmt == "Auto-Detect":
            fmt = ""

        return {
            "hash_file": self._hash_file_input.text(),
            "wordlist": self._wordlist_input.text(),
            "format": fmt,
            "rules": self._rules_input.text(),
            "incremental": self._incremental_check.isChecked(),
            "show": self._show_check.isChecked(),
            "extra_args": self._extra_args.text(),
        }

    def _get_parser(self) -> BaseParser:
        return JohnParser()
