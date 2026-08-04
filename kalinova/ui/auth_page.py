# pyrefly: ignore [missing-import]
from PyQt6.QtWidgets import QLabel, QLineEdit, QComboBox, QFileDialog
# pyrefly: ignore [missing-import]
from PyQt6.QtCore import Qt, pyqtSignal

from ui.tool_template import ToolModulePage


class AuthPage(ToolModulePage):

    run_command = pyqtSignal(str)

    def __init__(self):
        super().__init__(
            title="Authentication Testing",
            accent_color="#f59e0b",
            subtitle="Choose a credential testing tool and the required fields will appear .",
        )

        self.hydra_panel = self._create_hydra_panel()
        self.john_panel = self._create_john_panel()
        self.hash_identifier_panel = self._create_hash_identifier_panel()
        self.hashid_panel = self._create_hashid_panel()
        self.wfuzz_panel = self._create_wfuzz_panel()
        self.tlssled_panel = self._create_tlssled_panel()
        self.sslyze_panel = self._create_sslyze_panel()

        self.add_tool(
            tool_id="hydra",
            icon="⚡",
            name="Hydra",
            description="Brute Force",
            panel=self.hydra_panel,
            focus_widget=self.hydra_target_input,
        )
        self.add_tool(
            tool_id="john",
            icon="🔨",
            name="John",
            description="Hash Cracking",
            panel=self.john_panel,
            focus_widget=self.hash_file,
        )
        self.add_tool(
            tool_id="hash_identifier",
            icon="🔎",
            name="Hash Identifier",
            description="Identify hash types",
            panel=self.hash_identifier_panel,
            focus_widget=self.hash_input,
        )
        self.add_tool(
            tool_id="hashid",
            icon="🔎",
            name="HashID",
            description="Identify hash types (hashid)",
            panel=self.hashid_panel,
            focus_widget=self.hashid_input,
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

    def _create_hydra_panel(self):
        panel, layout = self.create_panel("⚡ Hydra Brute Force")

        self.hydra_target_input = QLineEdit()
        self.hydra_target_input.setPlaceholderText("Enter target IP")

        self.service_dropdown = QComboBox()
        self.service_dropdown.addItems([
            "ssh",
            "ftp",
            "http-get",
            "http-post-form",
        ])

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_file = QLineEdit()
        self.password_file.setPlaceholderText("Select password wordlist")

        self.sslyze_panel = self._create_sslyze_panel()
        self.sslscan_panel = self._create_sslscan_panel()

        self.add_tool(
            tool_id="hydra",
            icon="⚡",
            name="Hydra",
            description="Brute Force",
            panel=self.hydra_panel,
            focus_widget=self.hydra_target_input,
        )
        self.add_tool(
            tool_id="john",
            icon="🔨",
            name="John",
            description="Hash Cracking",
            panel=self.john_panel,
            focus_widget=self.hash_file,
        )

        self.add_tool(
            tool_id="hash_identifier",
            icon="🔎",
            name="Hash Identifier",
            description="Identify hash types",
            panel=self.hash_identifier_panel,
            focus_widget=self.hash_input,
        )
        self.add_tool(
            tool_id="hashid",
            icon="🔎",
            name="HashID",
            description="Identify hash types (hashid)",
            panel=self.hashid_panel,
            focus_widget=self.hashid_input,
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
            tool_id="wfuzz",
            icon="🕸️",
            name="Wfuzz",
            description="Web Application Fuzzer",
            panel=self.wfuzz_panel,
            focus_widget=self.wfuzz_url_input,
        )

    def _create_hydra_panel(self):
        panel, layout = self.create_panel("⚡ Hydra Brute Force")

        self.hydra_target_input = QLineEdit()
        self.hydra_target_input.setPlaceholderText("Enter target IP")

        self.service_dropdown = QComboBox()
        self.service_dropdown.addItems([
            "ssh",
            "ftp",
            "http-get",
            "http-post-form",
        ])

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_file = QLineEdit()
        self.password_file.setPlaceholderText("Select password wordlist")

        self.browse_btn = self.create_secondary_button("Browse Wordlist")
        self.browse_btn.clicked.connect(self.select_wordlist)

        self.hydra_btn = self.create_primary_button("Run Hydra")
        self.hydra_btn.clicked.connect(self.build_hydra)

        layout.addWidget(QLabel("Target IP"))
        layout.addWidget(self.hydra_target_input)
        layout.addWidget(QLabel("Service"))
        layout.addWidget(self.service_dropdown)
        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Password Wordlist"))
        layout.addWidget(self.password_file)
        layout.addWidget(self.browse_btn)
        layout.addWidget(self.hydra_btn)
        layout.addStretch()

        return panel

    def _create_john_panel(self):
        panel, layout = self.create_panel("🔨 John the Ripper")

        self.hash_file = QLineEdit()
        self.hash_file.setPlaceholderText("Select hash file")

        self.browse_hash_btn = self.create_secondary_button("Browse Hash File")
        self.browse_hash_btn.clicked.connect(self.select_hash_file)

        self.john_wordlist = QLineEdit()
        self.john_wordlist.setPlaceholderText("Select wordlist (optional)")

        self.browse_john_wordlist = self.create_secondary_button("Browse Wordlist")
        self.browse_john_wordlist.clicked.connect(self.select_john_wordlist)

        self.john_btn = self.create_primary_button("Run John")
        self.john_btn.clicked.connect(self.build_john)

        layout.addWidget(QLabel("Hash File"))
        layout.addWidget(self.hash_file)
        layout.addWidget(self.browse_hash_btn)
        layout.addWidget(QLabel("Wordlist"))
        layout.addWidget(self.john_wordlist)
        layout.addWidget(self.browse_john_wordlist)
        layout.addWidget(self.john_btn)
        layout.addStretch()

        return panel

    def show_hydra_panel(self):
        self.activate_tool("hydra")

    def show_john_panel(self):
        self.activate_tool("john")

    def show_hash_identifier_panel(self):
        self.activate_tool("hash_identifier")

    def show_hashid_panel(self):
        self.activate_tool("hashid")

    def show_sslscan_panel(self):
        self.activate_tool("sslscan")

    def show_sslyze_panel(self):
        self.activate_tool("sslyze")

    def show_tlssled_panel(self):
        self.activate_tool("tlssled")

    def select_wordlist(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Wordlist",
            "",
            "Text Files (*.txt)",
        )
        if file_path:
            self.password_file.setText(file_path)

    def select_hash_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Hash File",
            "",
            "Text Files (*.txt)",
        )
        if file_path:
            self.hash_file.setText(file_path)

    def select_john_wordlist(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Wordlist",
            "",
            "Text Files (*.txt)",
        )
        if file_path:
            self.john_wordlist.setText(file_path)

    def build_hydra(self):
        target = self.hydra_target_input.text().strip()
        service = self.service_dropdown.currentText()
        username = self.username_input.text().strip()
        wordlist = self.password_file.text().strip()

        if not target:
            self.emit_validation_error("Hydra target IP is required before running.")
            return

        if not username:
            self.emit_validation_error("Hydra username is required before running.")
            return

        if not wordlist:
            self.emit_validation_error("Hydra wordlist path is required before running.")
            return

        self.run_command.emit(
            f"hydra -l \"{username}\" -P \"{wordlist}\" {target} {service}"
        )

    def build_john(self):
        hash_file = self.hash_file.text().strip()
        wordlist = self.john_wordlist.text().strip()

        if not hash_file:
            self.emit_validation_error("John hash file is required before running.")
            return

        command = f"john \"{hash_file}\""
        if wordlist:
            command += f" --wordlist=\"{wordlist}\""

        self.run_command.emit(command)

    def _create_hash_identifier_panel(self):
        panel, layout = self.create_panel("🔎 Hash Identifier")
        self.hash_input = QLineEdit()
        self.hash_input.setPlaceholderText("Enter hash to identify")
        self.hash_btn = self.create_primary_button("Identify Hash")
        self.hash_btn.clicked.connect(self.build_hash_identifier)

        layout.addWidget(QLabel("Hash"))
        layout.addWidget(self.hash_input)
        layout.addWidget(self.hash_btn)
        layout.addStretch()
        return panel

    def build_hash_identifier(self):
        hash_val = self.hash_input.text().strip()
        if not hash_val:
            self.emit_validation_error("Hash value is required before running.")
            return
        # Execute hash-identifier with the provided hash
        self.run_command.emit(f"hash-identifier {hash_val}")

    def _create_hashid_panel(self):
        panel, layout = self.create_panel("🔎 HashID")
        self.hashid_input = QLineEdit()
        self.hashid_input.setPlaceholderText("Enter hash to identify")
        self.hashid_btn = self.create_primary_button("Identify with hashid")
        self.hashid_btn.clicked.connect(self.build_hashid)

        layout.addWidget(QLabel("Hash"))
        layout.addWidget(self.hashid_input)
        layout.addWidget(self.hashid_btn)
        layout.addStretch()
        return panel

    def build_hashid(self):
        hash_val = self.hashid_input.text().strip()
        if not hash_val:
            self.emit_validation_error("Hash value is required before running.")
            return
        self.run_command.emit(f"hashid {hash_val}")

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

    def build_sslscan(self):
        target = self.sslscan_target_input.text().strip()
        if not target:
            self.emit_validation_error("Target host is required before running.")
            return
        self.run_command.emit(f"sslscan {target}")

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

    def build_sslyze(self):
        target = self.sslyze_target_input.text().strip()
        if not target:
            self.emit_validation_error("Target host is required before running.")
            return
        self.run_command.emit(f"sslyze {target}")

<<<<<<< HEAD
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

    def build_wfuzz(self):
        url = self.wfuzz_url_input.text().strip()
        if not url:
            self.emit_validation_error("Wfuzz URL is required before running.")
            return
        # Example default command; users can edit the command in the UI later if needed.
        cmd = f"wfuzz -c -z file,/usr/share/wfuzz/wordlist/general/common.txt --hc 404 {url}"
        self.run_command.emit(cmd)
=======
>>>>>>> a5e05a07bb31dd605e12183ba96bffe5e9755c50

    def _create_tlssled_panel(self):
        panel, layout = self.create_panel("🔐 TLSSLed")
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

    def build_tlssled(self):
        host = self.tlssled_host_input.text().strip()
        port = self.tlssled_port_input.text().strip()
        if not host or not port:
            self.emit_validation_error("Host and port are required before running.")
            return
        self.run_command.emit(f"tlssled {host} {port}")
