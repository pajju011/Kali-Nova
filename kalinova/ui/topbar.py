# pyrefly: ignore [missing-import]
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox, QPushButton
# pyrefly: ignore [missing-import]
from PyQt6.QtCore import pyqtSignal, QTimer
from core.app_state import app_state


class TopBar(QWidget):

    mode_changed = pyqtSignal(str)
    toggle_output_signal = pyqtSignal()
    toggle_ai_copilot_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setObjectName("topBar")

        layout = QHBoxLayout()
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(10)

        self.title = QLabel("KALINOVA")
        self.title.setObjectName("topTitle")

        self.output_btn = QPushButton("📟 Tool Output")
        self.output_btn.setObjectName("outputToggleBtn")
        self.output_btn.setToolTip("Toggle / Slide Output Panel (F9 or Ctrl+O)")
        self.output_btn.clicked.connect(self.toggle_output_signal.emit)
        self.output_btn.setStyleSheet("""
            QPushButton#outputToggleBtn {
                padding: 6px 12px;
                font-size: 12px;
                font-weight: 600;
                background-color: #1a273e;
                border: 1px solid #324669;
                border-radius: 8px;
                color: #a5c2f5;
            }
            QPushButton#outputToggleBtn:hover {
                background-color: #24385a;
                border-color: #4d89ff;
                color: #ffffff;
            }
        """)

        self.mode_selector = QComboBox()
        self.mode_selector.setObjectName("modeSelector")
        self.mode_selector.addItems(["Beginner", "Expert"])
        self.mode_selector.currentTextChanged.connect(self.change_mode)

        self.risk_label = QLabel("Risk: LOW")
        self.risk_label.setObjectName("riskLabel")
        self.risk_label.setProperty("riskLevel", "low")

        layout.addWidget(self.title)
        layout.addStretch()
        layout.addWidget(self.output_btn)
        layout.addWidget(self.mode_selector)
        layout.addWidget(self.risk_label)


        self.setLayout(layout)

        # Auto refresh risk display
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_risk_display)
        self.timer.start(500)

    # ========================
    # Mode Change
    # ========================

    def change_mode(self, mode):
        app_state.mode = mode
        self.mode_changed.emit(mode)

    # ========================
    # Dynamic Risk Color
    # ========================

    def update_risk_display(self):

        risk = app_state.global_risk

        self.risk_label.setText(f"Risk: {risk}")

        self.risk_label.setProperty("riskLevel", risk.lower())
        self.risk_label.style().unpolish(self.risk_label)
        self.risk_label.style().polish(self.risk_label)

