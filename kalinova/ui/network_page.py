from PyQt6.QtWidgets import (
    QLabel, QLineEdit, QComboBox, QCheckBox,
    QSpinBox, QGroupBox, QHBoxLayout, QVBoxLayout,
    QPushButton, QFileDialog
)
from PyQt6.QtCore import Qt, pyqtSignal

from ui.tool_template import ToolModulePage


class NetworkPage(ToolModulePage):

    run_command = pyqtSignal(str)

    def __init__(self):
        super().__init__(
            title="Network Tools",
            accent_color="#8b5cf6",
            subtitle="Select a network tool to configure commands before execution.",
        )

        self.netcat_panel = self._create_netcat_panel()
        self.wireshark_panel = self._create_wireshark_panel()
        self.wifite_panel = self._create_wifite_panel()
        self.sslscan_panel = self._create_sslscan_panel()
        self.sslyze_panel = self._create_sslyze_panel()
        self.tlssled_panel = self._create_tlssled_panel()

        self.add_tool(
            tool_id="netcat",
            icon="🔗",
            name="Netcat",
            description="Network Utility",
            panel=self.netcat_panel,
            focus_widget=self.netcat_target_input,
        )
        self.add_tool(
            tool_id="wireshark",
            icon="🔎",
            name="Wireshark",
            description="Packet Analysis",
            panel=self.wireshark_panel,
        )
        self.add_tool(
            tool_id="wifite",
            icon="📡",
            name="Wifite",
            description="Wireless Auditor",
            panel=self.wifite_panel,
            focus_widget=self.wifite_interface_input,
        )
        self.add_tool(
            tool_id="sslscan",
            icon="🔒",
            name="SSLScan",
            description="SSL/TLS Scanner",
            panel=self.sslscan_panel,
            focus_widget=self.sslscan_target_input,
        )
        self.add_tool(
            tool_id="sslyze",
            icon="🔐",
            name="SSLyze",
            description="Full-Featured SSL Scanner",
            panel=self.sslyze_panel,
            focus_widget=self.sslyze_target_input,
        )
        self.add_tool(
            tool_id="tlssled",
            icon="🛡️",
            name="TLSSLed",
            description="SSL/TLS Evaluator",
            panel=self.tlssled_panel,
            focus_widget=self.tlssled_host_input,
        )

    def _create_netcat_panel(self):
        panel, layout = self.create_panel("🔗 Netcat Utility")

        self.netcat_target_input = QLineEdit()
        self.netcat_target_input.setPlaceholderText("Target IP")

        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("Port")

        self.mode_dropdown = QComboBox()
        self.mode_dropdown.addItems([
            "Connect to Target",
            "Listen Mode",
        ])

        self.netcat_btn = self.create_primary_button("Run Netcat")
        self.netcat_btn.clicked.connect(self.build_netcat)

        layout.addWidget(QLabel("Target IP"))
        layout.addWidget(self.netcat_target_input)
        layout.addWidget(QLabel("Port"))
        layout.addWidget(self.port_input)
        layout.addWidget(QLabel("Mode"))
        layout.addWidget(self.mode_dropdown)
        layout.addWidget(self.netcat_btn)
        layout.addStretch()

        return panel

    def _create_wireshark_panel(self):
        panel, layout = self.create_panel("🔎 Wireshark Packet Analyzer")

        info_label = QLabel(
            "Launch Wireshark to start live packet capture and analysis."
        )
        info_label.setWordWrap(True)

        self.wireshark_btn = self.create_primary_button("Launch Wireshark")
        self.wireshark_btn.clicked.connect(self.launch_wireshark)

        layout.addWidget(info_label)
        layout.addWidget(self.wireshark_btn)
        layout.addStretch()

        return panel

    def _create_wifite_panel(self):
        panel, layout = self.create_panel("📡 Wifite 2 Wireless Auditor")

        # Mode Selection
        layout.addWidget(QLabel("Operation Mode"))
        self.wifite_mode_combo = QComboBox()
        self.wifite_mode_combo.addItems([
            "Audit Scan (Default)",
            "Show Cracked Networks (--cracked)",
            "Show Ignored Networks (--ignored)",
            "Check .cap File (--check)",
            "Update MAC Database (--update-db)"
        ])
        self.wifite_mode_combo.currentIndexChanged.connect(self._on_wifite_mode_changed)
        layout.addWidget(self.wifite_mode_combo)

        # Check File Input (Hidden unless mode is Check .cap File)
        self.wifite_check_file_input = QLineEdit()
        self.wifite_check_file_input.setPlaceholderText("Path to .cap file (e.g. hs/*.cap)")
        self.wifite_check_file_input.hide()
        layout.addWidget(self.wifite_check_file_input)

        # Interface & Channel
        row_iface = QHBoxLayout()
        v_iface = QVBoxLayout()
        v_iface.addWidget(QLabel("Wireless Interface (-i)"))
        self.wifite_interface_input = QLineEdit()
        self.wifite_interface_input.setPlaceholderText("e.g. wlan0mon")
        v_iface.addWidget(self.wifite_interface_input)

        v_chan = QVBoxLayout()
        v_chan.addWidget(QLabel("Channel (-c)"))
        self.wifite_channel_input = QLineEdit()
        self.wifite_channel_input.setPlaceholderText("e.g. 1,3-6")
        v_chan.addWidget(self.wifite_channel_input)

        row_iface.addLayout(v_iface)
        row_iface.addLayout(v_chan)
        layout.addLayout(row_iface)

        # Protocol Filters Group
        proto_group = QGroupBox("Protocol Filters")
        proto_layout = QHBoxLayout()
        self.chk_wep = QCheckBox("WEP (--wep)")
        self.chk_wpa = QCheckBox("WPA/WPA2 (--wpa)")
        self.chk_wpa3 = QCheckBox("WPA3 (--wpa3)")
        self.chk_owe = QCheckBox("OWE (--owe)")
        self.chk_wps = QCheckBox("WPS (--wps)")
        self.chk_pmkid = QCheckBox("PMKID (--pmkid)")
        proto_layout.addWidget(self.chk_wep)
        proto_layout.addWidget(self.chk_wpa)
        proto_layout.addWidget(self.chk_wpa3)
        proto_layout.addWidget(self.chk_owe)
        proto_layout.addWidget(self.chk_wps)
        proto_layout.addWidget(self.chk_pmkid)
        proto_group.setLayout(proto_layout)
        layout.addWidget(proto_group)

        # Attack Options Group
        attack_group = QGroupBox("Attack & Scannning Settings")
        attack_layout = QVBoxLayout()

        row_chk1 = QHBoxLayout()
        self.chk_verbose = QCheckBox("Verbose (-v)")
        self.chk_kill = QCheckBox("Kill Conflicts (--kill)")
        self.chk_random_mac = QCheckBox("Random MAC (-mac)")
        self.chk_infinite = QCheckBox("Infinite Mode (-inf)")
        row_chk1.addWidget(self.chk_verbose)
        row_chk1.addWidget(self.chk_kill)
        row_chk1.addWidget(self.chk_random_mac)
        row_chk1.addWidget(self.chk_infinite)
        attack_layout.addLayout(row_chk1)

        row_chk2 = QHBoxLayout()
        self.chk_ignore_cracked = QCheckBox("Hide Cracked (-ic)")
        self.chk_clients_only = QCheckBox("Clients Only (--clients-only)")
        self.chk_nodeauths = QCheckBox("No Deauth (--nodeauths)")
        self.chk_skip_crack = QCheckBox("Skip Crack (--skip-crack)")
        row_chk2.addWidget(self.chk_ignore_cracked)
        row_chk2.addWidget(self.chk_clients_only)
        row_chk2.addWidget(self.chk_nodeauths)
        row_chk2.addWidget(self.chk_skip_crack)
        attack_layout.addLayout(row_chk2)

        # Wordlist
        wordlist_layout = QHBoxLayout()
        wordlist_layout.addWidget(QLabel("Wordlist (--dict):"))
        self.wifite_dict_input = QLineEdit()
        self.wifite_dict_input.setPlaceholderText("/usr/share/dict/wordlist-probable.txt")
        self.wifite_dict_btn = QPushButton("Browse...")
        self.wifite_dict_btn.clicked.connect(self._browse_wordlist)
        wordlist_layout.addWidget(self.wifite_dict_input)
        wordlist_layout.addWidget(self.wifite_dict_btn)
        attack_layout.addLayout(wordlist_layout)

        attack_group.setLayout(attack_layout)
        layout.addWidget(attack_group)

        self.wifite_btn = self.create_primary_button("Run Wifite")
        self.wifite_btn.clicked.connect(self.build_wifite)
        layout.addWidget(self.wifite_btn)
        layout.addStretch()

        return panel

    def _create_sslscan_panel(self):
        panel, layout = self.create_panel("🔒 SSLScan")
        self.sslscan_target_input = QLineEdit()
        self.sslscan_target_input.setPlaceholderText("Enter host:port or host")
        self.sslscan_btn = self.create_primary_button("Run SSLScan")
        self.sslscan_btn.clicked.connect(self.build_sslscan)

        layout.addWidget(QLabel("Target"))
        layout.addWidget(self.sslscan_target_input)
        layout.addWidget(self.sslscan_btn)
        layout.addStretch()
        return panel

    def _create_sslyze_panel(self):
        panel, layout = self.create_panel("🔐 SSLyze")
        self.sslyze_target_input = QLineEdit()
        self.sslyze_target_input.setPlaceholderText("Enter host (or host:port)")
        self.sslyze_btn = self.create_primary_button("Run SSLyze")
        self.sslyze_btn.clicked.connect(self.build_sslyze)

        layout.addWidget(QLabel("Target"))
        layout.addWidget(self.sslyze_target_input)
        layout.addWidget(self.sslyze_btn)
        layout.addStretch()
        return panel

    def _create_tlssled_panel(self):
        panel, layout = self.create_panel("🛡️ TLSSLed")
        self.tlssled_host_input = QLineEdit()
        self.tlssled_host_input.setPlaceholderText("Enter host")
        self.tlssled_port_input = QLineEdit()
        self.tlssled_port_input.setPlaceholderText("Enter port")
        self.tlssled_btn = self.create_primary_button("Run TLSSLed")
        self.tlssled_btn.clicked.connect(self.build_tlssled)

        layout.addWidget(QLabel("Host"))
        layout.addWidget(self.tlssled_host_input)
        layout.addWidget(QLabel("Port"))
        layout.addWidget(self.tlssled_port_input)
        layout.addWidget(self.tlssled_btn)
        layout.addStretch()
        usage_label = QLabel()
        usage_label.setTextFormat(Qt.TextFormat.RichText)
        usage_label.setWordWrap(True)
        usage_label.setText("""<pre style='font-family:monospace;'>
TLSSLed Usage Example
Check SSL/TLS on the host (192.168.1.1) and port (443):

root@kali:~# tlssled 192.168.1.1 443
------------------------------------------------------
 TLSSLed - (1.3) based on sslscan and openssl
                  by Raul Siles (www.taddong.com)
------------------------------------------------------
    openssl version: OpenSSL 1.0.1e 11 Feb 2013
    sslscan version 1.8.2
------------------------------------------------------
[*] Analyzing SSL/TLS on 192.168.1.1:443 ...
    ... (truncated output) ...
</pre>""")
        layout.addWidget(usage_label)
        layout.addStretch()
        return panel

    def _on_wifite_mode_changed(self, index):
        if index == 3:  # Check .cap file
            self.wifite_check_file_input.show()
        else:
            self.wifite_check_file_input.hide()

    def _browse_wordlist(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Cracking Wordlist", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            self.wifite_dict_input.setText(file_path)

    def show_netcat_panel(self):
        self.activate_tool("netcat")

    def show_wireshark_panel(self):
        self.activate_tool("wireshark")

    def show_wifite_panel(self):
        self.activate_tool("wifite")

    def show_sslscan_panel(self):
        self.activate_tool("sslscan")

    def show_sslyze_panel(self):
        self.activate_tool("sslyze")

    def show_tlssled_panel(self):
        self.activate_tool("tlssled")

    def build_netcat(self):
        target = self.netcat_target_input.text().strip()
        port = self.port_input.text().strip()
        mode = self.mode_dropdown.currentText()

        if not port:
            self.emit_validation_error("Netcat port is required before running.")
            return

        if mode == "Connect to Target":
            if not target:
                self.emit_validation_error("Netcat target IP is required in connect mode.")
                return
            command = f"nc {target} {port}"
        else:
            command = f"nc -lvnp {port}"

        self.run_command.emit(command)

    def launch_wireshark(self):
        self.run_command.emit("wireshark")

    def build_wifite(self):
        mode = self.wifite_mode_combo.currentText()

        if mode == "Show Cracked Networks (--cracked)":
            self.run_command.emit("wifite --cracked")
            return
        elif mode == "Show Ignored Networks (--ignored)":
            self.run_command.emit("wifite --ignored")
            return
        elif mode == "Update MAC Database (--update-db)":
            self.run_command.emit("wifite --update-db")
            return
        elif mode == "Check .cap File (--check)":
            cap_file = self.wifite_check_file_input.text().strip()
            if not cap_file:
                self.emit_validation_error("A .cap file path is required for handshake checking.")
                return
            self.run_command.emit(f"wifite --check {cap_file}")
            return

        # Audit Scan mode
        cmd = ["wifite"]

        iface = self.wifite_interface_input.text().strip()
        if iface:
            cmd.append(f"-i {iface}")

        chan = self.wifite_channel_input.text().strip()
        if chan:
            cmd.append(f"-c {chan}")

        if self.chk_verbose.isChecked():
            cmd.append("-v")
        if self.chk_kill.isChecked():
            cmd.append("--kill")
        if self.chk_random_mac.isChecked():
            cmd.append("-mac")
        if self.chk_infinite.isChecked():
            cmd.append("-inf")
        if self.chk_ignore_cracked.isChecked():
            cmd.append("-ic")
        if self.chk_clients_only.isChecked():
            cmd.append("--clients-only")
        if self.chk_nodeauths.isChecked():
            cmd.append("--nodeauths")
        if self.chk_skip_crack.isChecked():
            cmd.append("--skip-crack")

        if self.chk_wep.isChecked():
            cmd.append("--wep")
        if self.chk_wpa.isChecked():
            cmd.append("--wpa")
        if self.chk_wpa3.isChecked():
            cmd.append("--wpa3")
        if self.chk_owe.isChecked():
            cmd.append("--owe")
        if self.chk_wps.isChecked():
            cmd.append("--wps")
        if self.chk_pmkid.isChecked():
            cmd.append("--pmkid")

        dictionary = self.wifite_dict_input.text().strip()
        if dictionary:
            cmd.append(f"--dict {dictionary}")

        self.run_command.emit(" ".join(cmd))

    def build_sslscan(self):
        target = self.sslscan_target_input.text().strip()
        if not target:
            self.emit_validation_error("Target host is required before running.")
            return
        self.run_command.emit(f"sslscan {target}")

    def build_sslyze(self):
        target = self.sslyze_target_input.text().strip()
        if not target:
            self.emit_validation_error("Target host is required before running.")
            return
        self.run_command.emit(f"sslyze {target}")

    def build_tlssled(self):
        host = self.tlssled_host_input.text().strip()
        port = self.tlssled_port_input.text().strip()
        if not host or not port:
            self.emit_validation_error("Host and port are required before running.")
            return
        self.run_command.emit(f"tlssled {host} {port}")
