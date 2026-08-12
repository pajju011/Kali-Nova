"""
Tool Helper & Input Assistant Widget for Kali-Nova.
Provides real-time target input format validation, flag cheat-sheet, and workflow guides.
"""

# pyrefly: ignore [missing-import]
from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QCheckBox, QWidget
)
# pyrefly: ignore [missing-import]
from PyQt6.QtCore import Qt
from core.tool_guide import ToolGuide


class ToolHelperWidget(QFrame):
    """
    Embedded Helper widget for security tool forms.
    Validates user input syntax live, explains accepted input formats,
    and displays flag guidance.
    """

    def __init__(self, tool_key: str, parent=None):
        super().__init__(parent)
        self.tool_key = tool_key
        self.tool_info = ToolGuide.get_tool_guide(tool_key)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(10)

        self.setStyleSheet("""
            QFrame {
                background-color: #0f172a;
                border: 1px solid #1e293b;
                border-radius: 8px;
            }
        """)

        # 1. Header with Badge
        header_layout = QHBoxLayout()
        icon = QLabel("💡")
        header_layout.addWidget(icon)

        title = QLabel(f"Tool Assistant: {self.tool_info['name']}")
        title.setStyleSheet("font-size: 13px; font-weight: bold; color: #38bdf8;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        self.status_badge = QLabel("READY")
        self.status_badge.setStyleSheet("""
            background-color: #1e293b;
            color: #94a3b8;
            font-size: 10px;
            font-weight: bold;
            padding: 3px 8px;
            border-radius: 4px;
        """)
        header_layout.addWidget(self.status_badge)

        layout.addLayout(header_layout)

        # 2. Input Validation Message
        self.validation_label = QLabel("Enter a target above to see format guidance.")
        self.validation_label.setStyleSheet("font-size: 11px; color: #cbd5e1;")
        self.validation_label.setWordWrap(True)
        layout.addWidget(self.validation_label)

        # 3. Accepted Formats Summary
        accepted = self.tool_info.get("accepted_inputs", [])
        if accepted:
            formats_text = " • ".join(accepted)
            formats_label = QLabel(f"📌 Accepted Target Formats: {formats_text}")
            formats_label.setStyleSheet("font-size: 11px; color: #64748b;")
            formats_label.setWordWrap(True)
            layout.addWidget(formats_label)

        # 4. Best Practice Pro-Tip
        tip = self.tool_info.get("best_practices", "")
        if tip:
            tip_label = QLabel(f"⚡ Pro-Tip: {tip}")
            tip_label.setStyleSheet("font-size: 11px; color: #f59e0b; font-style: italic;")
            tip_label.setWordWrap(True)
            layout.addWidget(tip_label)

    def validate_text(self, text: str):
        """Live slot called whenever user types in the target input box."""
        is_valid, badge, message = ToolGuide.validate_input(self.tool_key, text)
        self.validation_label.setText(message)

        if not text.strip():
            self.status_badge.setText("EMPTY")
            self.status_badge.setStyleSheet("background-color: #1e293b; color: #94a3b8; font-size: 10px; font-weight: bold; padding: 3px 8px; border-radius: 4px;")
            self.validation_label.setStyleSheet("font-size: 11px; color: #94a3b8;")
        elif is_valid:
            self.status_badge.setText("VALID INPUT")
            self.status_badge.setStyleSheet("background-color: #064e3b; color: #34d399; font-size: 10px; font-weight: bold; padding: 3px 8px; border-radius: 4px; border: 1px solid #059669;")
            self.validation_label.setStyleSheet("font-size: 11px; color: #34d399;")
        else:
            self.status_badge.setText("FORMAT ERROR")
            self.status_badge.setStyleSheet("background-color: #450a0a; color: #f87171; font-size: 10px; font-weight: bold; padding: 3px 8px; border-radius: 4px; border: 1px solid #dc2626;")
            self.validation_label.setStyleSheet("font-size: 11px; color: #f87171;")
