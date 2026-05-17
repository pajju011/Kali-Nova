from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton,
    QComboBox, QGroupBox, QFileDialog
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from core.app_state import app_state
from ui.tool_icon_button import ToolIconButton


class WebPage(QWidget):

    run_command = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        # ========================
        # TITLE
        # ========================
        title = QLabel("🌐 Web Testing Tools")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: #e74c3c; padding: 10px;")
        main_layout.addWidget(title)

        # ========================
        # TOOLS GRID
        # ========================
        tools_layout = QHBoxLayout()
        tools_layout.setSpacing(20)

        # NIKTO Icon Button
        self.nikto_icon = ToolIconButton("🔍", "Nikto", "Web Scanning")
        self.nikto_icon.clicked.connect(self.show_nikto_panel)
        tools_layout.addWidget(self.nikto_icon)

        # SQLMAP Icon Button
        self.sqlmap_icon = ToolIconButton("💉", "SQLmap", "SQL Injection")
        self.sqlmap_icon.clicked.connect(self.show_sqlmap_panel)
        tools_layout.addWidget(self.sqlmap_icon)

        # GOBUSTER Icon Button
        self.gobuster_icon = ToolIconButton("🔓", "Gobuster", "Directory Brute Force")
        self.gobuster_icon.clicked.connect(self.show_gobuster_panel)
        tools_layout.addWidget(self.gobuster_icon)

        tools_layout.addStretch()
        main_layout.addLayout(tools_layout)

        # ========================
        # NIKTO INPUT PANEL
        # ========================

        nikto_group = QGroupBox("🔍 Nikto Web Scanner")
        nikto_layout = QVBoxLayout()

        self.nikto_url = QLineEdit()
        self.nikto_url.setPlaceholderText("Enter Target URL (http://example.com)")
        self.nikto_url.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #e74c3c;
                border-radius: 5px;
                background-color: #2c3e50;
                color: white;
            }
        """)

        self.ssl_option = QComboBox()
        self.ssl_option.addItems(["Auto Detect", "Force SSL"])
        self.ssl_option.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #e74c3c;
                border-radius: 5px;
                background-color: #2c3e50;
                color: white;
            }
        """)

        self.nikto_btn = QPushButton("▶️ Run Nikto")
        self.nikto_btn.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.nikto_btn.clicked.connect(self.build_nikto)

        nikto_layout.addWidget(QLabel("Target URL:"))
        nikto_layout.addWidget(self.nikto_url)
        nikto_layout.addWidget(QLabel("SSL Option:"))
        nikto_layout.addWidget(self.ssl_option)
        nikto_layout.addWidget(self.nikto_btn)
        nikto_layout.addStretch()

        nikto_group.setLayout(nikto_layout)
        nikto_group.setStyleSheet("""
            QGroupBox {
                color: white;
                border: 2px solid #e74c3c;
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
        # SQLMAP INPUT PANEL
        # ========================

        sqlmap_group = QGroupBox("💉 SQLmap Injection Testing")
        sqlmap_layout = QVBoxLayout()

        self.sqlmap_url = QLineEdit()
        self.sqlmap_url.setPlaceholderText(
            "Enter URL with parameter (http://site.com/page?id=1)"
        )
        self.sqlmap_url.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #e74c3c;
                border-radius: 5px;
                background-color: #2c3e50;
                color: white;
            }
        """)

        self.sqlmap_level = QComboBox()
        self.sqlmap_level.addItems([
            "Level 1 (Basic)",
            "Level 3 (Medium)",
            "Level 5 (Aggressive)"
        ])
        self.sqlmap_level.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #e74c3c;
                border-radius: 5px;
                background-color: #2c3e50;
                color: white;
            }
        """)

        self.sqlmap_btn = QPushButton("▶️ Run SQLmap")
        self.sqlmap_btn.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.sqlmap_btn.clicked.connect(self.build_sqlmap)

        sqlmap_layout.addWidget(QLabel("Target URL:"))
        sqlmap_layout.addWidget(self.sqlmap_url)
        sqlmap_layout.addWidget(QLabel("Detection Level:"))
        sqlmap_layout.addWidget(self.sqlmap_level)
        sqlmap_layout.addWidget(self.sqlmap_btn)
        sqlmap_layout.addStretch()

        sqlmap_group.setLayout(sqlmap_layout)
        sqlmap_group.setStyleSheet("""
            QGroupBox {
                color: white;
                border: 2px solid #e74c3c;
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
        # GOBUSTER INPUT PANEL
        # ========================

        gobuster_group = QGroupBox("🔓 Gobuster Directory Brute Force")
        gobuster_layout = QVBoxLayout()

        self.gobuster_url = QLineEdit()
        self.gobuster_url.setPlaceholderText("Enter Target URL (http://example.com)")
        self.gobuster_url.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #e74c3c;
                border-radius: 5px;
                background-color: #2c3e50;
                color: white;
            }
        """)

        self.wordlist_path = QLineEdit()
        self.wordlist_path.setPlaceholderText("Select Wordlist File")
        self.wordlist_path.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #e74c3c;
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

        self.gobuster_btn = QPushButton("▶️ Run Gobuster")
        self.gobuster_btn.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.gobuster_btn.clicked.connect(self.build_gobuster)

        gobuster_layout.addWidget(QLabel("Target URL:"))
        gobuster_layout.addWidget(self.gobuster_url)
        gobuster_layout.addWidget(QLabel("Wordlist:"))
        gobuster_layout.addWidget(self.wordlist_path)
        gobuster_layout.addWidget(self.browse_btn)
        gobuster_layout.addWidget(self.gobuster_btn)
        gobuster_layout.addStretch()

        gobuster_group.setLayout(gobuster_layout)
        gobuster_group.setStyleSheet("""
            QGroupBox {
                color: white;
                border: 2px solid #e74c3c;
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


        main_layout.addWidget(nikto_group)
        main_layout.addWidget(sqlmap_group)
        main_layout.addWidget(gobuster_group)
        main_layout.addStretch()

        self.setLayout(main_layout)

        # Apply label styling
        self.setStyleSheet("QLabel { color: white; }")

    # ========================
    # PANEL DISPLAY METHODS
    # ========================

    def show_nikto_panel(self):
        """Focus on Nikto URL input when icon clicked"""
        self.nikto_url.setFocus()
        self.nikto_url.selectAll()

    def show_sqlmap_panel(self):
        """Focus on SQLmap URL input when icon clicked"""
        self.sqlmap_url.setFocus()
        self.sqlmap_url.selectAll()

    def show_gobuster_panel(self):
        """Focus on Gobuster URL input when icon clicked"""
        self.gobuster_url.setFocus()
        self.gobuster_url.selectAll()

    # ========================
    # NIKTO COMMAND
    # ========================
    def build_nikto(self):
        url = self.nikto_url.text().strip()
        if not url:
            return

        command = f"nikto -h {url}"

        if self.ssl_option.currentText() == "Force SSL":
            command += " -ssl"

        self.run_command.emit(command)

    # ========================
    # SQLMAP COMMAND
    # ========================
    def build_sqlmap(self):
        url = self.sqlmap_url.text().strip()
        if not url:
            return

        command = f"sqlmap -u \"{url}\""

        # Beginner Mode forces safe behavior
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

    # ========================
    # GOBUSTER COMMAND
    # ========================
    def build_gobuster(self):
        url = self.gobuster_url.text().strip()
        wordlist = self.wordlist_path.text().strip()

        if not url or not wordlist:
            return

        command = f"gobuster dir -u {url} -w {wordlist}"

        self.run_command.emit(command)

    def select_wordlist(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Wordlist",
            "",
            "Text Files (*.txt)"
        )

        if file_path:
            self.wordlist_path.setText(file_path)