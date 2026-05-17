from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton,
    QComboBox, QGroupBox, QFileDialog
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from ui.tool_icon_button import ToolIconButton


class AuthPage(QWidget):

    run_command = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        # ========================
        # TITLE
        # ========================
        title = QLabel("🔐 Authentication Testing")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: #f39c12; padding: 10px;")
        main_layout.addWidget(title)

        # ========================
        # TOOLS GRID
        # ========================
        tools_layout = QHBoxLayout()
        tools_layout.setSpacing(20)

        # HYDRA Icon Button
        self.hydra_icon = ToolIconButton("⚡", "Hydra", "Brute Force")
        self.hydra_icon.clicked.connect(self.show_hydra_panel)
        tools_layout.addWidget(self.hydra_icon)

        # JOHN Icon Button
        self.john_icon = ToolIconButton("🔨", "John", "Hash Cracking")
        self.john_icon.clicked.connect(self.show_john_panel)
        tools_layout.addWidget(self.john_icon)

        tools_layout.addStretch()
        main_layout.addLayout(tools_layout)

        # ========================
        # HYDRA INPUT PANEL
        # ========================

        hydra_group = QGroupBox("⚡ Hydra Brute Force")
        hydra_layout = QVBoxLayout()

        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("Enter Target IP")
        self.target_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #f39c12;
                border-radius: 5px;
                background-color: #2c3e50;
                color: white;
            }
        """)

        self.service_dropdown = QComboBox()
        self.service_dropdown.addItems([
            "ssh",
            "ftp",
            "http-get",
            "http-post-form"
        ])
        self.service_dropdown.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #f39c12;
                border-radius: 5px;
                background-color: #2c3e50;
                color: white;
            }
        """)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #f39c12;
                border-radius: 5px;
                background-color: #2c3e50;
                color: white;
            }
        """)

        self.password_file = QLineEdit()
        self.password_file.setPlaceholderText("Select Password Wordlist")
        self.password_file.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #f39c12;
                border-radius: 5px;
                background-color: #2c3e50;
                color: white;
            }
        """)

        self.browse_btn = QPushButton("📁 Browse Wordlist")
        self.browse_btn.setStyleSheet("""
            QPushButton {
                padding: 8px;
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        self.browse_btn.clicked.connect(self.select_wordlist)

        self.hydra_btn = QPushButton("▶️ Run Hydra")
        self.hydra_btn.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background-color: #f39c12;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d68910;
            }
        """)
        self.hydra_btn.clicked.connect(self.build_hydra)

        hydra_layout.addWidget(QLabel("Target IP:"))
        hydra_layout.addWidget(self.target_input)
        hydra_layout.addWidget(QLabel("Service:"))
        hydra_layout.addWidget(self.service_dropdown)
        hydra_layout.addWidget(QLabel("Username:"))
        hydra_layout.addWidget(self.username_input)
        hydra_layout.addWidget(QLabel("Password Wordlist:"))
        hydra_layout.addWidget(self.password_file)
        hydra_layout.addWidget(self.browse_btn)
        hydra_layout.addWidget(self.hydra_btn)
        hydra_layout.addStretch()

        hydra_group.setLayout(hydra_layout)
        hydra_group.setStyleSheet("""
            QGroupBox {
                color: white;
                border: 2px solid #f39c12;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
        """)

        # ========================
        # JOHN INPUT PANEL
        # ========================

        john_group = QGroupBox("🔨 John the Ripper - Hash Cracking")
        john_layout = QVBoxLayout()

        self.hash_file = QLineEdit()
        self.hash_file.setPlaceholderText("Select Hash File")
        self.hash_file.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #f39c12;
                border-radius: 5px;
                background-color: #2c3e50;
                color: white;
            }
        """)

        self.browse_hash_btn = QPushButton("📁 Browse Hash File")
        self.browse_hash_btn.setStyleSheet("""
            QPushButton {
                padding: 8px;
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        self.browse_hash_btn.clicked.connect(self.select_hash_file)

        self.john_wordlist = QLineEdit()
        self.john_wordlist.setPlaceholderText("Select Wordlist")
        self.john_wordlist.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #f39c12;
                border-radius: 5px;
                background-color: #2c3e50;
                color: white;
            }
        """)

        self.browse_john_wordlist = QPushButton("📁 Browse Wordlist")
        self.browse_john_wordlist.setStyleSheet("""
            QPushButton {
                padding: 8px;
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        self.browse_john_wordlist.clicked.connect(self.select_john_wordlist)

        self.john_btn = QPushButton("▶️ Run John")
        self.john_btn.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background-color: #f39c12;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d68910;
            }
        """)
        self.john_btn.clicked.connect(self.build_john)

        john_layout.addWidget(QLabel("Hash File:"))
        john_layout.addWidget(self.hash_file)
        john_layout.addWidget(self.browse_hash_btn)
        john_layout.addWidget(QLabel("Wordlist:"))
        john_layout.addWidget(self.john_wordlist)
        john_layout.addWidget(self.browse_john_wordlist)
        john_layout.addWidget(self.john_btn)
        john_layout.addStretch()

        john_group.setLayout(john_layout)
        john_group.setStyleSheet("""
            QGroupBox {
                color: white;
                border: 2px solid #f39c12;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
        """)

        main_layout.addWidget(hydra_group)
        main_layout.addWidget(john_group)
        main_layout.addStretch()

        self.setLayout(main_layout)

        # Apply label styling
        self.setStyleSheet("QLabel { color: white; }")

    # ========================
    # PANEL DISPLAY METHODS
    # ========================

    def show_hydra_panel(self):
        """Focus on Hydra target input when icon clicked"""
        self.target_input.setFocus()
        self.target_input.selectAll()

    def show_john_panel(self):
        """Focus on John hash file input when icon clicked"""
        self.hash_file.setFocus()
        self.hash_file.selectAll()

    # ========================
    # FILE SELECTORS
    # ========================

    def select_wordlist(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Wordlist", "", "Text Files (*.txt)"
        )
        if file_path:
            self.password_file.setText(file_path)

    def select_hash_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Hash File", "", "Text Files (*.txt)"
        )
        if file_path:
            self.hash_file.setText(file_path)

    def select_john_wordlist(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Wordlist", "", "Text Files (*.txt)"
        )
        if file_path:
            self.john_wordlist.setText(file_path)

    # ========================
    # HYDRA COMMAND
    # ========================

    def build_hydra(self):
        target = self.target_input.text().strip()
        service = self.service_dropdown.currentText()
        username = self.username_input.text().strip()
        wordlist = self.password_file.text().strip()

        if not target or not username or not wordlist:
            return

        command = f"hydra -l {username} -P {wordlist} {target} {service}"

        self.run_command.emit(command)

    # ========================
    # JOHN COMMAND
    # ========================

    def build_john(self):
        hash_file = self.hash_file.text().strip()
        wordlist = self.john_wordlist.text().strip()

        if not hash_file:
            return

        command = f"john {hash_file}"

        if wordlist:
            command += f" --wordlist={wordlist}"

        self.run_command.emit(command)