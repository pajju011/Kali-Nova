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
        self.hash_identifier_panel = self._create_hash_identifier_panel()
        self.hashid_panel = self._create_hashid_panel()
        self.wordlists_panel = self._create_wordlists_panel()

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
            tool_id="wordlists",
            icon="📚",
            name="Wordlists",
            description="Wordlist Manager",
            panel=self.wordlists_panel,
            focus_widget=self.wordlist_action_combo,
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

    def _create_wordlists_panel(self):
        panel, layout = self.create_panel("📚 Wordlists Manager & Helper")

        self.wordlist_action_combo = QComboBox()
        self.wordlist_action_combo.addItems([
            "List System Wordlists",
            "Decompress RockYou (.gz)",
            "Wordlist Info / Line Count",
            "Find All Wordlist Files",
            "Install Wordlists Package",
        ])

        self.wordlist_target_path = QLineEdit()
        self.wordlist_target_path.setText("/usr/share/wordlists/rockyou.txt")
        self.wordlist_target_path.setPlaceholderText("Enter file or directory path")

        self.wordlist_browse_btn = self.create_secondary_button("Browse Wordlist File")
        self.wordlist_browse_btn.clicked.connect(self.select_wordlist_target)

        self.wordlists_btn = self.create_primary_button("Execute Action")
        self.wordlists_btn.clicked.connect(self.build_wordlists)

        layout.addWidget(QLabel("Action"))
        layout.addWidget(self.wordlist_action_combo)
        layout.addWidget(QLabel("Target Wordlist File / Directory"))
        layout.addWidget(self.wordlist_target_path)
        layout.addWidget(self.wordlist_browse_btn)
        layout.addWidget(self.wordlists_btn)
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

    def show_wordlists_panel(self):
        self.activate_tool("wordlists")

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

    def select_wordlist_target(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Wordlist File",
            "/usr/share/wordlists",
            "All Files (*)",
        )
        if file_path:
            self.wordlist_target_path.setText(file_path)

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

    def build_wordlists(self):
        action = self.wordlist_action_combo.currentText()
        target_path = self.wordlist_target_path.text().strip()

        if action == "List System Wordlists":
            path = target_path if target_path else "/usr/share/wordlists/"
            self.run_command.emit(f"ls -lh \"{path}\"")
        elif action == "Decompress RockYou (.gz)":
            gz_path = target_path if target_path else "/usr/share/wordlists/rockyou.txt.gz"
            if not gz_path.endswith(".gz"):
                gz_path = "/usr/share/wordlists/rockyou.txt.gz"
            self.run_command.emit(f"gunzip -k \"{gz_path}\"")
        elif action == "Wordlist Info / Line Count":
            if not target_path:
                self.emit_validation_error("Target wordlist path is required for line counting.")
                return
            self.run_command.emit(f"wc -l \"{target_path}\"")
        elif action == "Find All Wordlist Files":
            search_path = target_path if target_path else "/usr/share/wordlists"
            self.run_command.emit(f"find \"{search_path}\" -type f")
        elif action == "Install Wordlists Package":
            self.run_command.emit("sudo apt update && sudo apt install -y wordlists")
