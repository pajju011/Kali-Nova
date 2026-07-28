from PyQt6.QtWidgets import (
    QLabel, QLineEdit, QComboBox, QCheckBox,
    QSpinBox, QGroupBox, QHBoxLayout, QVBoxLayout,
    QPushButton, QFileDialog, QFrame
)
from PyQt6.QtCore import pyqtSignal

from core.app_state import app_state
from ui.tool_template import ToolModulePage


class ReconPage(ToolModulePage):

    run_command = pyqtSignal(str)

    def __init__(self):
        super().__init__(
            title="Reconnaissance & Forensics",
            accent_color="#4e8df8",
            subtitle="Select a recon or forensics tool to reveal its options and execute.",
        )

        self.nmap_panel = self._create_nmap_panel()
        self.whois_panel = self._create_whois_panel()
        self.harvester_panel = self._create_harvester_panel()
        self.autopsy_panel = self._create_autopsy_panel()

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
        self.add_tool(
            tool_id="autopsy",
            icon="🔬",
            name="Autopsy",
            description="Digital Forensics",
            panel=self.autopsy_panel,
            focus_widget=self.autopsy_locker_input,
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

    def _create_autopsy_panel(self):
        panel, layout = self.create_panel("🔬 Autopsy Forensic Browser")

        # Evidence Locker Directory (-d)
        locker_layout = QHBoxLayout()
        locker_layout.addWidget(QLabel("Evidence Locker Dir (-d):"))
        self.autopsy_locker_input = QLineEdit()
        self.autopsy_locker_input.setPlaceholderText("e.g. /var/lib/autopsy or custom folder")
        self.autopsy_locker_btn = QPushButton("Browse...")
        self.autopsy_locker_btn.clicked.connect(self._browse_evidence_locker)
        locker_layout.addWidget(self.autopsy_locker_input)
        locker_layout.addWidget(self.autopsy_locker_btn)
        layout.addLayout(locker_layout)

        # Server Port & Remote Address
        row_server = QHBoxLayout()
        v_port = QVBoxLayout()
        v_port.addWidget(QLabel("Server Port (-p)"))
        self.autopsy_port_spin = QSpinBox()
        self.autopsy_port_spin.setRange(1, 65535)
        self.autopsy_port_spin.setValue(9999)
        v_port.addWidget(self.autopsy_port_spin)

        v_remote = QVBoxLayout()
        v_remote.addWidget(QLabel("Remote Host Address"))
        self.autopsy_remote_input = QLineEdit()
        self.autopsy_remote_input.setText("localhost")
        v_remote.addWidget(self.autopsy_remote_input)

        row_server.addLayout(v_port)
        row_server.addLayout(v_remote)
        layout.addLayout(row_server)

        # Cookie Settings Group
        cookie_group = QGroupBox("Cookie Settings")
        cookie_layout = QHBoxLayout()
        self.autopsy_cookie_combo = QComboBox()
        self.autopsy_cookie_combo.addItems([
            "Default (Standard Authentication)",
            "Force Cookie in URL (-c)",
            "Force NO Cookie in URL (-C)"
        ])
        cookie_layout.addWidget(self.autopsy_cookie_combo)
        cookie_group.setLayout(cookie_layout)
        layout.addWidget(cookie_group)

        # Live Analysis Group (-i)
        live_group = QGroupBox("Live Analysis Options (-i)")
        live_layout = QVBoxLayout()
        self.chk_live_analysis = QCheckBox("Enable Live System Analysis")
        self.chk_live_analysis.toggled.connect(self._on_live_analysis_toggled)

        self.live_inputs_widget = QFrame()
        live_inputs_layout = QHBoxLayout(self.live_inputs_widget)
        live_inputs_layout.setContentsMargins(0, 4, 0, 0)

        self.autopsy_dev_input = QLineEdit()
        self.autopsy_dev_input.setPlaceholderText("Device (e.g. /dev/sda1)")

        self.autopsy_fs_input = QLineEdit()
        self.autopsy_fs_input.setPlaceholderText("Filesystem (e.g. ext4, ntfs)")

        self.autopsy_mnt_input = QLineEdit()
        self.autopsy_mnt_input.setPlaceholderText("Mount Point (e.g. /mnt)")

        live_inputs_layout.addWidget(self.autopsy_dev_input)
        live_inputs_layout.addWidget(self.autopsy_fs_input)
        live_inputs_layout.addWidget(self.autopsy_mnt_input)

        self.live_inputs_widget.hide()

        live_layout.addWidget(self.chk_live_analysis)
        live_layout.addWidget(self.live_inputs_widget)
        live_group.setLayout(live_layout)
        layout.addWidget(live_group)

        self.autopsy_btn = self.create_primary_button("Launch Autopsy Forensic Server")
        self.autopsy_btn.clicked.connect(self.build_autopsy)
        layout.addWidget(self.autopsy_btn)
        layout.addStretch()

        return panel

    def _browse_evidence_locker(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Evidence Locker Directory")
        if directory:
            self.autopsy_locker_input.setText(directory)

    def _on_live_analysis_toggled(self, checked):
        if checked:
            self.live_inputs_widget.show()
        else:
            self.live_inputs_widget.hide()

    def show_nmap_panel(self):
        self.activate_tool("nmap")

    def show_whois_panel(self):
        self.activate_tool("whois")

    def show_harvester_panel(self):
        self.activate_tool("harvester")

    def show_autopsy_panel(self):
        self.activate_tool("autopsy")

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

    def build_autopsy(self):
        cmd = ["autopsy"]

        cookie_option = self.autopsy_cookie_combo.currentText()
        if "Force Cookie" in cookie_option:
            cmd.append("-c")
        elif "Force NO Cookie" in cookie_option:
            cmd.append("-C")

        locker = self.autopsy_locker_input.text().strip()
        if locker:
            cmd.append(f"-d {locker}")

        if self.chk_live_analysis.isChecked():
            dev = self.autopsy_dev_input.text().strip()
            fs = self.autopsy_fs_input.text().strip()
            mnt = self.autopsy_mnt_input.text().strip()
            if not dev or not fs or not mnt:
                self.emit_validation_error("Live analysis requires Device, Filesystem, and Mount Point fields.")
                return
            cmd.append(f"-i {dev} {fs} {mnt}")

        port = self.autopsy_port_spin.value()
        if port != 9999:
            cmd.append(f"-p {port}")

        remote = self.autopsy_remote_input.text().strip()
        if remote:
            cmd.append(remote)

        self.run_command.emit(" ".join(cmd))

