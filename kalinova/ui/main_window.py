from PyQt6.QtWidgets import (
    QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout
)

from ui.sidebar import Sidebar
from ui.topbar import TopBar
from ui.workspace import Workspace
from ui.console import Console
from core.executor import CommandThread


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setObjectName("mainWindow")
        self.setWindowTitle("Kalinova OS")
        self.setGeometry(100, 100, 1300, 800)

        # =========================
        # Central Layout
        # =========================
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        middle_layout = QHBoxLayout()

        # Create Components FIRST
        self.topbar = TopBar()
        self.sidebar = Sidebar()
        self.workspace = Workspace()
        self.console = Console()
        self.workspace.setObjectName("workspace")

        # =========================
        # Layout Structure
        # =========================
        main_layout.addWidget(self.topbar)

        middle_layout.addWidget(self.sidebar, 1)
        middle_layout.addWidget(self.workspace, 4)

        main_layout.addLayout(middle_layout)
        main_layout.addWidget(self.console)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # =========================
        # Navigation Connection
        # =========================
        self.sidebar.navigate.connect(self.workspace.switch_page)

        # =========================
        # Mode Change Connection
        # =========================
        self.topbar.mode_changed.connect(
            self.workspace.pages["Recon"].update_mode
        )

        # =========================
        # Tool Execution Connections
        # =========================

        recon = self.workspace.pages["Recon"]
        recon.run_command.connect(self.execute)
        recon.validation_error.connect(self.handle_validation_error)

        web = self.workspace.pages["Web"]
        web.run_command.connect(self.execute)
        web.validation_error.connect(self.handle_validation_error)

        auth = self.workspace.pages["Auth"]
        auth.run_command.connect(self.execute)
        auth.validation_error.connect(self.handle_validation_error)

        network = self.workspace.pages["Network"]
        network.run_command.connect(self.execute)
        network.validation_error.connect(self.handle_validation_error)

        dashboard = self.workspace.pages["Dashboard"]
        dashboard.run_suggested_signal.connect(self.handle_suggested_tool)

        self._apply_theme()

    # =========================
    # Command Execution
    # =========================
    def execute(self, command):
        # Clear console before new execution
        self.console.clear()
        self.console.set_status("🔄 Preparing to execute...", "running")

        self.thread = CommandThread(command)
        self.thread.output_signal.connect(self.console.log)
        self.thread.status_signal.connect(self.console.set_status)
        self.thread.start()

    def handle_suggested_tool(self, suggested_tool):
        lower_tool = suggested_tool.lower()

        if "hydra" in lower_tool:
            self.workspace.switch_page("Auth")
            self.workspace.pages["Auth"].show_hydra_panel()
            self.console.log("Suggestion: Hydra selected. Configure the form and run it from the Auth page.")
            self.console.set_status("Suggestion ready: Hydra", "info")
            return

        if "nikto" in lower_tool:
            self.workspace.switch_page("Web")
            self.workspace.pages["Web"].show_nikto_panel()
            self.console.log("Suggestion: Nikto selected. Configure the target URL and run it from the Web page.")
            self.console.set_status("Suggestion ready: Nikto", "info")
            return

        if "sqlmap" in lower_tool:
            self.workspace.switch_page("Web")
            self.workspace.pages["Web"].show_sqlmap_panel()
            self.console.log("Suggestion: SQLmap selected. Configure the target URL and run it from the Web page.")
            self.console.set_status("Suggestion ready: SQLmap", "info")
            return

        if "nmap" in lower_tool or "whois" in lower_tool:
            self.workspace.switch_page("Recon")
            if "nmap" in lower_tool:
                self.workspace.pages["Recon"].show_nmap_panel()
                self.console.log("Suggestion: Nmap selected. Configure the target and run it from the Recon page.")
                self.console.set_status("Suggestion ready: Nmap", "info")
            else:
                self.workspace.pages["Recon"].show_whois_panel()
                self.console.log("Suggestion: Whois selected. Configure the domain and run it from the Recon page.")
                self.console.set_status("Suggestion ready: Whois", "info")
            return

        self.console.log(f"Suggested action: {suggested_tool}. Please open the appropriate tool page.")
        self.console.set_status("Suggestion ready", "info")

    def handle_validation_error(self, message):
        self.console.log(f"⚠️  {message}")
        self.console.set_status(f"⚠️  {message}", "error")

    def _apply_theme(self):
        self.setStyleSheet(
            """
            QMainWindow#mainWindow {
                background-color: #0b1220;
            }

            QWidget {
                color: #d6e2ff;
                font-family: 'Segoe UI';
            }

            QWidget#workspace {
                background-color: #0f172a;
                border-left: 1px solid #25324c;
            }

            QWidget#topBar {
                background-color: #101828;
                border-bottom: 1px solid #2a3958;
            }

            QLabel#topTitle {
                font-size: 18px;
                font-weight: 700;
                color: #f3f7ff;
            }

            QComboBox#modeSelector {
                min-width: 120px;
                padding: 7px 10px;
                border: 1px solid #3a4a6c;
                border-radius: 8px;
                background-color: #1a2438;
                color: #e2ecff;
            }

            QLabel#riskLabel {
                font-weight: 700;
                padding: 6px 10px;
                border-radius: 8px;
                background-color: #182235;
                color: #7ee787;
            }

            QLabel#riskLabel[riskLevel="medium"] {
                color: #f3b23f;
            }

            QLabel#riskLabel[riskLevel="high"] {
                color: #ff7a7a;
            }

            QWidget#sideBar {
                background-color: #101a2f;
                border-right: 1px solid #2a3958;
                min-width: 220px;
                max-width: 240px;
            }

            QPushButton#navButton {
                text-align: left;
                padding: 10px 12px;
                border: 1px solid #2d3f61;
                border-radius: 8px;
                background-color: #16233a;
                color: #d7e5ff;
                font-weight: 600;
            }

            QPushButton#navButton:hover {
                background-color: #1f3150;
                border-color: #3d78d8;
            }

            QPushButton#navButton:pressed {
                background-color: #27406a;
            }

            QWidget#toolModulePage {
                background-color: transparent;
            }

            QFrame#toolModuleHeader {
                border: 1px solid #2b3a57;
                border-radius: 14px;
                background-color: #121d31;
            }

            QLabel#toolModuleSubtitle {
                color: #91a8cc;
                font-size: 12px;
            }

            QFrame#toolRow {
                background-color: transparent;
                border: none;
            }

            QFrame#panelContainer {
                border: 1px solid #2b3a57;
                border-radius: 14px;
                background-color: #10192a;
            }

            QGroupBox[class="toolPanelGroup"] {
                border: 1px solid #324466;
                border-radius: 12px;
                margin-top: 14px;
                padding-top: 16px;
                font-size: 14px;
                font-weight: 600;
                color: #d9e6ff;
            }

            QGroupBox[class="toolPanelGroup"]::title {
                subcontrol-origin: margin;
                left: 14px;
                padding: 0 5px;
                color: #e8f0ff;
            }

            QLabel#emptyStateTitle {
                color: #dce8ff;
            }

            QLabel#emptyStateSubtitle {
                color: #8ea2c5;
                font-size: 12px;
            }

            QLineEdit,
            QComboBox,
            QTextEdit,
            QListWidget {
                padding: 9px;
                border: 1px solid #3a4a6c;
                border-radius: 8px;
                background-color: #1a2438;
                color: #e2ecff;
            }

            QLineEdit:focus,
            QComboBox:focus,
            QTextEdit:focus {
                border-color: #4d89ff;
            }

            QPushButton {
                padding: 9px 12px;
                border-radius: 8px;
                border: 1px solid #3a4a6c;
                background-color: #22324f;
                color: #d9e7ff;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #2a3c5d;
            }

            QPushButton[role="primary"] {
                background-color: #2f5eb8;
                border-color: #3567c7;
                color: #f2f7ff;
            }

            QPushButton[role="primary"]:hover {
                background-color: #3a6cca;
            }

            QPushButton[role="secondary"] {
                background-color: #26344f;
            }

            QWidget#consolePanel {
                border-top: 1px solid #2a3958;
                background-color: #0e1728;
            }

            QTextEdit#consoleOutput {
                border: 1px solid #284f35;
                background-color: #08100f;
                color: #6cff9a;
                font-family: 'Consolas';
                font-size: 10px;
            }
            """
        )
