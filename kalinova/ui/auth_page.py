# pyrefly: ignore [missing-import]
from PyQt6.QtWidgets import QLabel, QLineEdit, QComboBox, QFileDialog
# pyrefly: ignore [missing-import]
from PyQt6.QtCore import pyqtSignal

from ui.tool_template import ToolModulePage
from ui.icon_manager import get_tool_icon_path


class AuthPage(ToolModulePage):

    run_command = pyqtSignal(str)

    def __init__(self):
        super().__init__(
            title="Authentication Testing",
            accent_color="#f59e0b",
            subtitle="Choose a credential testing tool and the required fields will appear.",
        )

        self.hydra_panel = self._create_hydra_panel()
        self.ncrack_panel = self._create_ncrack_panel()
        self.john_panel = self._create_john_panel()
        self.hashcat_panel = self._create_hashcat_panel()
        self.hash_identifier_panel = self._create_hash_identifier_panel()
        self.hashid_panel = self._create_hashid_panel()

        self.add_tool(
            tool_id="hydra",
            icon=get_tool_icon_path("hydra"),
            name="Hydra",
            description="Brute Force",
            panel=self.hydra_panel,
            focus_widget=self.hydra_target_input,
        )
        self.add_tool(
            tool_id="ncrack",
            icon=get_tool_icon_path("ncrack"),
            name="Ncrack",
            description="Network Auth Cracker",
            panel=self.ncrack_panel,
            focus_widget=self.ncrack_target_input,
        )
        self.add_tool(
            tool_id="john",
            icon=get_tool_icon_path("john"),
            name="John",
            description="Hash Cracking",
            panel=self.john_panel,
            focus_widget=self.hash_file,
        )
        self.add_tool(
            tool_id="hashcat",
            icon=get_tool_icon_path("hashcat"),
            name="Hashcat",
            description="GPU/CPU Hash Recovery",
            panel=self.hashcat_panel,
            focus_widget=self.hashcat_file_input,
        )
        self.add_tool(
            tool_id="hash_identifier",
            icon=get_tool_icon_path("hashcat"),
            name="Hash Identifier",
            description="Identify hash types",
            panel=self.hash_identifier_panel,
            focus_widget=self.hash_input,
        )
        self.add_tool(
            tool_id="hashid",
            icon=get_tool_icon_path("hashid"),
            name="HashID",
            description="Identify hash types (hashid)",
            panel=self.hashid_panel,
            focus_widget=self.hashid_input,
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

    def _create_hashcat_panel(self):
        panel, layout = self.create_panel("⚡ Hashcat Password Recovery Engine")

        from PyQt6.QtWidgets import QCheckBox, QHBoxLayout
        from ui.components.tool_helper_widget import ToolHelperWidget

        self.hashcat_file_input = QLineEdit()
        self.hashcat_file_input.setPlaceholderText("Select hash file or enter hash (e.g., example500.hash)")

        self.hashcat_helper = ToolHelperWidget("hashcat")
        self.hashcat_file_input.textChanged.connect(self.hashcat_helper.validate_text)

        self.browse_hashcat_hash_btn = self.create_secondary_button("Browse Hash File")
        self.browse_hashcat_hash_btn.clicked.connect(self._browse_hashcat_file)

        self.hashcat_mode_combo = QComboBox()
        self.hashcat_mode_combo.addItems([
            "0 - MD5",
            "100 - SHA1",
            "500 - md5crypt, MD5(Unix), Cisco-IOS $1$",
            "1000 - NTLM",
            "1400 - SHA2-256",
            "1800 - sha512crypt, SHA512(Unix)",
            "2500 - WPA/WPA2",
            "3200 - bcrypt",
            "13000 - RAR5",
            "17000 - SHA3-256"
        ])

        self.hashcat_attack_combo = QComboBox()
        self.hashcat_attack_combo.addItems([
            "0 - Straight (Wordlist)",
            "1 - Combination",
            "3 - Brute-force / Mask",
            "6 - Hybrid Wordlist + Mask",
            "7 - Hybrid Mask + Wordlist"
        ])

        self.hashcat_wordlist_input = QLineEdit()
        self.hashcat_wordlist_input.setPlaceholderText("Select wordlist file (e.g. /usr/share/wordlists/sqlmap.txt)")

        self.browse_hashcat_wordlist_btn = self.create_secondary_button("Browse Wordlist")
        self.browse_hashcat_wordlist_btn.clicked.connect(self._browse_hashcat_wordlist)

        self.hashcat_outfile_input = QLineEdit()
        self.hashcat_outfile_input.setPlaceholderText("Output file for recovered hashes (-o) (optional)")

        self.chk_hashcat_benchmark = QCheckBox("Run Benchmark Speed Test (-b)")
        self.chk_hashcat_optimized = QCheckBox("Enable Optimized Kernels (-O)")
        self.chk_hashcat_optimized.setChecked(True)
        self.chk_hashcat_force = QCheckBox("Ignore Warnings (--force)")

        self.hashcat_btn = self.create_primary_button("Run Hashcat")
        self.hashcat_btn.clicked.connect(self.build_hashcat)

        layout.addWidget(QLabel("Hash File / Hash Target"))
        layout.addWidget(self.hashcat_file_input)
        layout.addWidget(self.hashcat_helper)
        layout.addWidget(self.browse_hashcat_hash_btn)
        layout.addWidget(QLabel("Hash Type (-m)"))
        layout.addWidget(self.hashcat_mode_combo)
        layout.addWidget(QLabel("Attack Mode (-a)"))
        layout.addWidget(self.hashcat_attack_combo)
        layout.addWidget(QLabel("Wordlist File"))
        layout.addWidget(self.hashcat_wordlist_input)
        layout.addWidget(self.browse_hashcat_wordlist_btn)
        layout.addWidget(QLabel("Output File (-o)"))
        layout.addWidget(self.hashcat_outfile_input)
        layout.addWidget(QLabel("Performance & Options"))
        layout.addWidget(self.chk_hashcat_benchmark)
        layout.addWidget(self.chk_hashcat_optimized)
        layout.addWidget(self.chk_hashcat_force)
        layout.addWidget(self.hashcat_btn)
        layout.addStretch()

        return panel

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

    def _create_ncrack_panel(self):
        panel, layout = self.create_panel("⚡ Ncrack Network Authentication Cracker")

        from PyQt6.QtWidgets import QCheckBox
        from ui.components.tool_helper_widget import ToolHelperWidget

        # Target Specification (Single Target vs Target List File -iL)
        self.ncrack_target_input = QLineEdit()
        self.ncrack_target_input.setPlaceholderText("Enter target IP / Hostname (e.g. 192.168.1.100)")

        self.ncrack_helper = ToolHelperWidget("ncrack")
        self.ncrack_target_input.textChanged.connect(self.ncrack_helper.validate_text)

        self.ncrack_target_file_input = QLineEdit()
        self.ncrack_target_file_input.setPlaceholderText("Select target list file (-iL win.txt)")

        self.browse_ncrack_targets_btn = self.create_secondary_button("Browse Target File (-iL)")
        self.browse_ncrack_targets_btn.clicked.connect(self._browse_ncrack_target_file)

        # Service / Protocol Selection
        self.ncrack_service_combo = QComboBox()
        self.ncrack_service_combo.addItems([
            "rdp",
            "ssh",
            "ftp",
            "smb",
            "vnc",
            "http",
            "https",
            "telnet",
            "pop3",
            "pop3s",
            "sip",
            "redis",
            "mongodb",
            "winrm"
        ])

        self.ncrack_custom_port_input = QLineEdit()
        self.ncrack_custom_port_input.setPlaceholderText("Custom service port (optional, e.g. 3389, 2222)")

        # Authentication Specification (Username & Wordlist)
        self.ncrack_user_input = QLineEdit()
        self.ncrack_user_input.setPlaceholderText("Single username (--user victim)")

        self.ncrack_user_file_input = QLineEdit()
        self.ncrack_user_file_input.setPlaceholderText("Username wordlist file (-U users.txt) (optional)")

        self.browse_ncrack_users_btn = self.create_secondary_button("Browse User List (-U)")
        self.browse_ncrack_users_btn.clicked.connect(self._browse_ncrack_user_file)

        self.ncrack_pass_input = QLineEdit()
        self.ncrack_pass_input.setPlaceholderText("Single password (--pass password123) (optional)")

        self.ncrack_pass_file_input = QLineEdit()
        self.ncrack_pass_file_input.setPlaceholderText("Password dictionary wordlist (-P passes.txt)")

        self.browse_ncrack_pass_btn = self.create_secondary_button("Browse Pass List (-P)")
        self.browse_ncrack_pass_btn.clicked.connect(self._browse_ncrack_pass_file)

        # Timing & Concurrency Limit
        self.ncrack_timing_combo = QComboBox()
        self.ncrack_timing_combo.addItems([
            "None (Default)",
            "-T0 - Paranoid",
            "-T1 - Sneaky",
            "-T2 - Polite",
            "-T3 - Normal",
            "-T4 - Aggressive",
            "-T5 - Insane"
        ])

        self.ncrack_cl_input = QLineEdit()
        self.ncrack_cl_input.setPlaceholderText("Max connection limit (e.g. CL=1 or CL=10)")

        # Flags & Checkboxes
        self.chk_ncrack_verbose = QCheckBox("Verbose mode (-v)")
        self.chk_ncrack_verbose.setChecked(True)
        self.chk_ncrack_extra_verbose = QCheckBox("Extra verbose mode (-vv)")
        self.chk_ncrack_stealthy = QCheckBox("Stealthy Linear mode (--stealthy-linear)")
        self.chk_ncrack_ssl = QCheckBox("Enable SSL (ssl)")

        self.ncrack_btn = self.create_primary_button("Run Ncrack")
        self.ncrack_btn.clicked.connect(self.build_ncrack)

        layout.addWidget(QLabel("Target IP / Hostname (or Target List File)"))
        layout.addWidget(self.ncrack_target_input)
        layout.addWidget(self.ncrack_helper)
        layout.addWidget(self.ncrack_target_file_input)
        layout.addWidget(self.browse_ncrack_targets_btn)
        layout.addWidget(QLabel("Service Protocol (-p)"))
        layout.addWidget(self.ncrack_service_combo)
        layout.addWidget(QLabel("Custom Service Port (Optional)"))
        layout.addWidget(self.ncrack_custom_port_input)
        layout.addWidget(QLabel("Username Credentials (--user or -U)"))
        layout.addWidget(self.ncrack_user_input)
        layout.addWidget(self.ncrack_user_file_input)
        layout.addWidget(self.browse_ncrack_users_btn)
        layout.addWidget(QLabel("Password Credentials (--pass or -P)"))
        layout.addWidget(self.ncrack_pass_input)
        layout.addWidget(self.ncrack_pass_file_input)
        layout.addWidget(self.browse_ncrack_pass_btn)
        layout.addWidget(QLabel("Performance & Concurrency Limit"))
        layout.addWidget(self.ncrack_timing_combo)
        layout.addWidget(self.ncrack_cl_input)
        layout.addWidget(self.chk_ncrack_verbose)
        layout.addWidget(self.chk_ncrack_extra_verbose)
        layout.addWidget(self.chk_ncrack_stealthy)
        layout.addWidget(self.chk_ncrack_ssl)
        layout.addWidget(self.ncrack_btn)
        layout.addStretch()

        return panel

    def show_hydra_panel(self):
        self.activate_tool("hydra")

    def show_ncrack_panel(self):
        self.activate_tool("ncrack")

    def show_john_panel(self):
        self.activate_tool("john")

    def show_hashcat_panel(self):
        self.activate_tool("hashcat")

    def show_hash_identifier_panel(self):
        self.activate_tool("hash_identifier")

    def show_hashid_panel(self):
        self.activate_tool("hashid")

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

    def build_hash_identifier(self):
        hash_val = self.hash_input.text().strip()
        if not hash_val:
            self.emit_validation_error("Hash value is required before running.")
            return
        self.run_command.emit(f"hash-identifier {hash_val}")

    def build_hashid(self):
        hash_val = self.hashid_input.text().strip()
        if not hash_val:
            self.emit_validation_error("Hash value is required before running.")
            return
        self.run_command.emit(f"hashid {hash_val}")

    def _browse_hashcat_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Hash File",
            "",
            "All Files (*.*)",
        )
        if file_path:
            self.hashcat_file_input.setText(file_path)

    def _browse_hashcat_wordlist(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Wordlist",
            "",
            "All Files (*.*)",
        )
        if file_path:
            self.hashcat_wordlist_input.setText(file_path)

    def build_hashcat(self):
        if self.chk_hashcat_benchmark.isChecked():
            cmd = ["hashcat", "-b"]
            if self.chk_hashcat_force.isChecked():
                cmd.append("--force")
            self.run_command.emit(" ".join(cmd))
            return

        hash_file = self.hashcat_file_input.text().strip()
        if not hash_file:
            self.emit_validation_error("Hash file or target hash is required before running Hashcat.")
            return

        mode_text = self.hashcat_mode_combo.currentText().split(" - ")[0]
        attack_text = self.hashcat_attack_combo.currentText().split(" - ")[0]

        cmd = ["hashcat", "-m", mode_text, "-a", attack_text, f"\"{hash_file}\""]

        wordlist = self.hashcat_wordlist_input.text().strip()
        if wordlist:
            cmd.append(f"\"{wordlist}\"")

        outfile = self.hashcat_outfile_input.text().strip()
        if outfile:
            cmd.extend(["-o", f"\"{outfile}\""])

        if self.chk_hashcat_optimized.isChecked():
            cmd.append("-O")

        if self.chk_hashcat_force.isChecked():
            cmd.append("--force")

        self.run_command.emit(" ".join(cmd))

    def _browse_ncrack_target_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Target List File (-iL)",
            "",
            "Text/List Files (*.txt *.list *.ip);;All Files (*.*)",
        )
        if file_path:
            self.ncrack_target_file_input.setText(file_path)

    def _browse_ncrack_user_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Username Wordlist (-U)",
            "",
            "Text/Wordlist Files (*.txt *.lst *.dict);;All Files (*.*)",
        )
        if file_path:
            self.ncrack_user_file_input.setText(file_path)

    def _browse_ncrack_pass_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Password Wordlist (-P)",
            "",
            "Text/Wordlist Files (*.txt *.lst *.dict);;All Files (*.*)",
        )
        if file_path:
            self.ncrack_pass_file_input.setText(file_path)

    def build_ncrack(self):
        target_host = self.ncrack_target_input.text().strip()
        target_file = self.ncrack_target_file_input.text().strip()

        if not target_host and not target_file:
            self.emit_validation_error("Target IP/Host or Target File (-iL) is required before running Ncrack.")
            return

        user = self.ncrack_user_input.text().strip()
        user_file = self.ncrack_user_file_input.text().strip()
        if not user and not user_file:
            self.emit_validation_error("Username (--user) or User list file (-U) is required before running Ncrack.")
            return

        pwd = self.ncrack_pass_input.text().strip()
        pwd_file = self.ncrack_pass_file_input.text().strip()
        if not pwd and not pwd_file:
            self.emit_validation_error("Password (--pass) or Password wordlist (-P) is required before running Ncrack.")
            return

        cmd = ["ncrack"]

        if self.chk_ncrack_extra_verbose.isChecked():
            cmd.append("-vv")
        elif self.chk_ncrack_verbose.isChecked():
            cmd.append("-v")

        if target_file:
            cmd.extend(["-iL", target_file])

        if user_file:
            cmd.extend(["-U", user_file])
        elif user:
            cmd.extend(["--user", user])

        if pwd_file:
            cmd.extend(["-P", pwd_file])
        elif pwd:
            cmd.extend(["--pass", pwd])

        # Service / Port
        service = self.ncrack_service_combo.currentText().strip()
        port = self.ncrack_custom_port_input.text().strip()
        if port:
            service_spec = f"{service}:{port}"
        else:
            service_spec = service

        if self.chk_ncrack_ssl.isChecked() and not service_spec.endswith(",ssl"):
            service_spec = f"{service_spec},ssl"

        cmd.extend(["-p", service_spec])

        # Connection Limit CL= or cl=
        cl_val = self.ncrack_cl_input.text().strip()
        if cl_val:
            if not cl_val.startswith("CL=") and not cl_val.startswith("cl="):
                cl_val = f"CL={cl_val}"
            cmd.append(cl_val)

        # Timing template
        timing_idx = self.ncrack_timing_combo.currentIndex()
        if timing_idx > 0:
            template_flag = f"-T{timing_idx - 1}"
            cmd.append(template_flag)

        if self.chk_ncrack_stealthy.isChecked():
            cmd.append("--stealthy-linear")

        if target_host and not target_file:
            cmd.append(target_host)

        self.run_command.emit(" ".join(cmd))

