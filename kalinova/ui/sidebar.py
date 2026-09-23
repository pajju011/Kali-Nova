from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal, QSize
from PyQt6.QtGui import QIcon
from ui.icon_manager import get_nav_icon_path


class Sidebar(QWidget):

    navigate = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setObjectName("sideBar")

        layout = QVBoxLayout()
        layout.setContentsMargins(14, 18, 14, 18)
        layout.setSpacing(8)

        # -----------------------
        # Navigation Buttons with Official SVGs
        # -----------------------
        self.dashboard_btn = self._create_btn("Dashboard", "dashboard", "Dashboard")
        layout.addWidget(self.dashboard_btn)

        self.recon_btn = self._create_btn("Recon", "recon", "Recon")
        layout.addWidget(self.recon_btn)

        self.web_btn = self._create_btn("Web Testing", "web", "Web")
        layout.addWidget(self.web_btn)

        self.auth_btn = self._create_btn("Authentication", "auth", "Auth")
        layout.addWidget(self.auth_btn)

        self.network_btn = self._create_btn("Network", "network", "Network")
        layout.addWidget(self.network_btn)

        self.reports_btn = self._create_btn("Reports", "reports", "Reports")
        layout.addWidget(self.reports_btn)

        self.settings_btn = self._create_btn("Settings", "settings", "Settings")
        layout.addWidget(self.settings_btn)

        layout.addStretch()

        self.setLayout(layout)

    def _create_btn(self, text: str, icon_id: str, nav_target: str) -> QPushButton:
        btn = QPushButton(f"  {text}")
        btn.setObjectName("navButton")
        icon_path = get_nav_icon_path(icon_id)
        if icon_path:
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(20, 20))
        btn.clicked.connect(lambda: self.navigate.emit(nav_target))
        return btn

