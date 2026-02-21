from PyQt6.QtWidgets import QStackedWidget

from ui.dashboard_page import DashboardPage
from ui.recon_page import ReconPage
from ui.web_page import WebPage
from ui.auth_page import AuthPage
from ui.network_page import NetworkPage
from ui.reports_page import ReportsPage
from ui.settings_page import SettingsPage


class Workspace(QStackedWidget):

    def __init__(self):
        super().__init__()

        self.pages = {
            "Dashboard": DashboardPage(),
            "Recon": ReconPage(),
            "Web Testing": WebPage(),
            "Authentication": AuthPage(),
            "Network": NetworkPage(),
            "Reports": ReportsPage(),
            "Settings": SettingsPage(),
        }

        for page in self.pages.values():
            self.addWidget(page)

    def switch_page(self, page_name):
        if page_name in self.pages:
            self.setCurrentWidget(self.pages[page_name])