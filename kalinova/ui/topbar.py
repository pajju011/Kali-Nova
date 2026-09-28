import os
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit, QFrame
from PyQt6.QtCore import pyqtSignal, QTimer, QSize, Qt
from PyQt6.QtGui import QIcon, QShortcut, QKeySequence, QPainter, QPixmap
from PyQt6.QtSvg import QSvgRenderer
from core.app_state import app_state
from ui.icon_manager import get_nav_icon_path, get_tool_icon_path


class TopBar(QWidget):

    mode_changed = pyqtSignal(str)
    toggle_output_signal = pyqtSignal()
    search_submitted = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setObjectName("topBar")
        self.setFixedHeight(54)
        self.setStyleSheet("""
            QWidget#topBar {
                background-color: #060b13;
                border-bottom: 1px solid #111e33;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 6, 16, 6)
        layout.setSpacing(14)

        # -------------------------------------------------------------
        # Left: Logo + KALINOVA Brand & Subtitle
        # -------------------------------------------------------------
        brand_layout = QHBoxLayout()
        brand_layout.setSpacing(10)

        logo_path = get_tool_icon_path("kalinova")
        self.logo_label = QLabel()
        self.logo_label.setFixedSize(44, 30)
        if logo_path and os.path.exists(logo_path):
            renderer = QSvgRenderer(logo_path)
            pix = QPixmap(44, 30)
            pix.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pix)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            renderer.render(painter)
            painter.end()
            self.logo_label.setPixmap(pix)

        brand_text_box = QVBoxLayout()
        brand_text_box.setSpacing(1)
        brand_text_box.setContentsMargins(0, 0, 0, 0)

        self.title = QLabel("KALINOVA")
        self.title.setStyleSheet("""
            font-size: 16px;
            font-weight: 900;
            color: #f8fafc;
            letter-spacing: 1.5px;
            font-family: 'Segoe UI', 'Inter', sans-serif;
        """)

        self.subtitle = QLabel("PENETRATION TESTING SUITE")
        self.subtitle.setStyleSheet("""
            font-size: 8.5px;
            font-weight: 800;
            color: #38bdf8;
            letter-spacing: 1px;
            font-family: 'Segoe UI', 'Inter', sans-serif;
        """)

        brand_text_box.addWidget(self.title)
        brand_text_box.addWidget(self.subtitle)

        brand_layout.addWidget(self.logo_label)
        brand_layout.addLayout(brand_text_box)
        layout.addLayout(brand_layout)

        # -------------------------------------------------------------
        # Center: Sleek Cyber Search Bar with Ctrl+K keycap
        # -------------------------------------------------------------
        search_frame = QFrame()
        search_frame.setObjectName("searchContainer")
        search_frame.setStyleSheet("""
            QFrame#searchContainer {
                background-color: #08101e;
                border: 1px solid #162844;
                border-radius: 8px;
                min-width: 420px;
                max-width: 520px;
            }
            QFrame#searchContainer:hover {
                border-color: #2563eb;
            }
        """)
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(10, 2, 10, 2)
        search_layout.setSpacing(6)

        prompt_lbl = QLabel(">_")
        prompt_lbl.setStyleSheet("color: #00f0ff; font-weight: 800; font-size: 12px; font-family: monospace;")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search modules, tools, or type a command...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: none;
                color: #e2e8f0;
                font-size: 11px;
                padding: 4px;
            }
            QLineEdit:focus {
                border: none;
            }
        """)
        self.search_input.returnPressed.connect(lambda: self.search_submitted.emit(self.search_input.text()))

        keycap_lbl = QLabel("Ctrl + K")
        keycap_lbl.setStyleSheet("""
            background-color: #0c182b;
            color: #64748b;
            font-size: 9.5px;
            font-weight: 700;
            padding: 2px 6px;
            border: 1px solid #1a2c4a;
            border-radius: 4px;
            font-family: 'Segoe UI', monospace;
        """)

        search_layout.addWidget(prompt_lbl)
        search_layout.addWidget(self.search_input, 1)
        search_layout.addWidget(keycap_lbl)

        layout.addStretch()
        layout.addWidget(search_frame)
        layout.addStretch()

        # Shortcut Ctrl+K to focus search bar
        shortcut = QShortcut(QKeySequence("Ctrl+K"), self)
        shortcut.activated.connect(self.search_input.setFocus)

        # -------------------------------------------------------------
        # Right: Terminal Output, Mode Pill, Risk Badge
        # -------------------------------------------------------------
        right_layout = QHBoxLayout()
        right_layout.setSpacing(10)

        # Terminal Output dropdown button
        self.output_btn = QPushButton("  Terminal Output  ˇ")
        self.output_btn.setObjectName("outputToggleBtn")
        self.output_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        output_icon_path = get_nav_icon_path("output")
        if output_icon_path and os.path.exists(output_icon_path):
            self.output_btn.setIcon(QIcon(output_icon_path))
            self.output_btn.setIconSize(QSize(14, 14))
        self.output_btn.setToolTip("Toggle / Slide Output Panel (F9 or Ctrl+O)")
        self.output_btn.clicked.connect(self.toggle_output_signal.emit)
        self.output_btn.setStyleSheet("""
            QPushButton#outputToggleBtn {
                padding: 6px 12px;
                font-size: 11px;
                font-weight: 600;
                background-color: #08101e;
                border: 1px solid #162844;
                border-radius: 8px;
                color: #94a3b8;
            }
            QPushButton#outputToggleBtn:hover {
                background-color: #0f1c32;
                border-color: #38bdf8;
                color: #ffffff;
            }
        """)

        # Beginner / Expert Mode Selector
        self.mode_selector = QComboBox()
        self.mode_selector.setObjectName("modeSelector")
        self.mode_selector.addItems(["Beginner", "Expert"])
        self.mode_selector.setCursor(Qt.CursorShape.PointingHandCursor)
        auth_icon_path = get_nav_icon_path("auth")
        if auth_icon_path and os.path.exists(auth_icon_path):
            self.mode_selector.setItemIcon(0, QIcon(auth_icon_path))
            self.mode_selector.setItemIcon(1, QIcon(auth_icon_path))
        self.mode_selector.currentTextChanged.connect(self.change_mode)
        self.mode_selector.setStyleSheet("""
            QComboBox#modeSelector {
                padding: 5px 12px;
                font-size: 11px;
                font-weight: 600;
                background-color: #08101e;
                border: 1px solid #162844;
                border-radius: 8px;
                color: #e2e8f0;
                min-width: 95px;
            }
            QComboBox#modeSelector:hover {
                border-color: #38bdf8;
            }
            QComboBox#modeSelector::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 18px;
                border-left-width: 0px;
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
            }
            QComboBox QAbstractItemView {
                background-color: #08101e;
                border: 1px solid #162844;
                color: #e2e8f0;
                selection-background-color: #1d4ed8;
            }
        """)

        # Risk indicator pill badge
        self.risk_label = QLabel("il|  Risk: LOW")
        self.risk_label.setObjectName("riskLabel")
        self.risk_label.setStyleSheet("""
            QLabel#riskLabel {
                font-size: 11px;
                font-weight: 800;
                padding: 5px 12px;
                border-radius: 6px;
                background-color: #041f17;
                border: 1px solid #059669;
                color: #10b981;
            }
        """)

        right_layout.addWidget(self.output_btn)
        right_layout.addWidget(self.mode_selector)
        right_layout.addWidget(self.risk_label)

        layout.addLayout(right_layout)

        # Auto refresh risk display
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_risk_display)
        self.timer.start(500)

    def change_mode(self, mode):
        app_state.mode = mode
        self.mode_changed.emit(mode)

    def update_risk_display(self):
        risk = app_state.global_risk.upper()
        if risk == "HIGH":
            self.risk_label.setText(f"il|  Risk: {risk}")
            self.risk_label.setStyleSheet("""
                QLabel#riskLabel {
                    font-size: 11px;
                    font-weight: 800;
                    padding: 5px 12px;
                    border-radius: 6px;
                    background-color: #2b0b12;
                    border: 1px solid #e11d48;
                    color: #fb7185;
                }
            """)
        elif risk == "MEDIUM":
            self.risk_label.setText(f"il|  Risk: {risk}")
            self.risk_label.setStyleSheet("""
                QLabel#riskLabel {
                    font-size: 11px;
                    font-weight: 800;
                    padding: 5px 12px;
                    border-radius: 6px;
                    background-color: #2b1a07;
                    border: 1px solid #d97706;
                    color: #fbbf24;
                }
            """)
        else:
            self.risk_label.setText(f"il|  Risk: {risk}")
            self.risk_label.setStyleSheet("""
                QLabel#riskLabel {
                    font-size: 11px;
                    font-weight: 800;
                    padding: 5px 12px;
                    border-radius: 6px;
                    background-color: #041f17;
                    border: 1px solid #059669;
                    color: #10b981;
                }
            """)
