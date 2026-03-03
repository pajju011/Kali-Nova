"""
DisclaimerDialog — First-launch legal consent dialog.

Displays ethical usage terms and requires acceptance
before allowing access to the application.
"""

import os
import json
import logging
from typing import Optional

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTextBrowser,
    QPushButton, QHBoxLayout, QCheckBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

logger = logging.getLogger(__name__)


DISCLAIMER_TEXT = """
<h2>⚠️ Legal Disclaimer & Ethical Usage Agreement</h2>

<p>By using <strong>Kalinova</strong>, you agree to the following terms:</p>

<h3>1. Authorized Use Only</h3>
<p>You must <strong>only</strong> use Kalinova's tools against systems and networks
for which you have <strong>explicit written authorization</strong>. Unauthorized
access to computer systems is illegal and punishable by law.</p>

<h3>2. Ethical Hacking</h3>
<p>Kalinova is designed for <strong>educational purposes</strong> and <strong>authorized
security assessments</strong>. Do not use this tool for:</p>
<ul>
    <li>Attacking systems without permission</li>
    <li>Stealing data or credentials</li>
    <li>Disrupting services (DoS/DDoS)</li>
    <li>Any illegal activity</li>
</ul>

<h3>3. Applicable Laws</h3>
<p>You are responsible for compliance with all applicable local, state, national,
and international laws. Key regulations include:</p>
<ul>
    <li>Computer Fraud and Abuse Act (CFAA) — United States</li>
    <li>Computer Misuse Act — United Kingdom</li>
    <li>Information Technology Act — India</li>
    <li>GDPR — European Union</li>
</ul>

<h3>4. No Liability</h3>
<p>The Kalinova team is <strong>not responsible</strong> for any misuse of this tool.
Users assume all risk and liability for their actions.</p>

<h3>5. Educational Purpose</h3>
<p>Kalinova is a learning tool. Use it to study cybersecurity concepts in
controlled lab environments or with proper authorization.</p>

<hr>
<p style="color: #ff6b6b;"><strong>Remember: With great power comes great responsibility.</strong></p>
"""


class DisclaimerDialog(QDialog):
    """
    First-launch legal disclaimer dialog.

    Shows once and saves acceptance state. If declined,
    the application exits.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kalinova — Legal Disclaimer")
        self.setMinimumSize(600, 520)
        self.setModal(True)
        self._accepted = False
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("🔐 Kalinova Security Suite")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #00d4ff;")
        layout.addWidget(title)

        # Disclaimer content
        browser = QTextBrowser()
        browser.setHtml(DISCLAIMER_TEXT)
        browser.setOpenExternalLinks(False)
        browser.setStyleSheet("""
            QTextBrowser {
                background-color: #1a1a2e;
                border: 1px solid #2a2a4e;
                border-radius: 10px;
                padding: 16px;
                color: #d0d0d0;
                font-size: 14px;
            }
        """)
        layout.addWidget(browser)

        # Checkbox
        self._agree_check = QCheckBox(
            "I understand and agree to use Kalinova ethically and legally."
        )
        self._agree_check.setStyleSheet("font-size: 14px; font-weight: bold;")
        self._agree_check.toggled.connect(self._on_checkbox_toggled)
        layout.addWidget(self._agree_check)

        # Buttons
        btn_layout = QHBoxLayout()

        self._decline_btn = QPushButton("Decline & Exit")
        self._decline_btn.setObjectName("danger")
        self._decline_btn.setMinimumWidth(160)
        self._decline_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self._decline_btn)

        btn_layout.addStretch()

        self._accept_btn = QPushButton("Accept & Continue")
        self._accept_btn.setObjectName("primary")
        self._accept_btn.setMinimumWidth(180)
        self._accept_btn.setEnabled(False)
        self._accept_btn.clicked.connect(self._on_accept)
        btn_layout.addWidget(self._accept_btn)

        layout.addLayout(btn_layout)

    def _on_checkbox_toggled(self, checked: bool):
        self._accept_btn.setEnabled(checked)

    def _on_accept(self):
        self._accepted = True
        self._save_acceptance()
        self.accept()

    def _save_acceptance(self):
        """Save acceptance state to config."""
        config_dir = os.path.expanduser("~/.kalinova")
        os.makedirs(config_dir, exist_ok=True)
        config_file = os.path.join(config_dir, "state.json")

        state = {}
        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    state = json.load(f)
            except Exception:
                pass

        state["disclaimer_accepted"] = True
        state["accepted_at"] = __import__("datetime").datetime.now().isoformat()

        with open(config_file, "w") as f:
            json.dump(state, f, indent=2)

        logger.info("Disclaimer accepted and saved.")

    @staticmethod
    def was_accepted() -> bool:
        """Check if the disclaimer was previously accepted."""
        config_file = os.path.expanduser("~/.kalinova/state.json")
        if not os.path.exists(config_file):
            return False
        try:
            with open(config_file, "r") as f:
                state = json.load(f)
            return state.get("disclaimer_accepted", False)
        except Exception:
            return False

    @property
    def accepted(self) -> bool:
        return self._accepted
