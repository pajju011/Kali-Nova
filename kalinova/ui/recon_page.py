from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QComboBox, QGroupBox, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from core.app_state import app_state
from ui.tool_icon_button import ToolIconButton


class ReconPage(QWidget):

    run_command = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        # ========================
        # TITLE
        # ========================
        title = QLabel("🔍 Reconnaissance Tools")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: #3498db; padding: 10px;")
        main_layout.addWidget(title)

        # ========================
        # TOOLS GRID
        # ========================
        tools_layout = QHBoxLayout()
        tools_layout.setSpacing(20)

        # NMAP Icon Button
        self.nmap_icon = ToolIconButton("🎯", "Nmap", "Port Scanning")
        self.nmap_icon.clicked.connect(self.show_nmap_panel)
        tools_layout.addWidget(self.nmap_icon)

        # WHOIS Icon Button
        self.whois_icon = ToolIconButton("🌐", "Whois", "Domain Lookup")
        self.whois_icon.clicked.connect(self.show_whois_panel)
        tools_layout.addWidget(self.whois_icon)

        # HARVESTER Icon Button
        self.harvester_icon = ToolIconButton("🕵️", "Harvester", "OSINT")
        self.harvester_icon.clicked.connect(self.show_harvester_panel)
        tools_layout.addWidget(self.harvester_icon)

        tools_layout.addStretch()
        main_layout.addLayout(tools_layout)

        # ========================
        # NMAP INPUT PANEL
        # ========================

        nmap_group = QGroupBox("🎯 Nmap Configuration")
        nmap_layout = QVBoxLayout()

        self.nmap_target = QLineEdit()
        self.nmap_target.setPlaceholderText("Enter Target IP / Domain")
        self.nmap_target.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #3498db;
                border-radius: 5px;
                background-color: #2c3e50;
                color: white;
            }
        """)

        self.scan_type = QComboBox()
        self.scan_type.addItems([
            "Quick Scan",
            "Service Detection",
            "Aggressive Scan"
        ])
        self.scan_type.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #3498db;
                border-radius: 5px;
                background-color: #2c3e50;
                color: white;
            }
        """)

        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("Custom Port (optional)")
        self.port_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #3498db;
                border-radius: 5px;
                background-color: #2c3e50;
                color: white;
            }
        """)

        self.nmap_btn = QPushButton("▶️ Run Nmap")
        self.nmap_btn.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        self.nmap_btn.clicked.connect(self.build_nmap)

        nmap_layout.addWidget(QLabel("Target:"))
        nmap_layout.addWidget(self.nmap_target)
        nmap_layout.addWidget(QLabel("Scan Type:"))
        nmap_layout.addWidget(self.scan_type)
        nmap_layout.addWidget(QLabel("Custom Port:"))
        nmap_layout.addWidget(self.port_input)
        nmap_layout.addWidget(self.nmap_btn)
        nmap_layout.addStretch()

        nmap_group.setLayout(nmap_layout)
        nmap_group.setStyleSheet("""
            QGroupBox {
                color: white;
                border: 2px solid #3498db;
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
        # WHOIS INPUT PANEL
        # ========================

        whois_group = QGroupBox("🌐 Whois Lookup")
        whois_layout = QVBoxLayout()

        self.whois_target = QLineEdit()
        self.whois_target.setPlaceholderText("Enter Domain (example.com)")
        self.whois_target.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #3498db;
                border-radius: 5px;
                background-color: #2c3e50;
                color: white;
            }
        """)

        self.whois_btn = QPushButton("▶️ Run Whois")
        self.whois_btn.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        self.whois_btn.clicked.connect(self.build_whois)

        whois_layout.addWidget(QLabel("Domain:"))
        whois_layout.addWidget(self.whois_target)
        whois_layout.addWidget(self.whois_btn)
        whois_layout.addStretch()

        whois_group.setLayout(whois_layout)
        whois_group.setStyleSheet("""
            QGroupBox {
                color: white;
                border: 2px solid #3498db;
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
        # HARVESTER INPUT PANEL
        # ========================

        harvester_group = QGroupBox("🕵️ theHarvester OSINT")
        harvester_layout = QVBoxLayout()

        self.harvester_domain = QLineEdit()
        self.harvester_domain.setPlaceholderText("Enter Domain")
        self.harvester_domain.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #3498db;
                border-radius: 5px;
                background-color: #2c3e50;
                color: white;
            }
        """)

        self.harvester_source = QComboBox()
        self.harvester_source.addItems([
            "google",
            "bing",
            "yahoo",
            "duckduckgo"
        ])
        self.harvester_source.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #3498db;
                border-radius: 5px;
                background-color: #2c3e50;
                color: white;
            }
        """)

        self.harvester_btn = QPushButton("▶️ Run Harvester")
        self.harvester_btn.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        self.harvester_btn.clicked.connect(self.build_harvester)

        harvester_layout.addWidget(QLabel("Domain:"))
        harvester_layout.addWidget(self.harvester_domain)
        harvester_layout.addWidget(QLabel("Data Source:"))
        harvester_layout.addWidget(self.harvester_source)
        harvester_layout.addWidget(self.harvester_btn)
        harvester_layout.addStretch()

        harvester_group.setLayout(harvester_layout)
        harvester_group.setStyleSheet("""
            QGroupBox {
                color: white;
                border: 2px solid #3498db;
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

        main_layout.addWidget(nmap_group)
        main_layout.addWidget(whois_group)
        main_layout.addWidget(harvester_group)
        main_layout.addStretch()

        self.setLayout(main_layout)

        # Apply label styling
        self.setStyleSheet("QLabel { color: white; }")

        # Apply current mode rules when page loads
        self.update_mode(app_state.mode)

    # ========================
    # PANEL DISPLAY METHODS
    # ========================

    def show_nmap_panel(self):
        """Focus on Nmap target input when icon clicked"""
        self.nmap_target.setFocus()
        self.nmap_target.selectAll()

    def show_whois_panel(self):
        """Focus on Whois target input when icon clicked"""
        self.whois_target.setFocus()
        self.whois_target.selectAll()

    def show_harvester_panel(self):
        """Focus on Harvester domain input when icon clicked"""
        self.harvester_domain.setFocus()
        self.harvester_domain.selectAll()

    # ========================
    # MODE UPDATE FUNCTION
    # ========================

    def update_mode(self, mode):
        index = self.scan_type.findText("Aggressive Scan")

        if index != -1:
            item = self.scan_type.model().item(index)

            if mode == "Beginner":
                item.setEnabled(False)

                # If currently selected, reset to safe option
                if self.scan_type.currentText() == "Aggressive Scan":
                    self.scan_type.setCurrentIndex(0)

            else:
                item.setEnabled(True)

    # ========================
    # NMAP COMMAND
    # ========================

    def build_nmap(self):
        target = self.nmap_target.text().strip()
        if not target:
            return

        app_state.reset_scan()

        scan = self.scan_type.currentText()

        # Backend safety check
        if scan == "Aggressive Scan" and app_state.mode == "Beginner":
            print("Aggressive scan disabled in Beginner mode.")
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
    # WHOIS COMMAND
    # ========================

    def build_whois(self):
        target = self.whois_target.text().strip()
        if not target:
            return

        command = f"whois {target}"
        self.run_command.emit(command)

    # ========================
    # HARVESTER COMMAND
    # ========================

    def build_harvester(self):
        domain = self.harvester_domain.text().strip()
        source = self.harvester_source.currentText()

        if not domain:
            return

        command = f"theHarvester -d {domain} -b {source}"
        self.run_command.emit(command)