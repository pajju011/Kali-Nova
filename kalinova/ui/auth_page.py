# pyrefly: ignore [missing-import]
from PyQt6.QtWidgets import QLabel, QLineEdit, QComboBox, QFileDialog
# pyrefly: ignore [missing-import]
from PyQt6.QtCore import pyqtSignal

from ui.tool_template import ToolModulePage


class AuthPage(ToolModulePage):

    run_command = pyqtSignal(str)

    def __init__(self):
        super().__init__(
            title="Authentication Testing",
            accent_color="#f59e0b",
            subtitle="Choose a credential testing tool and the required fields will appear.",
        )

        self.hydra_panel = self._create_hydra_panel()
        self.john_panel = self._create_john_panel()
        self.ncrack_panel = self._create_ncrack_panel()
        self.hash_identifier_panel = self._create_hash_identifier_panel()
        self.hashid_panel = self._create_hashid_panel()

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
            tool_id="ncrack",
            icon="🔓",
            name="Ncrack",
            description="Network Auth Cracker",
            panel=self.ncrack_panel,
            focus_widget=self.ncrack_target_input,
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
        panel, layout = self.create_panel("🔓 Ncrack Network Auth Cracker")

        self.ncrack_target_input = QLineEdit()
        self.ncrack_target_input.setPlaceholderText("Target IP / Host (e.g. 192.168.1.200)")

        self.ncrack_service_combo = QComboBox()
        self.ncrack_service_combo.addItems([
            "rdp",
            "ssh",
            "ftp",
            "smb",
            "http",
            "vnc",
            "telnet",
            "pop3",
        ])

        self.ncrack_user_input = QLineEdit()
        self.ncrack_user_input.setPlaceholderText("Username (e.g. victim)")

        self.ncrack_pass_file = QLineEdit()
        self.ncrack_pass_file.setPlaceholderText("Select password dictionary (-P)")

        self.browse_ncrack_pass_btn = self.create_secondary_button("Browse Passwords")
        self.browse_ncrack_pass_btn.clicked.connect(self.select_ncrack_pass_file)

        self.ncrack_cl_input = QLineEdit()
        self.ncrack_cl_input.setPlaceholderText("Max Connection Limit (e.g. 1)")
        self.ncrack_cl_input.setText("1")

        self.ncrack_btn = self.create_primary_button("Run Ncrack")
        self.ncrack_btn.clicked.connect(self.build_ncrack)

        layout.addWidget(QLabel("Target Host / IP"))
        layout.addWidget(self.ncrack_target_input)
        layout.addWidget(QLabel("Protocol / Service (-p)"))
        layout.addWidget(self.ncrack_service_combo)
        layout.addWidget(QLabel("Username (--user)"))
        layout.addWidget(self.ncrack_user_input)
        layout.addWidget(QLabel("Password Dictionary (-P)"))
        layout.addWidget(self.ncrack_pass_file)
        layout.addWidget(self.browse_ncrack_pass_btn)
        layout.addWidget(QLabel("Max Connection Limit (CL=)"))
        layout.addWidget(self.ncrack_cl_input)
        layout.addWidget(self.ncrack_btn)
        layout.addStretch()

        return panel

    def show_hydra_panel(self):
        self.activate_tool("hydra")

    def show_john_panel(self):
        self.activate_tool("john")

    def show_ncrack_panel(self):
        self.activate_tool("ncrack")

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

    def select_ncrack_pass_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Password Dictionary",
            "",
            "Text Files (*.txt)",
        )
        if file_path:
            self.ncrack_pass_file.setText(file_path)

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

    def build_ncrack(self):
        target = self.ncrack_target_input.text().strip()
        service = self.ncrack_service_combo.currentText().strip()
        user = self.ncrack_user_input.text().strip()
        pass_file = self.ncrack_pass_file.text().strip()
        cl_limit = self.ncrack_cl_input.text().strip()

        if not target:
            self.emit_validation_error("Ncrack target IP / Host is required before running.")
            return

        if not user:
            self.emit_validation_error("Ncrack username is required before running.")
            return

        if not pass_file:
            self.emit_validation_error("Ncrack password dictionary is required before running.")
            return

        cmd = f"ncrack -v --user {user} -P \"{pass_file}\" -p {service}"
        if cl_limit:
            cmd += f" CL={cl_limit}"
        cmd += f" {target}"

        self.run_command.emit(cmd)

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
