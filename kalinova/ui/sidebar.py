from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal


class Sidebar(QWidget):

    navigate = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setObjectName("sideBar")

        layout = QVBoxLayout()
        layout.setContentsMargins(16, 18, 16, 18)
        layout.setSpacing(8)

        # -----------------------
        # Dashboard
        # -----------------------
        self.dashboard_btn = QPushButton("Dashboard")
        self.dashboard_btn.setObjectName("navButton")
        self.dashboard_btn.clicked.connect(
            lambda: self.navigate.emit("Dashboard")
        )
        layout.addWidget(self.dashboard_btn)

        # -----------------------
        # Recon
        # -----------------------
        self.recon_btn = QPushButton("Recon")
        self.recon_btn.setObjectName("navButton")
        self.recon_btn.clicked.connect(
            lambda: self.navigate.emit("Recon")
        )
        layout.addWidget(self.recon_btn)

        # -----------------------
        # Web Testing
        # -----------------------
        self.web_btn = QPushButton("Web Testing")
        self.web_btn.setObjectName("navButton")
        self.web_btn.clicked.connect(
            lambda: self.navigate.emit("Web")
        )
        layout.addWidget(self.web_btn)

        # -----------------------
        # Future Categories (Placeholders)
        # -----------------------
        self.auth_btn = QPushButton("Authentication")
        self.auth_btn.setObjectName("navButton")
        self.auth_btn.clicked.connect(
            lambda: self.navigate.emit("Auth")
        )
        layout.addWidget(self.auth_btn)

        self.network_btn = QPushButton("Network")
        self.network_btn.setObjectName("navButton")
        self.network_btn.clicked.connect(
            lambda: self.navigate.emit("Network")
        )
        layout.addWidget(self.network_btn)

        self.reports_btn = QPushButton("Reports")
        self.reports_btn.setObjectName("navButton")
        self.reports_btn.clicked.connect(
            lambda: self.navigate.emit("Reports")
        )
        layout.addWidget(self.reports_btn)

        # -----------------------
        # Settings
        # -----------------------
        self.settings_btn = QPushButton("Settings")
        self.settings_btn.setObjectName("navButton")
        self.settings_btn.clicked.connect(
            lambda: self.navigate.emit("Settings")
        )
        layout.addWidget(self.settings_btn)

        layout.addStretch()

        self.setLayout(layout)

