"""
Next-Step Action Card for Kali-Nova Dashboard.
Displays ML scenario recommendation, confidence score, rationale, and one-click execution.
"""

from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from core.ml.ml_advisor import MLAdvisor
from core.app_state import app_state


class NextStepCard(QFrame):
    """
    Interactive Cyber Dashboard Widget rendering prescribed ML next actions,
    confidence probability gauge, rationale badges, and one-click auto-fill workflow buttons.
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
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(10)

        self.setStyleSheet("""
            QFrame#NextStepCard {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0f192e, stop:0.5 #0c1424, stop:1 #111c33);
                border: 1px solid #1e355b;
                border-left: 4px solid #00f0ff;
                border-radius: 12px;
            }
            QFrame#NextStepCard:hover {
                border-color: #38bdf8;
            }
        """)

        # 1. Header: Directive Icon + Category Title + High-Tech Confidence Badge
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        self.directive_tag = QLabel("⚡ ML SCENARIO INTELLIGENCE // RECOMMENDED NEXT ACTION")
        self.directive_tag.setStyleSheet("""
            font-size: 11px;
            font-weight: 800;
            color: #00f0ff;
            letter-spacing: 1.2px;
            text-transform: uppercase;
        """)
        header_layout.addWidget(self.directive_tag)

        header_layout.addStretch()

        self.confidence_badge = QLabel("● 95.0% AI CONFIDENCE")
        self.confidence_badge.setStyleSheet("""
            background-color: #052e16;
            color: #34d399;
            font-size: 11px;
            font-weight: 800;
            padding: 4px 12px;
            border-radius: 12px;
            border: 1px solid #059669;
            letter-spacing: 0.5px;
        """)
        header_layout.addWidget(self.confidence_badge)

        layout.addLayout(header_layout)

        # 2. Main Directive Action Title
        self.action_title_label = QLabel("Comprehensive Port & Service Scan (Nmap)")
        self.action_title_label.setStyleSheet("font-size: 17px; font-weight: 800; color: #ffffff; letter-spacing: 0.3px;")
        self.action_title_label.setWordWrap(True)
        layout.addWidget(self.action_title_label)

        # 3. Action Description
        self.action_desc_label = QLabel("Scan target host to identify listening ports and active services.")
        self.action_desc_label.setStyleSheet("font-size: 12px; color: #94a3b8; line-height: 1.4;")
        self.action_desc_label.setWordWrap(True)
        layout.addWidget(self.action_desc_label)

        # 4. Inset Intel Boxes (Rationale & Outcome)
        intel_row = QHBoxLayout()
        intel_row.setSpacing(12)

        # Left Inset: Technical Rationale
        self.rationale_frame = QFrame()
        self.rationale_frame.setStyleSheet("""
            QFrame {
                background-color: #070d18;
                border: 1px solid #172642;
                border-left: 3px solid #00f0ff;
                border-radius: 6px;
                padding: 6px;
            }
        """)
        rationale_layout = QVBoxLayout(self.rationale_frame)
        rationale_layout.setContentsMargins(8, 6, 8, 6)
        rationale_layout.setSpacing(3)

        rationale_hdr = QLabel("💡 STRATEGIC RATIONALE")
        rationale_hdr.setStyleSheet("font-size: 10px; font-weight: 800; color: #38bdf8; letter-spacing: 0.5px;")
        rationale_layout.addWidget(rationale_hdr)

        self.rationale_label = QLabel("Initial assessment stage.")
        self.rationale_label.setStyleSheet("font-size: 11px; color: #cbd5e1;")
        self.rationale_label.setWordWrap(True)
        rationale_layout.addWidget(self.rationale_label)
        intel_row.addWidget(self.rationale_frame, 1)

        # Right Inset: Expected Outcome
        self.outcome_frame = QFrame()
        self.outcome_frame.setStyleSheet("""
            QFrame {
                background-color: #070d18;
                border: 1px solid #172642;
                border-left: 3px solid #10b981;
                border-radius: 6px;
                padding: 6px;
            }
        """)
        outcome_layout = QVBoxLayout(self.outcome_frame)
        outcome_layout.setContentsMargins(8, 6, 8, 6)
        outcome_layout.setSpacing(3)

        outcome_hdr = QLabel("🎯 EXPECTED INTELLIGENCE OUTCOME")
        outcome_hdr.setStyleSheet("font-size: 10px; font-weight: 800; color: #34d399; letter-spacing: 0.5px;")
        outcome_layout.addWidget(outcome_hdr)

        self.outcome_label = QLabel("Discovers listening services and attack surfaces.")
        self.outcome_label.setStyleSheet("font-size: 11px; color: #cbd5e1;")
        self.outcome_label.setWordWrap(True)
        outcome_layout.addWidget(self.outcome_label)
        intel_row.addWidget(self.outcome_frame, 1)

        layout.addLayout(intel_row)

        # 5. Action Button Bar
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        self.execute_btn = QPushButton("⚡ Execute Next Step (Auto-Fill & Launch)")
        self.execute_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.execute_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0284c7, stop:1 #2563eb);
                color: #ffffff;
                font-weight: 800;
                font-size: 13px;
                padding: 10px 22px;
                border-radius: 8px;
                border: 1px solid #38bdf8;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0ea5e9, stop:1 #3b82f6);
                border: 1px solid #7dd3fc;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
        """)
        self.execute_btn.clicked.connect(self.on_execute_clicked)
        btn_layout.addWidget(self.execute_btn, 3)

        self.refresh_btn = QPushButton("🔄 Refresh AI Analysis")
        self.refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #111c30;
                color: #94a3b8;
                font-size: 12px;
                font-weight: 600;
                padding: 10px 16px;
                border-radius: 8px;
                border: 1px solid #1e2f4f;
            }
            QPushButton:hover {
                background-color: #172642;
                color: #f1f5f9;
                border-color: #38bdf8;
            }
        """)
        self.refresh_btn.clicked.connect(self.refresh_guidance)
        btn_layout.addWidget(self.refresh_btn, 1)

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

        self.confidence_badge.setText(f"● {conf}% AI CONFIDENCE")
        if conf >= 85:
            self.confidence_badge.setStyleSheet("background-color: #052e16; color: #34d399; font-size: 11px; font-weight: 800; padding: 4px 12px; border-radius: 12px; border: 1px solid #059669;")
        elif conf >= 65:
            self.confidence_badge.setStyleSheet("background-color: #451a03; color: #fbbf24; font-size: 11px; font-weight: 800; padding: 4px 12px; border-radius: 12px; border: 1px solid #d97706;")
        else:
            self.confidence_badge.setStyleSheet("background-color: #1e1b4b; color: #a5b4fc; font-size: 11px; font-weight: 800; padding: 4px 12px; border-radius: 12px; border: 1px solid #6366f1;")

        self.action_title_label.setText(f"{action_title} ({tool_name})")
        self.action_desc_label.setText(action_desc)
        self.rationale_label.setText(rationale)
        self.outcome_label.setText(outcome)
        self.execute_btn.setText(f"⚡ Execute Directive (Auto-Fill & Launch {tool_name})")

    def on_execute_clicked(self):
        """Emits signal to switch to target tool page with pre-populated parameters."""
        page = self.current_guidance.get("page", "recon_page")
        sub_tool = self.current_guidance.get("sub_tool", "nmap")
        target = self.current_guidance.get("suggested_target", "127.0.0.1")
        flags = self.current_guidance.get("suggested_flags", "")

        self.execute_step_signal.emit(page, sub_tool, target, flags)
