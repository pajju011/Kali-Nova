"""
Next-Step Action Card for Kali-Nova Dashboard.
Displays ML scenario recommendation, confidence score, rationale, and one-click execution.
"""

# pyrefly: ignore [missing-import]
from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget
)
# pyrefly: ignore [missing-import]
from PyQt6.QtCore import pyqtSignal, Qt
from core.ml.ml_advisor import MLAdvisor
from core.app_state import app_state


class NextStepCard(QFrame):
    """
    Interactive Dashboard Widget that renders the prescribed ML next action,
    confidence probability gauge, and one-click workflow navigation button.
    """

    # Signal: (page_name, sub_tool_key, suggested_target, suggested_flags)
    execute_step_signal = pyqtSignal(str, str, str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("NextStepCard")
        self.current_guidance = {}
        self.init_ui()
        self.refresh_guidance()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(12)

        self.setStyleSheet("""
            QFrame#NextStepCard {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1a1e2e, stop:1 #131722);
                border: 1px solid #2e3856;
                border-radius: 12px;
            }
        """)

        # 1. Header: Icon + Title + Confidence Badge
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        icon_label = QLabel("🚀")
        icon_label.setStyleSheet("font-size: 20px;")
        header_layout.addWidget(icon_label)

        self.header_title = QLabel("ML Scenario Intelligence: Recommended Next Step")
        self.header_title.setStyleSheet("font-size: 14px; font-weight: 700; color: #38bdf8;")
        header_layout.addWidget(self.header_title)

        header_layout.addStretch()

        self.confidence_badge = QLabel("95.0% Confidence")
        self.confidence_badge.setStyleSheet("""
            background-color: #064e3b;
            color: #34d399;
            font-size: 11px;
            font-weight: bold;
            padding: 4px 10px;
            border-radius: 6px;
            border: 1px solid #059669;
        """)
        header_layout.addWidget(self.confidence_badge)

        layout.addLayout(header_layout)

        # 2. Action Goal & Tool Name
        self.action_title_label = QLabel("Comprehensive Port & Service Scan (Nmap)")
        self.action_title_label.setStyleSheet("font-size: 16px; font-weight: 700; color: #f8fafc;")
        self.action_title_label.setWordWrap(True)
        layout.addWidget(self.action_title_label)

        # 3. Action Description
        self.action_desc_label = QLabel("Scan target host to identify listening ports and active services.")
        self.action_desc_label.setStyleSheet("font-size: 12px; color: #94a3b8; line-height: 1.4;")
        self.action_desc_label.setWordWrap(True)
        layout.addWidget(self.action_desc_label)

        # 4. Rationale Container Box
        self.rationale_frame = QFrame()
        self.rationale_frame.setStyleSheet("""
            QFrame {
                background-color: #0f172a;
                border-left: 3px solid #38bdf8;
                border-radius: 4px;
                padding: 6px 10px;
            }
        """)
        rationale_layout = QVBoxLayout(self.rationale_frame)
        rationale_layout.setContentsMargins(8, 6, 8, 6)
        rationale_layout.setSpacing(4)

        rationale_header = QLabel("💡 Why this step? (Technical Rationale)")
        rationale_header.setStyleSheet("font-size: 11px; font-weight: bold; color: #38bdf8;")
        rationale_layout.addWidget(rationale_header)

        self.rationale_label = QLabel("Initial assessment stage.")
        self.rationale_label.setStyleSheet("font-size: 11px; color: #cbd5e1;")
        self.rationale_label.setWordWrap(True)
        rationale_layout.addWidget(self.rationale_label)

        layout.addWidget(self.rationale_frame)

        # 5. Expected Outcome Box
        self.outcome_label = QLabel("🎯 Expected Outcome: Identifies listening services.")
        self.outcome_label.setStyleSheet("font-size: 11px; color: #a7f3d0; font-style: italic;")
        self.outcome_label.setWordWrap(True)
        layout.addWidget(self.outcome_label)

        # 6. Action Button Bar
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        self.execute_btn = QPushButton("⚡ Execute Next Step (Auto-Fill & Launch)")
        self.execute_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.execute_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0284c7, stop:1 #0369a1);
                color: #ffffff;
                font-weight: bold;
                font-size: 13px;
                padding: 10px 18px;
                border-radius: 8px;
                border: 1px solid #38bdf8;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0ea5e9, stop:1 #0284c7);
                border: 1px solid #7dd3fc;
            }
            QPushButton:pressed {
                background-color: #0369a1;
            }
        """)
        self.execute_btn.clicked.connect(self.on_execute_clicked)
        btn_layout.addWidget(self.execute_btn)

        self.refresh_btn = QPushButton("🔄 Refresh AI Analysis")
        self.refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #1e293b;
                color: #94a3b8;
                font-size: 12px;
                padding: 10px 14px;
                border-radius: 8px;
                border: 1px solid #334155;
            }
            QPushButton:hover {
                background-color: #334155;
                color: #f1f5f9;
                border: 1px solid #475569;
            }
        """)
        self.refresh_btn.clicked.connect(self.refresh_guidance)
        btn_layout.addWidget(self.refresh_btn)

        layout.addLayout(btn_layout)

    def refresh_guidance(self):
        """Re-evaluates ML scenario guidance and updates UI."""
        self.current_guidance = MLAdvisor.get_guidance()
        
        conf = self.current_guidance.get("confidence", 85.0)
        tool_name = self.current_guidance.get("tool_name", "Tool")
        action_title = self.current_guidance.get("action_title", "Recommended Step")
        action_desc = self.current_guidance.get("action_desc", "")
        rationale = self.current_guidance.get("rationale", "")
        outcome = self.current_guidance.get("expected_outcome", "")

        self.confidence_badge.setText(f"{conf}% ML Confidence")
        if conf >= 85:
            self.confidence_badge.setStyleSheet("background-color: #064e3b; color: #34d399; font-size: 11px; font-weight: bold; padding: 4px 10px; border-radius: 6px; border: 1px solid #059669;")
        elif conf >= 65:
            self.confidence_badge.setStyleSheet("background-color: #451a03; color: #fbbf24; font-size: 11px; font-weight: bold; padding: 4px 10px; border-radius: 6px; border: 1px solid #d97706;")
        else:
            self.confidence_badge.setStyleSheet("background-color: #312e81; color: #a5b4fc; font-size: 11px; font-weight: bold; padding: 4px 10px; border-radius: 6px; border: 1px solid #6366f1;")

        self.action_title_label.setText(f"{action_title} ({tool_name})")
        self.action_desc_label.setText(action_desc)
        self.rationale_label.setText(rationale)
        self.outcome_label.setText(f"🎯 Expected Outcome: {outcome}")
        self.execute_btn.setText(f"⚡ Execute Next Step (Launch {tool_name})")

    def on_execute_clicked(self):
        """Emits signal to switch to target tool page with pre-populated parameters."""
        page = self.current_guidance.get("page", "recon_page")
        sub_tool = self.current_guidance.get("sub_tool", "nmap")
        target = self.current_guidance.get("suggested_target", "127.0.0.1")
        flags = self.current_guidance.get("suggested_flags", "")

        self.execute_step_signal.emit(page, sub_tool, target, flags)
