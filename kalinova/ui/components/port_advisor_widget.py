"""
Smart Port Advisor Widget for Kali-Nova Nmap GUI.
Provides one-click strategic port profile selectors and risk severity indicators.
"""

# pyrefly: ignore [missing-import]
from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton
)
# pyrefly: ignore [missing-import]
from PyQt6.QtCore import pyqtSignal, Qt
from core.port_advisor import PortAdvisor


class PortAdvisorWidget(QFrame):
    """
    Port Prioritization Widget that lets users select high-value port profiles
    and explains why specific ports are critical targets.
    """

    # Signal emitted when a port profile is chosen: emits formatted ports string
    port_profile_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(8)

        self.setStyleSheet("""
            QFrame {
                background-color: #0f172a;
                border: 1px solid #1e293b;
                border-radius: 8px;
            }
        """)

        # 1. Header + Dropdown
        row = QHBoxLayout()
        icon = QLabel("🎯")
        row.addWidget(icon)

        title = QLabel("Smart Port Advisor:")
        title.setStyleSheet("font-size: 12px; font-weight: bold; color: #38bdf8;")
        row.addWidget(title)

        self.profile_combo = QComboBox()
        self.profile_combo.setStyleSheet("""
            QComboBox {
                background-color: #1e293b;
                color: #f8fafc;
                border: 1px solid #334155;
                border-radius: 6px;
                padding: 4px 10px;
                font-size: 11px;
            }
            QComboBox:hover {
                border: 1px solid #38bdf8;
            }
            QComboBox QAbstractItemView {
                background-color: #1e293b;
                color: #f8fafc;
                selection-background-color: #0284c7;
            }
        """)

        self.profile_keys = ["NONE"] + list(PortAdvisor.PORT_PROFILES.keys())
        self.profile_combo.addItem("-- Select Strategic Port Profile --", "NONE")
        for key in self.profile_keys[1:]:
            prof = PortAdvisor.PORT_PROFILES[key]
            self.profile_combo.addItem(prof["name"], key)

        self.profile_combo.currentIndexChanged.connect(self.on_profile_changed)
        row.addWidget(self.profile_combo, 1)

        self.apply_btn = QPushButton("Apply Ports")
        self.apply_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.apply_btn.setStyleSheet("""
            QPushButton {
                background-color: #0284c7;
                color: white;
                font-size: 11px;
                font-weight: bold;
                padding: 5px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #0ea5e9;
            }
            QPushButton:disabled {
                background-color: #1e293b;
                color: #64748b;
                border: 1px solid #334155;
            }
        """)
        self.apply_btn.clicked.connect(self.on_apply_clicked)
        row.addWidget(self.apply_btn)

        layout.addLayout(row)

        # 2. Description & Rationale
        self.desc_label = QLabel()
        self.desc_label.setStyleSheet("font-size: 11px; color: #94a3b8;")
        self.desc_label.setWordWrap(True)
        layout.addWidget(self.desc_label)

        self.rationale_label = QLabel()
        self.rationale_label.setStyleSheet("font-size: 11px; color: #34d399; font-style: italic;")
        self.rationale_label.setWordWrap(True)
        layout.addWidget(self.rationale_label)

        # Initialize text
        self.on_profile_changed(0)

    def on_profile_changed(self, index: int):
        if index <= 0:
            self.desc_label.setText("Select a strategic port profile above or enter target input to view scan recommendations.")
            self.rationale_label.setText("")
            self.apply_btn.setEnabled(False)
        elif 1 <= index < len(self.profile_keys):
            key = self.profile_keys[index]
            prof = PortAdvisor.get_profile(key)
            self.desc_label.setText(prof["description"])
            self.rationale_label.setText(f"💡 Strategy: {prof['rationale']}")
            self.apply_btn.setEnabled(True)

    def on_apply_clicked(self):
        index = self.profile_combo.currentIndex()
        if 1 <= index < len(self.profile_keys):
            key = self.profile_keys[index]
            ports_str = PortAdvisor.get_ports_string(key)
            self.port_profile_selected.emit(ports_str)
