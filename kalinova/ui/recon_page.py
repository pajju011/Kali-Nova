from PyQt6.QtWidgets import QLabel, QLineEdit, QComboBox
from PyQt6.QtCore import pyqtSignal

from core.app_state import app_state
from ui.tool_template import ToolModulePage


class ReconPage(ToolModulePage):

    run_command = pyqtSignal(str)

    def __init__(self):
        super().__init__(
            title="Reconnaissance Tools",
            accent_color="#4e8df8",
            subtitle="Select a recon tool to reveal its options and run a focused scan.",
        )

        self.nmap_panel = self._create_nmap_panel()
        self.whois_panel = self._create_whois_panel()
        self.harvester_panel = self._create_harvester_panel()

        self.add_tool(
            tool_id="nmap",
            icon="🎯",
            name="Nmap",
            description="Port Scanning",
            panel=self.nmap_panel,
            focus_widget=self.nmap_target,
        )
        self.add_tool(
            tool_id="whois",
            icon="🌐",
            name="Whois",
            description="Domain Lookup",
            panel=self.whois_panel,
            focus_widget=self.whois_target,
        )
        self.add_tool(
            tool_id="harvester",
            icon="🕵️",
            name="Harvester",
            description="OSINT",
            panel=self.harvester_panel,
            focus_widget=self.harvester_domain,
        )

        self.update_mode(app_state.mode)

    def _create_nmap_panel(self):
        panel, layout = self.create_panel("🎯 Nmap Configuration")

        self.nmap_target = QLineEdit()
        self.nmap_target.setPlaceholderText("Enter target IP or domain")

        self.scan_type = QComboBox()
        self.scan_type.addItems([
            "Quick Scan",
            "Service Detection",
            "Aggressive Scan",
        ])

        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("Custom Port (optional)")

        self.nmap_btn = self.create_primary_button("Run Nmap")
        self.nmap_btn.clicked.connect(self.build_nmap)

        layout.addWidget(QLabel("Target IP / Domain"))
        layout.addWidget(self.nmap_target)
        layout.addWidget(QLabel("Scan Type"))
        layout.addWidget(self.scan_type)
        layout.addWidget(QLabel("Custom Port"))
        layout.addWidget(self.port_input)
        layout.addWidget(self.nmap_btn)
        layout.addStretch()

        return panel

    def _create_whois_panel(self):
        panel, layout = self.create_panel("🌐 Whois Lookup")

        self.whois_target = QLineEdit()
        self.whois_target.setPlaceholderText("Enter domain (example.com)")

        self.whois_btn = self.create_primary_button("Run Whois")
        self.whois_btn.clicked.connect(self.build_whois)

        layout.addWidget(QLabel("Domain"))
        layout.addWidget(self.whois_target)
        layout.addWidget(self.whois_btn)
        layout.addStretch()

        return panel

    def _create_harvester_panel(self):
        panel, layout = self.create_panel("🕵️ theHarvester OSINT")

        self.harvester_domain = QLineEdit()
        self.harvester_domain.setPlaceholderText("Enter domain")

        self.harvester_source = QComboBox()
        self.harvester_source.addItems([
            "google",
            "bing",
            "yahoo",
            "duckduckgo",
        ])

        self.harvester_btn = self.create_primary_button("Run Harvester")
        self.harvester_btn.clicked.connect(self.build_harvester)

        layout.addWidget(QLabel("Domain"))
        layout.addWidget(self.harvester_domain)
        layout.addWidget(QLabel("Data Source"))
        layout.addWidget(self.harvester_source)
        layout.addWidget(self.harvester_btn)
        layout.addStretch()

        return panel

    def show_nmap_panel(self):
        self.activate_tool("nmap")

    def show_whois_panel(self):
        self.activate_tool("whois")

    def show_harvester_panel(self):
        self.activate_tool("harvester")

    def update_mode(self, mode):
        index = self.scan_type.findText("Aggressive Scan")

        if index == -1:
            return

        item = self.scan_type.model().item(index)

        if mode == "Beginner":
            item.setEnabled(False)
            if self.scan_type.currentText() == "Aggressive Scan":
                self.scan_type.setCurrentIndex(0)
        else:
            item.setEnabled(True)

    def build_nmap(self):
        target = self.nmap_target.text().strip()
        if not target:
            self.emit_validation_error("Nmap target is required before running.")
            return

        app_state.reset_scan()
        scan = self.scan_type.currentText()

        if scan == "Aggressive Scan" and app_state.mode == "Beginner":
            self.emit_validation_error("Aggressive scan is disabled in Beginner mode.")
            return

        command = "nmap "

        if scan == "Service Detection":
            command += "-sV "
        elif scan == "Aggressive Scan":
            command += "-A "

        port = self.port_input.text().strip()
        if port:
            command += f"-p {port} "

        command += target
        self.run_command.emit(command)

    def build_whois(self):
        target = self.whois_target.text().strip()
        if not target:
            self.emit_validation_error("Whois domain is required before running.")
            return

        self.run_command.emit(f"whois {target}")

    def build_harvester(self):
        domain = self.harvester_domain.text().strip()
        if not domain:
            self.emit_validation_error("Harvester domain is required before running.")
            return

        source = self.harvester_source.currentText()
        self.run_command.emit(f"theHarvester -d {domain} -b {source}")
