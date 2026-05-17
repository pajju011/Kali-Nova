from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton,
    QComboBox, QGroupBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from ui.tool_icon_button import ToolIconButton


class NetworkPage(QWidget):

    run_command = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        # ========================
        # TITLE
        # ========================
        title = QLabel("🌐 Network Tools")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: #9b59b6; padding: 10px;")
        main_layout.addWidget(title)

        # ========================
        # TOOLS GRID
        # ========================
        tools_layout = QHBoxLayout()
        tools_layout.setSpacing(20)

        # NETCAT Icon Button
        self.netcat_icon = ToolIconButton("🔗", "Netcat", "Network Utility")
        self.netcat_icon.clicked.connect(self.show_netcat_panel)
        tools_layout.addWidget(self.netcat_icon)

        # WIRESHARK Icon Button
        self.wireshark_icon = ToolIconButton("🔎", "Wireshark", "Packet Analysis")
        self.wireshark_icon.clicked.connect(self.show_wireshark_panel)
        tools_layout.addWidget(self.wireshark_icon)

        tools_layout.addStretch()
        main_layout.addLayout(tools_layout)

        # ========================
        # NETCAT INPUT PANEL
        # ========================

        netcat_group = QGroupBox("🔗 Netcat Utility")
        netcat_layout = QVBoxLayout()

        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("Target IP")
        self.target_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #9b59b6;
                border-radius: 5px;
                background-color: #2c3e50;
                color: white;
            }
        """)

        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("Port")
        self.port_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #9b59b6;
                border-radius: 5px;
                background-color: #2c3e50;
                color: white;
            }
        """)

        self.mode_dropdown = QComboBox()
        self.mode_dropdown.addItems([
            "Connect to Target",
            "Listen Mode"
        ])
        self.mode_dropdown.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #9b59b6;
                border-radius: 5px;
                background-color: #2c3e50;
                color: white;
            }
        """)

        self.netcat_btn = QPushButton("▶️ Run Netcat")
        self.netcat_btn.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background-color: #9b59b6;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        self.netcat_btn.clicked.connect(self.build_netcat)

        netcat_layout.addWidget(QLabel("Target IP:"))
        netcat_layout.addWidget(self.target_input)
        netcat_layout.addWidget(QLabel("Port:"))
        netcat_layout.addWidget(self.port_input)
        netcat_layout.addWidget(QLabel("Mode:"))
        netcat_layout.addWidget(self.mode_dropdown)
        netcat_layout.addWidget(self.netcat_btn)
        netcat_layout.addStretch()

        netcat_group.setLayout(netcat_layout)
        netcat_group.setStyleSheet("""
            QGroupBox {
                color: white;
                border: 2px solid #9b59b6;
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
        # WIRESHARK INPUT PANEL
        # ========================

        wireshark_group = QGroupBox("🔎 Wireshark Packet Analyzer")
        wireshark_layout = QVBoxLayout()

        info_label = QLabel("Click 'Launch Wireshark' to start packet capture and analysis")
        info_label.setStyleSheet("color: #95a5a6; font-style: italic; padding: 10px;")

        self.wireshark_btn = QPushButton("▶️ Launch Wireshark")
        self.wireshark_btn.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background-color: #9b59b6;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        self.wireshark_btn.clicked.connect(self.launch_wireshark)

        wireshark_layout.addWidget(info_label)
        wireshark_layout.addWidget(self.wireshark_btn)
        wireshark_layout.addStretch()

        wireshark_group.setLayout(wireshark_layout)
        wireshark_group.setStyleSheet("""
            QGroupBox {
                color: white;
                border: 2px solid #9b59b6;
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

        main_layout.addWidget(netcat_group)
        main_layout.addWidget(wireshark_group)
        main_layout.addStretch()

        self.setLayout(main_layout)

        # Apply label styling
        self.setStyleSheet("QLabel { color: white; }")

    # ========================
    # PANEL DISPLAY METHODS
    # ========================

    def show_netcat_panel(self):
        """Focus on Netcat target input when icon clicked"""
        self.target_input.setFocus()
        self.target_input.selectAll()

    def show_wireshark_panel(self):
        """Launch Wireshark"""
        self.launch_wireshark()

    # ========================
    # NETCAT COMMAND
    # ========================

    def build_netcat(self):
        target = self.target_input.text().strip()
        port = self.port_input.text().strip()
        mode = self.mode_dropdown.currentText()

        if not port:
            return

        if mode == "Connect to Target":
            if not target:
                return
            command = f"nc {target} {port}"
        else:
            command = f"nc -lvnp {port}"

        self.run_command.emit(command)

    # ========================
    # WIRESHARK LAUNCH
    # ========================

    def launch_wireshark(self):
        command = "wireshark"
        self.run_command.emit(command)