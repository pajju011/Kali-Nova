from PyQt6.QtWidgets import (
    QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QLabel, QTabWidget
)
from PyQt6.QtCore import Qt

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
        self.showMaximized()
        self.thread = None
        self._threads = []
        self._thread_consoles = {}
        self._thread_tab_base_titles = {}
        self._tool_run_counts = {}

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
        self.console = Console(panel_title="Bottom Console", output_height=150)
        self.side_console = QWidget()
        self.side_console.setObjectName("sideConsolePanel")
        side_layout = QVBoxLayout(self.side_console)
        side_layout.setContentsMargins(8, 8, 8, 8)
        side_layout.setSpacing(6)
        self.side_console_title = QLabel("Tool Output")
        self.side_console_title.setObjectName("sideConsoleTitle")
        self.side_tabs = QTabWidget()
        self.side_tabs.setObjectName("sideOutputTabs")
        self.side_tabs.setTabsClosable(True)
        self.side_tabs.tabCloseRequested.connect(self._close_output_tab)
        side_layout.addWidget(self.side_console_title)
        side_layout.addWidget(self.side_tabs)
        self.side_console.setMinimumWidth(340)
        self.side_console.setMaximumWidth(520)
        self.side_console.hide()
        self.workspace.setObjectName("workspace")

        # =========================
        # Layout Structure
        # =========================
        main_layout.addWidget(self.topbar)

        middle_layout.addWidget(self.sidebar, 1)
        middle_layout.addWidget(self.workspace, 4)
        middle_layout.addWidget(self.side_console, 2)

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
        self._show_side_output_panel()
        tool_name = self._extract_tool_name(command)
        tab_console, base_title = self._create_output_tab(tool_name)
        self._log_main(f"Starting {base_title}...")
        self._set_main_status("🔄 Preparing to execute...", "running")

        thread = CommandThread(command)
        thread.output_signal.connect(
            lambda message, t=thread: self._handle_thread_output(t, message)
        )
        thread.status_signal.connect(
            lambda status, status_type, t=thread: self._handle_thread_status(
                t, status, status_type
            )
        )
        thread.finished_signal.connect(lambda t=thread: self._on_thread_finished(t))

        self.thread = thread
        self._threads.append(thread)
        self._thread_consoles[thread] = tab_console
        self._thread_tab_base_titles[thread] = base_title
        self._set_thread_tab_running(thread, True)
        thread.start()

    def handle_suggested_tool(self, suggested_tool):
        lower_tool = suggested_tool.lower()

        if "hydra" in lower_tool:
            self._open_tool_panel(
                page_name="Auth",
                panel_method="show_hydra_panel",
                tool_name="Hydra",
                instruction="Configure the form and run it from the Auth page.",
            )
            return

        if "john" in lower_tool:
            self._open_tool_panel(
                page_name="Auth",
                panel_method="show_john_panel",
                tool_name="John",
                instruction="Choose the hash file and run it from the Auth page.",
            )
            return

        if "nikto" in lower_tool:
            self._open_tool_panel(
                page_name="Web",
                panel_method="show_nikto_panel",
                tool_name="Nikto",
                instruction="Configure the target URL and run it from the Web page.",
            )
            return

        if "sqlmap" in lower_tool:
            self._open_tool_panel(
                page_name="Web",
                panel_method="show_sqlmap_panel",
                tool_name="SQLmap",
                instruction="Configure the target URL and run it from the Web page.",
            )
            return

        if "gobuster" in lower_tool:
            self._open_tool_panel(
                page_name="Web",
                panel_method="show_gobuster_panel",
                tool_name="Gobuster",
                instruction="Set URL and wordlist, then run it from the Web page.",
            )
            return

        if "nmap" in lower_tool:
            self._open_tool_panel(
                page_name="Recon",
                panel_method="show_nmap_panel",
                tool_name="Nmap",
                instruction="Configure target details and run it from the Recon page.",
            )
            return

        if "whois" in lower_tool:
            self._open_tool_panel(
                page_name="Recon",
                panel_method="show_whois_panel",
                tool_name="Whois",
                instruction="Configure the domain and run it from the Recon page.",
            )
            return

        if "harvester" in lower_tool:
            self._open_tool_panel(
                page_name="Recon",
                panel_method="show_harvester_panel",
                tool_name="Harvester",
                instruction="Set domain/source and run it from the Recon page.",
            )
            return

        if "netcat" in lower_tool:
            self._open_tool_panel(
                page_name="Network",
                panel_method="show_netcat_panel",
                tool_name="Netcat",
                instruction="Set mode and port, then run from the Network page.",
            )
            return

        if "wireshark" in lower_tool:
            self._open_tool_panel(
                page_name="Network",
                panel_method="show_wireshark_panel",
                tool_name="Wireshark",
                instruction="Launch it from the Network page.",
            )
            return

        self._log_main(
            f"Suggested action: {suggested_tool}. Please open the appropriate tool page."
        )
        self._set_main_status("Suggestion ready", "info")

    def handle_validation_error(self, message):
        self._log_main(f"⚠️  {message}")
        self._set_main_status(f"⚠️  {message}", "error")

    def _extract_tool_name(self, command):
        parts = command.strip().split()
        if not parts:
            return "COMMAND"
        return parts[0].upper()

    def _create_output_tab(self, tool_name):
        run_count = self._tool_run_counts.get(tool_name, 0) + 1
        self._tool_run_counts[tool_name] = run_count
        base_title = f"{tool_name} #{run_count}"
        tab_console = Console(panel_title=base_title, output_height=None)
        tab_console.setObjectName("toolOutputConsole")
        tab_index = self.side_tabs.addTab(tab_console, base_title)
        self.side_tabs.setCurrentIndex(tab_index)
        return tab_console, base_title

    def _log_main(self, message):
        self.console.log(message)

    def _set_main_status(self, status, status_type="info"):
        self.console.set_status(status, status_type)

    def _handle_thread_output(self, thread, message):
        self._log_main(message)
        tab_console = self._thread_consoles.get(thread)
        if tab_console is not None:
            tab_console.log(message)

    def _handle_thread_status(self, thread, status, status_type):
        self._set_main_status(status, status_type)
        tab_console = self._thread_consoles.get(thread)
        if tab_console is not None:
            tab_console.set_status(status, status_type)

    def _open_tool_panel(self, page_name, panel_method, tool_name, instruction):
        self.workspace.switch_page(page_name)
        page = self.workspace.pages[page_name]
        getattr(page, panel_method)()
        self._log_main(
            f"Suggestion: {tool_name} selected. {instruction}"
        )
        self._set_main_status(f"Suggestion ready: {tool_name}", "info")

    def _show_side_output_panel(self):
        self.side_console.show()

    def _set_thread_tab_running(self, thread, is_running):
        tab_console = self._thread_consoles.get(thread)
        base_title = self._thread_tab_base_titles.get(thread, "Command")
        if tab_console is None:
            return
        tab_index = self.side_tabs.indexOf(tab_console)
        if tab_index == -1:
            return
        if is_running:
            self.side_tabs.setTabText(tab_index, f"{base_title} [RUN]")
        else:
            self.side_tabs.setTabText(tab_index, f"{base_title} [DONE]")

    def _on_thread_finished(self, thread):
        self._set_thread_tab_running(thread, False)
        if thread in self._threads:
            self._threads.remove(thread)
        if self.thread is thread:
            self.thread = None

    def _close_output_tab(self, tab_index):
        tab_widget = self.side_tabs.widget(tab_index)
        if tab_widget is None:
            return

        for thread, console_widget in list(self._thread_consoles.items()):
            if console_widget is tab_widget:
                if thread.isRunning():
                    thread.stop()
                    thread.wait(1000)
                self._thread_consoles.pop(thread, None)
                self._thread_tab_base_titles.pop(thread, None)
                if thread in self._threads:
                    self._threads.remove(thread)
                if self.thread is thread:
                    self.thread = None
                break

        self.side_tabs.removeTab(tab_index)
        tab_widget.deleteLater()
        if self.side_tabs.count() == 0:
            self.side_console.hide()

    def closeEvent(self, event):
        running_threads = list(self._threads)
        if running_threads:
            self._set_main_status("Stopping running commands before exit...", "running")
            self._log_main("Stopping running commands before exit...")
        for thread in running_threads:
            if thread.isRunning():
                thread.stop()
                thread.wait(3000)
                if thread.isRunning():
                    thread.terminate()
                    thread.wait(1000)

        self._threads.clear()
        self._thread_consoles.clear()
        self._thread_tab_base_titles.clear()
        self.thread = None
        super().closeEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_F11:
            if self.isFullScreen():
                self.showMaximized()
                self._log_main("Switched to Maximized window mode.")
            else:
                self.showFullScreen()
                self._log_main("Switched to Full Screen mode (Press F11 or Esc to exit).")
        elif event.key() == Qt.Key.Key_Escape and self.isFullScreen():
            self.showMaximized()
            self._log_main("Switched to Maximized window mode.")
        else:
            super().keyPressEvent(event)

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

            #toolModulePage {
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

            QWidget#sideConsolePanel {
                border-left: 1px solid #2a3958;
                background-color: #0e1728;
                border-radius: 10px;
            }

            QLabel#consoleTitle,
            QLabel#sideConsoleTitle {
                font-size: 12px;
                font-weight: 700;
                color: #bcd0f5;
                padding: 0 4px;
            }

            QTabWidget#sideOutputTabs::pane {
                border: 1px solid #2b3a57;
                border-radius: 8px;
                background-color: #0e1728;
            }

            QTabWidget#sideOutputTabs QTabBar::tab {
                background-color: #192741;
                color: #cfe0ff;
                border: 1px solid #2f4568;
                padding: 6px 10px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }

            QTabWidget#sideOutputTabs QTabBar::tab:selected {
                background-color: #24406e;
                border-color: #3d78d8;
                color: #f4f8ff;
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
