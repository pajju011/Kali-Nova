from PyQt6.QtWidgets import (
    QLabel, QLineEdit, QComboBox, QFileDialog,
    QCheckBox, QPushButton, QGroupBox, QHBoxLayout, QVBoxLayout
)
from PyQt6.QtCore import pyqtSignal

from core.app_state import app_state
from ui.tool_template import ToolModulePage
from ui.components.tool_helper_widget import ToolHelperWidget
from ui.icon_manager import get_tool_icon_path


class WebPage(ToolModulePage):

    run_command = pyqtSignal(str)

    def __init__(self):
        super().__init__(
            title="Web Testing Tools",
            accent_color="#ff5b4d",
            subtitle="Pick a web tool card to reveal only that tool's inputs and controls.",
        )

        self.nikto_panel = self._create_nikto_panel()
        self.sqlmap_panel = self._create_sqlmap_panel()
        self.gobuster_panel = self._create_gobuster_panel()
        self.wfuzz_panel = self._create_wfuzz_panel()
        self.whatweb_panel = self._create_whatweb_panel()

        self.add_tool(
            tool_id="nikto",
            icon=get_tool_icon_path("nikto"),
            name="Nikto",
            description="Web Scanning",
            panel=self.nikto_panel,
            focus_widget=self.nikto_url,
        )
        self.add_tool(
            tool_id="sqlmap",
            icon=get_tool_icon_path("sqlmap"),
            name="SQLmap",
            description="SQL Injection",
            panel=self.sqlmap_panel,
            focus_widget=self.sqlmap_url,
        )
        self.add_tool(
            tool_id="gobuster",
            icon=get_tool_icon_path("gobuster"),
            name="Gobuster",
            description="Directory Brute Force",
            panel=self.gobuster_panel,
            focus_widget=self.gobuster_url,
        )
        self.add_tool(
            tool_id="wfuzz",
            icon=get_tool_icon_path("wfuzz"),
            name="Wfuzz",
            description="Web Application Fuzzer",
            panel=self.wfuzz_panel,
            focus_widget=self.wfuzz_url_input,
        )
        self.add_tool(
            tool_id="whatweb",
            icon=get_tool_icon_path("whatweb"),
            name="WhatWeb",
            description="Web Tech Scanner",
            panel=self.whatweb_panel,
            focus_widget=self.whatweb_url,
        )

    def _create_nikto_panel(self):
        panel, layout = self.create_panel("🔍 Nikto Web Scanner")

        self.nikto_url = QLineEdit()
        self.nikto_url.setPlaceholderText("Enter target URL (http://example.com)")

        self.nikto_helper = ToolHelperWidget("nikto")
        self.nikto_url.textChanged.connect(self.nikto_helper.validate_text)

        self.ssl_option = QComboBox()
        self.ssl_option.addItems(["Auto Detect", "Force SSL"])

        self.nikto_btn = self.create_primary_button("Run Nikto")
        self.nikto_btn.clicked.connect(self.build_nikto)

        layout.addWidget(QLabel("Target URL"))
        layout.addWidget(self.nikto_url)
        layout.addWidget(self.nikto_helper)
        layout.addWidget(QLabel("SSL Option"))
        layout.addWidget(self.ssl_option)
        layout.addWidget(self.nikto_btn)
        layout.addStretch()

        return panel

    def _create_sqlmap_panel(self):
        panel, layout = self.create_panel("💉 SQLmap Injection Testing")

        self.sqlmap_url = QLineEdit()
        self.sqlmap_url.setPlaceholderText(
            "Enter URL with parameter (http://site.com/page?id=1)"
        )

        self.sqlmap_helper = ToolHelperWidget("sqlmap")
        self.sqlmap_url.textChanged.connect(self.sqlmap_helper.validate_text)

        self.sqlmap_level = QComboBox()
        self.sqlmap_level.addItems([
            "Level 1 (Basic)",
            "Level 3 (Medium)",
            "Level 5 (Aggressive)",
        ])

        self.sqlmap_btn = self.create_primary_button("Run SQLmap")
        self.sqlmap_btn.clicked.connect(self.build_sqlmap)

        layout.addWidget(QLabel("Target URL"))
        layout.addWidget(self.sqlmap_url)
        layout.addWidget(self.sqlmap_helper)
        layout.addWidget(QLabel("Detection Level"))
        layout.addWidget(self.sqlmap_level)
        layout.addWidget(self.sqlmap_btn)
        layout.addStretch()

        return panel

    def _create_gobuster_panel(self):
        panel, layout = self.create_panel("🔓 Gobuster Directory Brute Force")

        self.gobuster_url = QLineEdit()
        self.gobuster_url.setPlaceholderText("Enter target URL (http://example.com)")

        self.gobuster_helper = ToolHelperWidget("gobuster")
        self.gobuster_url.textChanged.connect(self.gobuster_helper.validate_text)

        self.wordlist_path = QLineEdit()
        self.wordlist_path.setPlaceholderText("Select wordlist file")

        self.browse_btn = self.create_secondary_button("Browse Wordlist")
        self.browse_btn.clicked.connect(self.select_wordlist)

        self.gobuster_btn = self.create_primary_button("Run Gobuster")
        self.gobuster_btn.clicked.connect(self.build_gobuster)

        layout.addWidget(QLabel("Target URL"))
        layout.addWidget(self.gobuster_url)
        layout.addWidget(self.gobuster_helper)
        layout.addWidget(QLabel("Wordlist"))
        layout.addWidget(self.wordlist_path)
        layout.addWidget(self.browse_btn)
        layout.addWidget(self.gobuster_btn)
        layout.addStretch()

        return panel

    def _create_wfuzz_panel(self):
        panel, layout = self.create_panel("🕸️ Wfuzz Web Fuzzer")

        self.wfuzz_url_input = QLineEdit()
        self.wfuzz_url_input.setPlaceholderText("Enter URL with FUZZ placeholder (e.g., http://example.com/FUZZ)")

        self.wfuzz_btn = self.create_primary_button("Run Wfuzz")
        self.wfuzz_btn.clicked.connect(self.build_wfuzz)

        layout.addWidget(QLabel("Target URL"))
        layout.addWidget(self.wfuzz_url_input)
        layout.addWidget(self.wfuzz_btn)
        layout.addStretch()

        return panel

    def show_nikto_panel(self):
        self.activate_tool("nikto")

    def show_sqlmap_panel(self):
        self.activate_tool("sqlmap")

    def show_gobuster_panel(self):
        self.activate_tool("gobuster")

    def show_wfuzz_panel(self):
        self.activate_tool("wfuzz")

    def build_nikto(self):
        url = self.nikto_url.text().strip()
        if not url:
            self.emit_validation_error("Nikto target URL is required before running.")
            return

        command = f"nikto -h {url}"
        if self.ssl_option.currentText() == "Force SSL":
            command += " -ssl"

        self.run_command.emit(command)

    def build_sqlmap(self):
        url = self.sqlmap_url.text().strip()
        if not url:
            self.emit_validation_error("SQLmap target URL is required before running.")
            return

        command = f"sqlmap -u \"{url}\""

        if app_state.mode == "Beginner":
            command += " --batch --level=1"
        else:
            command += " --batch"

            level = self.sqlmap_level.currentText()
            if "Level 3" in level:
                command += " --level=3"
            elif "Level 5" in level:
                command += " --level=5"

        self.run_command.emit(command)

    def build_gobuster(self):
        url = self.gobuster_url.text().strip()
        wordlist = self.wordlist_path.text().strip()

        if not url:
            self.emit_validation_error("Gobuster target URL is required before running.")
            return

        if not wordlist:
            self.emit_validation_error("Gobuster wordlist path is required before running.")
            return

        self.run_command.emit(f"gobuster dir -u \"{url}\" -w \"{wordlist}\"")

    def build_wfuzz(self):
        url = self.wfuzz_url_input.text().strip()
        if not url:
            self.emit_validation_error("Wfuzz URL is required before running.")
            return
        cmd = f"wfuzz -c -z file,/usr/share/wfuzz/wordlist/general/common.txt --hc 404 {url}"
        self.run_command.emit(cmd)

    def select_wordlist(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Wordlist",
            "",
            "Text Files (*.txt)",
        )

        if file_path:
            self.wordlist_path.setText(file_path)

    def _create_whatweb_panel(self):
        panel, layout = self.create_panel("🌐 WhatWeb - Next Generation Web Scanner")

        self.whatweb_url = QLineEdit()
        self.whatweb_url.setPlaceholderText("Enter Target URL, IP, or range (e.g. 192.168.0.102)")

        # Aggression dropdown
        self.whatweb_aggression = QComboBox()
        self.whatweb_aggression.addItems([
            "Stealthy (Level 1)",
            "Aggressive (Level 3)",
            "Heavy (Level 4)"
        ])

        # HTTP Options group
        http_group = QGroupBox("HTTP Options")
        http_layout = QVBoxLayout()

        self.whatweb_user_agent = QLineEdit()
        self.whatweb_user_agent.setPlaceholderText("Custom User-Agent [Optional]")

        self.whatweb_header = QLineEdit()
        self.whatweb_header.setPlaceholderText("Custom HTTP Header, e.g. Foo:Bar [Optional]")

        self.whatweb_cookie = QLineEdit()
        self.whatweb_cookie.setPlaceholderText("Custom Cookies, e.g. name=value [Optional]")

        http_layout.addWidget(QLabel("User-Agent"))
        http_layout.addWidget(self.whatweb_user_agent)
        http_layout.addWidget(QLabel("Header"))
        http_layout.addWidget(self.whatweb_header)
        http_layout.addWidget(QLabel("Cookies"))
        http_layout.addWidget(self.whatweb_cookie)
        http_group.setLayout(http_layout)

        # Output / Formatting group
        out_group = QGroupBox("Output Settings")
        out_layout = QHBoxLayout()
        self.chk_whatweb_verbose = QCheckBox("Verbose Output (-v)")
        self.chk_whatweb_verbose.setChecked(True)
        self.chk_whatweb_no_errors = QCheckBox("Suppress Errors (--no-errors)")
        out_layout.addWidget(self.chk_whatweb_verbose)
        out_layout.addWidget(self.chk_whatweb_no_errors)
        out_group.setLayout(out_layout)

        self.whatweb_btn = self.create_primary_button("Run WhatWeb")
        self.whatweb_btn.clicked.connect(self.build_whatweb)

        layout.addWidget(QLabel("Target URL/IP"))
        layout.addWidget(self.whatweb_url)
        layout.addWidget(QLabel("Aggression Level"))
        layout.addWidget(self.whatweb_aggression)
        layout.addWidget(http_group)
        layout.addWidget(out_group)
        layout.addWidget(self.whatweb_btn)
        layout.addStretch()

        return panel

    def show_whatweb_panel(self):
        self.activate_tool("whatweb")

    def build_whatweb(self):
        target = self.whatweb_url.text().strip()
        if not target:
            self.emit_validation_error("WhatWeb target URL, IP, or range is required before running.")
            return

        cmd = ["whatweb"]

        # Aggression
        agg = self.whatweb_aggression.currentText()
        if "Level 3" in agg:
            cmd.extend(["-a", "3"])
        elif "Level 4" in agg:
            cmd.extend(["-a", "4"])
        else:
            cmd.extend(["-a", "1"])

        # User-Agent
        ua = self.whatweb_user_agent.text().strip()
        if ua:
            cmd.extend(["-U", f"\"{ua}\""])

        # Header
        hdr = self.whatweb_header.text().strip()
        if hdr:
            cmd.extend(["-H", f"\"{hdr}\""])

        # Cookie
        cookie = self.whatweb_cookie.text().strip()
        if cookie:
            cmd.extend(["-c", f"\"{cookie}\""])

        # Flags
        if self.chk_whatweb_verbose.isChecked():
            cmd.append("-v")
        if self.chk_whatweb_no_errors.isChecked():
            cmd.append("--no-errors")

        cmd.append(target)

        self.run_command.emit(" ".join(cmd))
