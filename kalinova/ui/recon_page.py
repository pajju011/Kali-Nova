from PyQt6.QtWidgets import (
    QLabel, QLineEdit, QComboBox, QCheckBox,
    QSpinBox, QGroupBox, QHBoxLayout, QVBoxLayout,
    QPushButton, QFileDialog, QFrame
)
from PyQt6.QtCore import pyqtSignal

from core.app_state import app_state
from ui.tool_template import ToolModulePage
from ui.components.tool_helper_widget import ToolHelperWidget
from ui.components.port_advisor_widget import PortAdvisorWidget


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
        self.metagoofil_panel = self._create_metagoofil_panel()
        self.photon_panel = self._create_photon_panel()
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
            tool_id="metagoofil",
            icon="📄",
            name="Metagoofil",
            description="Metadata Extractor",
            panel=self.metagoofil_panel,
            focus_widget=self.metagoofil_domain,
        )
        self.add_tool(
            tool_id="photon",
            icon="⚡",
            name="Photon",
            description="OSINT Crawler",
            panel=self.photon_panel,
            focus_widget=self.photon_url_input,
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

        self.nmap_helper = ToolHelperWidget("nmap")
        self.nmap_target.textChanged.connect(self.nmap_helper.validate_text)

        self.port_advisor = PortAdvisorWidget()
        self.port_advisor.port_profile_selected.connect(lambda p: self.port_input.setText(p))

        self.scan_type = QComboBox()
        self.scan_type.addItems([
            "Quick Scan",
            "Service Detection",
            "Aggressive Scan",
        ])

        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("Custom Port (e.g. 80,443,8080)")

        self.nmap_btn = self.create_primary_button("Run Nmap")
        self.nmap_btn.clicked.connect(self.build_nmap)

        layout.addWidget(QLabel("Target IP / Domain"))
        layout.addWidget(self.nmap_target)
        layout.addWidget(self.nmap_helper)
        layout.addWidget(self.port_advisor)
        layout.addWidget(QLabel("Scan Type"))
        layout.addWidget(self.scan_type)
        layout.addWidget(QLabel("Target Ports"))
        layout.addWidget(self.port_input)
        layout.addWidget(self.nmap_btn)
        layout.addStretch()

        return panel

    def _create_whois_panel(self):
        panel, layout = self.create_panel("🌐 Whois Lookup")

        self.whois_target = QLineEdit()
        self.whois_target.setPlaceholderText("Enter domain (example.com)")

        self.whois_helper = ToolHelperWidget("whois")
        self.whois_target.textChanged.connect(self.whois_helper.validate_text)

        self.whois_btn = self.create_primary_button("Run Whois")
        self.whois_btn.clicked.connect(self.build_whois)

        layout.addWidget(QLabel("Domain"))
        layout.addWidget(self.whois_target)
        layout.addWidget(self.whois_helper)
        layout.addWidget(self.whois_btn)
        layout.addStretch()

        return panel

    def _create_harvester_panel(self):
        panel, layout = self.create_panel("🕵️ theHarvester OSINT")

        self.harvester_domain = QLineEdit()
        self.harvester_domain.setPlaceholderText("Enter domain (e.g. target.com)")

        self.harvester_helper = ToolHelperWidget("theharvester")
        self.harvester_domain.textChanged.connect(self.harvester_helper.validate_text)

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
        layout.addWidget(self.harvester_helper)
        layout.addWidget(QLabel("Data Source"))
        layout.addWidget(self.harvester_source)
        layout.addWidget(self.harvester_btn)
        layout.addStretch()

        return panel

    def _create_metagoofil_panel(self):
        panel, layout = self.create_panel("📄 Metagoofil - Document Metadata Extractor")

        self.metagoofil_domain = QLineEdit()
        self.metagoofil_domain.setPlaceholderText("Target Domain (-d) (e.g. kali.org or target.com)")

        self.metagoofil_helper = ToolHelperWidget("metagoofil")
        self.metagoofil_domain.textChanged.connect(self.metagoofil_helper.validate_text)

        self.metagoofil_filetypes = QLineEdit()
        self.metagoofil_filetypes.setText("pdf")
        self.metagoofil_filetypes.setPlaceholderText("File types (-t) (e.g. pdf,doc,xls,ppt,docx,xlsx,ALL)")

        self.metagoofil_search_max = QSpinBox()
        self.metagoofil_search_max.setRange(1, 10000)
        self.metagoofil_search_max.setValue(100)
        self.metagoofil_search_max.setSuffix(" max search results (-l)")

        self.metagoofil_download_limit = QSpinBox()
        self.metagoofil_download_limit.setRange(1, 10000)
        self.metagoofil_download_limit.setValue(25)
        self.metagoofil_download_limit.setSuffix(" max files to download (-n)")

        self.metagoofil_delay = QSpinBox()
        self.metagoofil_delay.setRange(0, 300)
        self.metagoofil_delay.setValue(30)
        self.metagoofil_delay.setSuffix(" s delay between searches (-e)")

        self.metagoofil_threads = QSpinBox()
        self.metagoofil_threads.setRange(1, 64)
        self.metagoofil_threads.setValue(8)
        self.metagoofil_threads.setSuffix(" downloader threads (-r)")

        self.metagoofil_url_timeout = QSpinBox()
        self.metagoofil_url_timeout.setRange(1, 120)
        self.metagoofil_url_timeout.setValue(15)
        self.metagoofil_url_timeout.setSuffix(" s URL timeout (-i)")

        out_layout = QHBoxLayout()
        self.metagoofil_output_dir = QLineEdit()
        self.metagoofil_output_dir.setPlaceholderText("Save directory (-o) (e.g. kalipdf)")
        self.metagoofil_output_btn = QPushButton("Browse...")
        self.metagoofil_output_btn.clicked.connect(self._browse_metagoofil_output)
        out_layout.addWidget(self.metagoofil_output_dir)
        out_layout.addWidget(self.metagoofil_output_btn)

        self.metagoofil_save_file = QLineEdit()
        self.metagoofil_save_file.setPlaceholderText("Save HTML links file (-f) (e.g. kalipdf.html)")

        self.metagoofil_user_agent = QLineEdit()
        self.metagoofil_user_agent.setPlaceholderText("Custom User-Agent header (-u) (optional)")

        self.chk_metagoofil_download = QCheckBox("Download files locally (-w)")
        self.chk_metagoofil_download.setChecked(True)

        self.metagoofil_btn = self.create_primary_button("Run Metagoofil")
        self.metagoofil_btn.clicked.connect(self.build_metagoofil)

        layout.addWidget(QLabel("Target Domain (-d)"))
        layout.addWidget(self.metagoofil_domain)
        layout.addWidget(self.metagoofil_helper)
        layout.addWidget(QLabel("File Types (-t)"))
        layout.addWidget(self.metagoofil_filetypes)
        layout.addWidget(QLabel("Search & Download Limits"))
        layout.addWidget(self.metagoofil_search_max)
        layout.addWidget(self.metagoofil_download_limit)
        layout.addWidget(QLabel("Output Directory (-o)"))
        layout.addLayout(out_layout)
        layout.addWidget(QLabel("Save HTML Links Output (-f)"))
        layout.addWidget(self.metagoofil_save_file)
        layout.addWidget(QLabel("Performance & Timeout Options"))
        layout.addWidget(self.metagoofil_delay)
        layout.addWidget(self.metagoofil_threads)
        layout.addWidget(self.metagoofil_url_timeout)
        layout.addWidget(QLabel("User Agent (-u)"))
        layout.addWidget(self.metagoofil_user_agent)
        layout.addWidget(self.chk_metagoofil_download)
        layout.addWidget(self.metagoofil_btn)
        layout.addStretch()

        return panel

    def _create_photon_panel(self):
        panel, layout = self.create_panel("⚡ Photon - OSINT Web Crawler")

        self.photon_url_input = QLineEdit()
        self.photon_url_input.setPlaceholderText("Root URL (e.g. http://example.com)")

        self.photon_level_spin = QSpinBox()
        self.photon_level_spin.setRange(1, 10)
        self.photon_level_spin.setValue(2)
        self.photon_level_spin.setSuffix(" crawl depth level (-l)")

        self.photon_threads_spin = QSpinBox()
        self.photon_threads_spin.setRange(1, 100)
        self.photon_threads_spin.setValue(10)
        self.photon_threads_spin.setSuffix(" threads (-t)")

        self.photon_delay_spin = QSpinBox()
        self.photon_delay_spin.setRange(0, 60)
        self.photon_delay_spin.setValue(0)
        self.photon_delay_spin.setSuffix(" s delay between requests (-d)")

        output_layout = QHBoxLayout()
        self.photon_output_input = QLineEdit()
        self.photon_output_input.setPlaceholderText("Custom output directory (-o) (optional)")
        self.photon_output_btn = QPushButton("Browse...")
        self.photon_output_btn.clicked.connect(self._browse_photon_output)
        output_layout.addWidget(self.photon_output_input)
        output_layout.addWidget(self.photon_output_btn)

        self.photon_regex_input = QLineEdit()
        self.photon_regex_input.setPlaceholderText("Custom regex pattern (-r) (optional)")

        self.photon_cookie_input = QLineEdit()
        self.photon_cookie_input.setPlaceholderText("Custom cookie header (-c) (optional)")

        self.photon_user_agent_input = QLineEdit()
        self.photon_user_agent_input.setPlaceholderText("Custom User-Agent header (--user-agent) (optional)")

        self.photon_export_combo = QComboBox()
        self.photon_export_combo.addItems(["none", "csv", "json"])

        self.chk_photon_dns = QCheckBox("Enumerate subdomains & DNS data (--dns)")
        self.chk_photon_keys = QCheckBox("Find secret keys & API tokens (--keys)")
        self.chk_photon_only_urls = QCheckBox("Only extract URLs (--only-urls)")
        self.chk_photon_wayback = QCheckBox("Fetch seed URLs from archive.org (--wayback)")
        self.chk_photon_clone = QCheckBox("Clone website locally (--clone)")
        self.chk_photon_ninja = QCheckBox("Ninja / Stealth mode (--ninja)")
        self.chk_photon_verbose = QCheckBox("Verbose output (-v)")

        self.photon_btn = self.create_primary_button("Run Photon Crawler")
        self.photon_btn.clicked.connect(self.build_photon)

        layout.addWidget(QLabel("Target URL"))
        layout.addWidget(self.photon_url_input)
        layout.addWidget(QLabel("Crawl Level"))
        layout.addWidget(self.photon_level_spin)
        layout.addWidget(QLabel("Threads"))
        layout.addWidget(self.photon_threads_spin)
        layout.addWidget(QLabel("Request Delay"))
        layout.addWidget(self.photon_delay_spin)
        layout.addWidget(QLabel("Output Directory"))
        layout.addLayout(output_layout)
        layout.addWidget(QLabel("Regex Extraction"))
        layout.addWidget(self.photon_regex_input)
        layout.addWidget(QLabel("Cookie Header"))
        layout.addWidget(self.photon_cookie_input)
        layout.addWidget(QLabel("User Agent"))
        layout.addWidget(self.photon_user_agent_input)
        layout.addWidget(QLabel("Export Format"))
        layout.addWidget(self.photon_export_combo)
        layout.addWidget(self.chk_photon_dns)
        layout.addWidget(self.chk_photon_keys)
        layout.addWidget(self.chk_photon_only_urls)
        layout.addWidget(self.chk_photon_wayback)
        layout.addWidget(self.chk_photon_clone)
        layout.addWidget(self.chk_photon_ninja)
        layout.addWidget(self.chk_photon_verbose)
        layout.addWidget(self.photon_btn)
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

    def show_metagoofil_panel(self):
        self.activate_tool("metagoofil")

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

    def _browse_photon_output(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if folder:
            self.photon_output_input.setText(folder)

    def build_photon(self):
        url = self.photon_url_input.text().strip()
        if not url:
            self.emit_validation_error("Target URL is required before running Photon.")
            return

        cmd = ["photon", "-u", url]

        level = self.photon_level_spin.value()
        if level != 2:
            cmd.extend(["-l", str(level)])

        threads = self.photon_threads_spin.value()
        if threads != 10:
            cmd.extend(["-t", str(threads)])

        delay = self.photon_delay_spin.value()
        if delay > 0:
            cmd.extend(["-d", str(delay)])

        output_dir = self.photon_output_input.text().strip()
        if output_dir:
            cmd.extend(["-o", output_dir])

        regex_pat = self.photon_regex_input.text().strip()
        if regex_pat:
            cmd.extend(["-r", regex_pat])

        cookie = self.photon_cookie_input.text().strip()
        if cookie:
            cmd.extend(["-c", cookie])

        user_agent = self.photon_user_agent_input.text().strip()
        if user_agent:
            cmd.extend(["--user-agent", user_agent])

        export_fmt = self.photon_export_combo.currentText()
        if export_fmt != "none":
            cmd.extend(["-e", export_fmt])

        if self.chk_photon_dns.isChecked():
            cmd.append("--dns")
        if self.chk_photon_keys.isChecked():
            cmd.append("--keys")
        if self.chk_photon_only_urls.isChecked():
            cmd.append("--only-urls")
        if self.chk_photon_wayback.isChecked():
            cmd.append("--wayback")
        if self.chk_photon_clone.isChecked():
            cmd.append("--clone")
        if self.chk_photon_ninja.isChecked():
            cmd.append("--ninja")
        if self.chk_photon_verbose.isChecked():
            cmd.append("-v")

        self.run_command.emit(" ".join(cmd))

    def _browse_metagoofil_output(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Save Directory")
        if folder:
            self.metagoofil_output_dir.setText(folder)

    def build_metagoofil(self):
        domain = self.metagoofil_domain.text().strip()
        if not domain:
            self.emit_validation_error("Target domain (-d) is required before running Metagoofil.")
            return

        cmd = ["metagoofil", "-d", domain]

        filetypes = self.metagoofil_filetypes.text().strip()
        if filetypes:
            cmd.extend(["-t", filetypes])
        else:
            cmd.extend(["-t", "pdf"])

        search_max = self.metagoofil_search_max.value()
        if search_max != 100:
            cmd.extend(["-l", str(search_max)])

        download_limit = self.metagoofil_download_limit.value()
        if download_limit != 100:
            cmd.extend(["-n", str(download_limit)])

        out_dir = self.metagoofil_output_dir.text().strip()
        if out_dir:
            cmd.extend(["-o", out_dir])

        save_file = self.metagoofil_save_file.text().strip()
        if save_file:
            cmd.extend(["-f", save_file])

        delay = self.metagoofil_delay.value()
        if delay != 30:
            cmd.extend(["-e", str(delay)])

        threads = self.metagoofil_threads.value()
        if threads != 8:
            cmd.extend(["-r", str(threads)])

        url_timeout = self.metagoofil_url_timeout.value()
        if url_timeout != 15:
            cmd.extend(["-i", str(url_timeout)])

        ua = self.metagoofil_user_agent.text().strip()
        if ua:
            cmd.extend(["-u", ua])

        if self.chk_metagoofil_download.isChecked():
            cmd.append("-w")

        self.run_command.emit(" ".join(cmd))


