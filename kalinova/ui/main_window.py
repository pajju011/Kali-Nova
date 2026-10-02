# pyrefly: ignore [missing-import]
from PyQt6.QtWidgets import (
    QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QLabel, QTabWidget, QSplitter, QPushButton
)
from PyQt6.QtCore import Qt

from ui.sidebar import Sidebar
from ui.topbar import TopBar
from ui.workspace import Workspace
from ui.console import Console
from ui.ai_copilot_drawer import AICopilotDrawer
from core.executor import CommandThread
from core.app_state import app_state
from ui.icon_manager import get_tool_icon_path
from PyQt6.QtGui import QIcon
import os


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setObjectName("mainWindow")
        self.setWindowTitle("Kalinova")
        self.setGeometry(100, 100, 1300, 800)
        self.showMaximized()

        app_icon_path = get_tool_icon_path("kalinova")
        if app_icon_path and os.path.exists(app_icon_path):
            self.setWindowIcon(QIcon(app_icon_path))

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
        self.ai_drawer = AICopilotDrawer(workspace=self.workspace)
        self.ai_drawer.setMinimumWidth(360)
        self.ai_drawer.hide()

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
        self.side_console.setMinimumWidth(0)
        self.side_console.setMaximumWidth(16777215)
        self.side_console.hide()
        self.workspace.setObjectName("workspace")
        self.workspace.setMinimumWidth(0)

        # Splitter between workspace, side output panel, and AI drawer
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.setObjectName("mainSplitter")
        self.splitter.setHandleWidth(8)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.addWidget(self.workspace)
        self.splitter.addWidget(self.side_console)
        self.splitter.addWidget(self.ai_drawer)
        self.splitter.setStretchFactor(0, 3)
        self.splitter.setStretchFactor(1, 2)
        self.splitter.setStretchFactor(2, 2)
        self.splitter.setCollapsible(0, False)

        # =========================
        # Layout Structure
        # =========================
        main_layout.addWidget(self.topbar)

        middle_layout.addWidget(self.sidebar, 0)
        middle_layout.addWidget(self.splitter, 1)

        main_layout.addLayout(middle_layout)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # =========================
        # Navigation Connection
        # =========================
        self.sidebar.navigate.connect(self._on_navigation_change)

        # =========================
        # Mode Change Connection
        # =========================
        self.topbar.mode_changed.connect(
            self.workspace.pages["Recon"].update_mode
        )
        self.topbar.toggle_output_signal.connect(self.toggle_output_panel)
        if hasattr(self.topbar, "toggle_ai_copilot_signal"):
            self.topbar.toggle_ai_copilot_signal.connect(self.toggle_ai_copilot)
        if hasattr(self.topbar, "search_submitted"):
            self.topbar.search_submitted.connect(self._handle_global_search)


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

        for page in [recon, web, auth, network]:
            if hasattr(page, "ai_assist_requested"):
                page.ai_assist_requested.connect(self._handle_in_tool_ai_assist)

        # Connect bottom console input
        self.console.input_submitted.connect(self._handle_main_console_input)

        self._apply_theme()

    def _handle_main_console_input(self, text: str):
        if self.thread is not None and self.thread.isRunning():
            self.thread.send_input(text)
        else:
            self.execute(text)


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
        tab_console.input_submitted.connect(lambda text, t=thread: t.send_input(text))

        self.thread = thread
        self._threads.append(thread)
        self._thread_consoles[thread] = tab_console
        self._thread_tab_base_titles[thread] = base_title
        self._set_thread_tab_running(thread, True)
        thread.start()

    def handle_suggested_tool(self, suggested_tool, target=None, flags=None):
        if not suggested_tool:
            return

        # Handle tuple/list or delimiter-separated payloads
        if isinstance(suggested_tool, (list, tuple)):
            if len(suggested_tool) >= 3:
                suggested_tool, target, flags = str(suggested_tool[0]), str(suggested_tool[1]), str(suggested_tool[2])
            elif len(suggested_tool) == 2:
                suggested_tool, target = str(suggested_tool[0]), str(suggested_tool[1])
            elif len(suggested_tool) == 1:
                suggested_tool = str(suggested_tool[0])

        if isinstance(suggested_tool, str) and "|" in suggested_tool:
            parts = suggested_tool.split("|")
            suggested_tool = parts[0]
            if len(parts) > 1 and parts[1]:
                target = target or parts[1]
            if len(parts) > 2 and parts[2]:
                flags = flags or parts[2]

        auto_target = getattr(app_state, "next_target", "") or ""
        if not auto_target and getattr(app_state, "pipeline_artifacts", {}).get("targets"):
            auto_target = app_state.pipeline_artifacts["targets"][0]
        target = target or auto_target or ""
        flags = flags or ""
        lower_tool = str(suggested_tool).lower()

        # 0. Handle AI Copilot Remediation
        if "remediate" in lower_tool or "copilot" in lower_tool or "hardening" in lower_tool:
            self.workspace.switch_page("Dashboard")
            self.ai_drawer.inspect_and_open()
            self._log_main("Suggestion: AI Defensive Remediation opened with recommended mitigations.")
            self._set_main_status("AI Remediation Active", "info")
            return

        if "hydra" in lower_tool:
            self._open_tool_panel(
                page_name="Auth",
                panel_method="show_hydra_panel",
                tool_name="Hydra",
                instruction="Configure target host/service and run password audit.",
                tool_id="hydra",
                target=target,
                flags=flags
            )
            return

        if "john" in lower_tool:
            self._open_tool_panel(
                page_name="Auth",
                panel_method="show_john_panel",
                tool_name="John",
                instruction="Choose hash file and run offline recovery.",
                tool_id="john",
                target=target,
                flags=flags
            )
            return

        if "hashcat" in lower_tool:
            self._open_tool_panel(
                page_name="Auth",
                panel_method="show_hashcat_panel",
                tool_name="Hashcat",
                instruction="Configure hash target and attack options, then run from Auth page.",
                tool_id="hashcat",
                target=target,
                flags=flags
            )
            return

        if "ncrack" in lower_tool:
            self._open_tool_panel(
                page_name="Auth",
                panel_method="show_ncrack_panel",
                tool_name="Ncrack",
                instruction="Configure network auth target and run cracking scan.",
                tool_id="ncrack",
                target=target,
                flags=flags
            )
            return

        if "sslscan" in lower_tool:
            self._open_tool_panel(
                page_name="Network",
                panel_method="show_sslscan_panel",
                tool_name="SSLScan",
                instruction="Enter target host and verify SSL/TLS ciphers.",
                tool_id="sslscan",
                target=target,
                flags=flags
            )
            return

        if "sslyze" in lower_tool:
            self._open_tool_panel(
                page_name="Network",
                panel_method="show_sslyze_panel",
                tool_name="SSLyze",
                instruction="Enter target host and analyze SSL/TLS configuration.",
                tool_id="sslyze",
                target=target,
                flags=flags
            )
            return

        if "tlssled" in lower_tool:
            self._open_tool_panel(
                page_name="Network",
                panel_method="show_tlssled_panel",
                tool_name="TLSSLed",
                instruction="Enter host and port, then run SSL security audit.",
                tool_id="tlssled",
                target=target,
                flags=flags
            )
            return

        if "nikto" in lower_tool:
            self._open_tool_panel(
                page_name="Web",
                panel_method="show_nikto_panel",
                tool_name="Nikto",
                instruction="Target URL auto-populated. Run web server vulnerability scan.",
                tool_id="nikto",
                target=target,
                flags=flags
            )
            return

        if "sqlmap" in lower_tool:
            self._open_tool_panel(
                page_name="Web",
                panel_method="show_sqlmap_panel",
                tool_name="SQLmap",
                instruction="Target URL auto-populated. Test parameter for SQL injection vulnerabilities.",
                tool_id="sqlmap",
                target=target,
                flags=flags
            )
            return

        if "gobuster" in lower_tool:
            self._open_tool_panel(
                page_name="Web",
                panel_method="show_gobuster_panel",
                tool_name="Gobuster",
                instruction="Target URL auto-populated. Start directory and URI fuzzing.",
                tool_id="gobuster",
                target=target,
                flags=flags
            )
            return

        if "whatweb" in lower_tool:
            self._open_tool_panel(
                page_name="Web",
                panel_method="show_whatweb_panel",
                tool_name="WhatWeb",
                instruction="Target URL auto-populated. Fingerprint web technologies.",
                tool_id="whatweb",
                target=target,
                flags=flags
            )
            return

        if "wfuzz" in lower_tool:
            self._open_tool_panel(
                page_name="Web",
                panel_method="show_wfuzz_panel",
                tool_name="Wfuzz",
                instruction="Target URL auto-populated. Fuzz web endpoints.",
                tool_id="wfuzz",
                target=target,
                flags=flags
            )
            return

        if "nmap" in lower_tool:
            self._open_tool_panel(
                page_name="Recon",
                panel_method="show_nmap_panel",
                tool_name="Nmap",
                instruction="Target host auto-populated. Launch network discovery scan.",
                tool_id="nmap",
                target=target,
                flags=flags
            )
            return

        if "whois" in lower_tool:
            self._open_tool_panel(
                page_name="Recon",
                panel_method="show_whois_panel",
                tool_name="Whois",
                instruction="Target domain auto-populated. Query registrar information.",
                tool_id="whois",
                target=target,
                flags=flags
            )
            return

        if "harvester" in lower_tool:
            self._open_tool_panel(
                page_name="Recon",
                panel_method="show_harvester_panel",
                tool_name="Harvester",
                instruction="Target domain auto-populated. Harvest emails and subdomains.",
                tool_id="harvester",
                target=target,
                flags=flags
            )
            return

        if "metagoofil" in lower_tool:
            self._open_tool_panel(
                page_name="Recon",
                panel_method="show_metagoofil_panel",
                tool_name="Metagoofil",
                instruction="Target domain auto-populated. Extract document metadata.",
                tool_id="metagoofil",
                target=target,
                flags=flags
            )
            return

        if "amass" in lower_tool:
            self._open_tool_panel(
                page_name="Recon",
                panel_method="show_amass_panel",
                tool_name="Amass",
                instruction="Target domain auto-populated. Map external network perimeter.",
                tool_id="amass",
                target=target,
                flags=flags
            )
            return

        if "photon" in lower_tool:
            self._open_tool_panel(
                page_name="Recon",
                panel_method="show_photon_panel",
                tool_name="Photon",
                instruction="Target URL auto-populated. Crawl and scrape OSINT endpoints.",
                tool_id="photon",
                target=target,
                flags=flags
            )
            return

        if "autopsy" in lower_tool or "forensic" in lower_tool:
            self._open_tool_panel(
                page_name="Recon",
                panel_method="show_autopsy_panel",
                tool_name="Autopsy",
                instruction="Configure evidence locker and port, then launch digital forensics.",
                tool_id="autopsy",
                target=target,
                flags=flags
            )
            return

        if "netcat" in lower_tool:
            self._open_tool_panel(
                page_name="Network",
                panel_method="show_netcat_panel",
                tool_name="Netcat",
                instruction="Set mode and port, then run from Network page.",
                tool_id="netcat",
                target=target,
                flags=flags
            )
            return

        if "wireshark" in lower_tool:
            self._open_tool_panel(
                page_name="Network",
                panel_method="show_wireshark_panel",
                tool_name="Wireshark",
                instruction="Launch network packet sniffer from Network page.",
                tool_id="wireshark",
                target=target,
                flags=flags
            )
            return

        if "wifite" in lower_tool or "wifi" in lower_tool or "wpa" in lower_tool:
            self._open_tool_panel(
                page_name="Network",
                panel_method="show_wifite_panel",
                tool_name="Wifite",
                instruction="Configure interface and wireless scan options.",
                tool_id="wifite",
                target=target,
                flags=flags
            )
            return

        if "wash" in lower_tool:
            self._open_tool_panel(
                page_name="Network",
                panel_method="show_wash_panel",
                tool_name="Wash",
                instruction="Scan WPS-enabled access points.",
                tool_id="wash",
                target=target,
                flags=flags
            )
            return

        if "reaver" in lower_tool:
            self._open_tool_panel(
                page_name="Network",
                panel_method="show_reaver_panel",
                tool_name="Reaver",
                instruction="Test WPS PIN resilience.",
                tool_id="reaver",
                target=target,
                flags=flags
            )
            return

        if "sparrow" in lower_tool:
            self._open_tool_panel(
                page_name="Network",
                panel_method="show_sparrowwifi_panel",
                tool_name="Sparrow-WiFi",
                instruction="Launch Sparrow-WiFi spectrum analyzer.",
                tool_id="sparrowwifi",
                target=target,
                flags=flags
            )
            return

        self._log_main(
            f"Suggested action: {suggested_tool}. Please open the appropriate tool page."
        )
        self._set_main_status("Suggestion ready", "info")

    def handle_validation_error(self, message):
        self._log_main(f"⚠️  {message}")
        self._set_main_status(f"⚠️  {message}", "error")
        import os
        if os.environ.get("QT_QPA_PLATFORM") != "offscreen":
            # pyrefly: ignore [missing-import]
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Configuration Required", message)

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

    def _on_navigation_change(self, page_name):
        self.workspace.switch_page(page_name)
        if hasattr(self.sidebar, "set_active_page"):
            self.sidebar.set_active_page(page_name)
        if hasattr(self.workspace, "get_active_context"):
            ctx = self.workspace.get_active_context()
            self.ai_drawer.update_active_context_realtime(
                page_name=ctx.get("page_name", page_name),
                tool_name=ctx.get("tool_name", page_name),
                inputs_dict=ctx.get("inputs", {})
            )

    def _handle_global_search(self, query: str):
        q = query.strip()
        if not q:
            return
        ql = q.lower()
        if ql in ("dashboard", "home"):
            self._on_navigation_change("Dashboard")
        elif ql in ("recon", "nmap", "whois", "harvester", "metagoofil", "amass", "photon", "autopsy"):
            self._on_navigation_change("Recon")
        elif ql in ("web", "nikto", "sqlmap", "gobuster", "wfuzz", "whatweb"):
            self._on_navigation_change("Web")
        elif ql in ("auth", "hydra", "john", "hashcat", "ncrack", "hashid"):
            self._on_navigation_change("Auth")
        elif ql in ("network", "netcat", "wireshark", "wifite", "wash", "reaver", "sslscan", "sslyze"):
            self._on_navigation_change("Network")
        elif ql in ("reports", "report", "logs", "log"):
            self._on_navigation_change("Reports")
        elif ql in ("settings", "config"):
            self._on_navigation_change("Settings")
        elif " " in q:
            self.execute(q)

    def _handle_thread_output(self, thread, message):
        self._log_main(message)
        tab_console = self._thread_consoles.get(thread)
        if tab_console is not None:
            tab_console.log(message)

        # Real-time AI Copilot live stream listener
        tool_name = self._extract_tool_name(getattr(thread, "command", ""))
        clean_msg = message.strip()
        if clean_msg.startswith("[ALERT]") or clean_msg.startswith("[INFO]"):
            ev = "SIGNAL_DETECTED"
            lower_msg = clean_msg.lower()
            if "sql" in lower_msg:
                ev = "SQL_INJECTION"
            elif "secret" in lower_msg or "api_key" in lower_msg:
                ev = "SECRET_LEAK"
            elif "handshake" in lower_msg or "pmkid" in lower_msg:
                ev = "WIRELESS_HANDSHAKE"
            elif "brute" in lower_msg:
                ev = "BRUTE_FORCE"
            elif "email" in lower_msg:
                ev = "EMAIL_ENUM"
            elif "subdomain" in lower_msg:
                ev = "SUBDOMAIN_ENUM"
            elif "wps" in lower_msg:
                ev = "WPS_WIFI_AUDIT"
            elif "forensics" in lower_msg:
                ev = "FORENSICS_ANALYSIS"
            self.ai_drawer.handle_live_event(ev, detail=clean_msg, tool_name=tool_name)

    def _handle_thread_status(self, thread, status, status_type):
        self._set_main_status(status, status_type)
        tab_console = self._thread_consoles.get(thread)
        if tab_console is not None:
            tab_console.set_status(status, status_type)
        self.ai_drawer.handle_live_status(status, status_type)

    def _open_tool_panel(self, page_name, panel_method, tool_name, instruction, tool_id=None, target="", flags=""):
        self.workspace.switch_page(page_name)
        page = self.workspace.pages[page_name]
        getattr(page, panel_method)()
        if tool_id and hasattr(page, "populate_tool_inputs") and target:
            page.populate_tool_inputs(tool_id, target=target, flags=flags)
        self._log_main(
            f"Suggestion: {tool_name} selected. {instruction}"
        )
        self._set_main_status(f"Suggestion ready: {tool_name}", "info")

    def _show_side_output_panel(self):
        self.side_console.show()

    def toggle_ai_copilot(self):
        if not self.ai_drawer.isHidden():
            self.ai_drawer.hide()
        else:
            self.ai_drawer.inspect_and_open()

    def _handle_in_tool_ai_assist(self, ctx_dict):
        self.ai_drawer.inspect_and_open(custom_ctx=ctx_dict)




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
        tool_name = self._extract_tool_name(getattr(thread, "command", ""))
        stdout_txt = "\n".join(getattr(thread, "stdout_lines", []))
        self.ai_drawer.handle_scan_completed(tool_name, stdout_txt)
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

    def set_output_panel_split(self, ratio=0.35):
        if not self.side_console.isVisible():
            self.side_console.show()
        total_w = self.splitter.width()
        if total_w <= 100:
            total_w = max(1000, self.width() - 240)
        side_w = int(total_w * ratio)
        work_w = max(200, total_w - side_w)
        self.splitter.setSizes([work_w, side_w])

    def toggle_output_panel(self):
        if self.side_console.isVisible():
            self.side_console.hide()
        else:
            self.set_output_panel_split(0.40)

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
        elif event.key() == Qt.Key.Key_F9 or (event.key() == Qt.Key.Key_O and (event.modifiers() & Qt.KeyboardModifier.ControlModifier)):
            self.toggle_output_panel()
        else:
            super().keyPressEvent(event)

    def _apply_theme(self):
        self.setStyleSheet(
            """
            QMainWindow#mainWindow {
                background-color: #060b13;
            }

            QWidget {
                color: #cbd5e1;
                font-family: 'Segoe UI', 'Inter', sans-serif;
            }

            QWidget#workspace {
                background-color: #060b13;
                border: none;
            }

            QWidget#topBar {
                background-color: #060b13;
                border-bottom: 1px solid #111e33;
            }

            QWidget#sideBar {
                background-color: #060b13;
                border-right: 1px solid #111e33;
                min-width: 210px;
                max-width: 230px;
            }

            #toolModulePage {
                background-color: #060b13;
            }

            QFrame#toolModuleHeader {
                border: 1px solid #14243e;
                border-radius: 8px;
                background-color: #081220;
            }

            QLabel#toolModuleSubtitle {
                color: #64748b;
                font-size: 11px;
            }

            QFrame#toolRow {
                background-color: transparent;
                border: none;
            }

            QFrame#panelContainer {
                border: 1px solid #14243e;
                border-radius: 8px;
                background-color: #081220;
            }

            QGroupBox[class="toolPanelGroup"] {
                border: 1px solid #14243e;
                border-radius: 8px;
                margin-top: 14px;
                padding-top: 16px;
                font-size: 13px;
                font-weight: 700;
                color: #e2e8f0;
            }

            QGroupBox[class="toolPanelGroup"]::title {
                subcontrol-origin: margin;
                left: 14px;
                padding: 0 5px;
                color: #00f0ff;
            }

            QLabel#emptyStateTitle {
                color: #e2e8f0;
            }

            QLabel#emptyStateSubtitle {
                color: #64748b;
                font-size: 11px;
            }

            QLineEdit,
            QComboBox,
            QTextEdit,
            QListWidget {
                padding: 7px 10px;
                border: 1px solid #162844;
                border-radius: 6px;
                background-color: #08101e;
                color: #e2e8f0;
                font-size: 11px;
            }

            QLineEdit:focus,
            QComboBox:focus,
            QTextEdit:focus {
                border-color: #2563eb;
            }

            QPushButton {
                padding: 7px 12px;
                border-radius: 6px;
                border: 1px solid #162844;
                background-color: #0c182b;
                color: #cbd5e1;
                font-weight: 600;
                font-size: 11px;
            }

            QPushButton:hover {
                background-color: #12243d;
                border-color: #38bdf8;
                color: #ffffff;
            }

            QPushButton[role="primary"] {
                background-color: #1d4ed8;
                border-color: #2563eb;
                color: #ffffff;
                font-weight: 700;
            }

            QPushButton[role="primary"]:hover {
                background-color: #2563eb;
                border-color: #38bdf8;
            }

            QPushButton[role="secondary"] {
                background-color: #0c182b;
                border: 1px solid #162844;
                color: #94a3b8;
            }
            QPushButton[role="secondary"]:hover {
                background-color: #142540;
                color: #ffffff;
            }

            QWidget#consolePanel {
                border-top: 1px solid #111e33;
                background-color: #050c18;
            }

            QWidget#sideConsolePanel {
                border-left: 1px solid #111e33;
                background-color: #050c18;
                border-radius: 8px;
            }

            QLabel#consoleTitle,
            QLabel#sideConsoleTitle {
                font-size: 12px;
                font-weight: 800;
                color: #cbd5e1;
                padding: 2px 4px;
                letter-spacing: 0.5px;
            }

            QPushButton#slideExpandBtn {
                padding: 4px 10px;
                font-size: 10px;
                font-weight: 700;
                background-color: #0c182b;
                border: 1px solid #162844;
                border-radius: 6px;
                color: #38bdf8;
            }
            QPushButton#slideExpandBtn:hover {
                background-color: #162844;
                border-color: #38bdf8;
                color: #ffffff;
            }

            QSplitter#mainSplitter::handle:horizontal {
                background-color: #060b13;
                border-left: 1px solid #111e33;
                border-right: 1px solid #111e33;
                width: 6px;
            }
            QSplitter#mainSplitter::handle:horizontal:hover {
                background-color: #1d4ed8;
            }

            QTabWidget#sideOutputTabs::pane {
                border: 1px solid #14243e;
                border-radius: 6px;
                background-color: #050c18;
            }

            QTabWidget#sideOutputTabs QTabBar::tab {
                background-color: #081220;
                color: #94a3b8;
                border: 1px solid #14243e;
                padding: 5px 12px;
                font-size: 11px;
                font-weight: 600;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }

            QTabWidget#sideOutputTabs QTabBar::tab:selected {
                background-color: #1d4ed8;
                border-color: #2563eb;
                color: #ffffff;
            }

            QTextEdit#consoleOutput {
                border: 1px solid #111e33;
                background-color: #050c18;
                color: #10b981;
                font-family: 'Consolas', 'Cascadia Code', 'Courier New', monospace;
                font-size: 12px;
                line-height: 1.4;
                padding: 8px;
            }

            QScrollBar:vertical {
                border: none;
                background: #060b13;
                width: 6px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #14243e;
                min-height: 20px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical:hover {
                background: #2563eb;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            """
        )
