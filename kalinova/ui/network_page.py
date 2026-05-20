from PyQt6.QtWidgets import QLabel, QLineEdit, QComboBox
from PyQt6.QtCore import pyqtSignal

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

    def show_netcat_panel(self):
        self.activate_tool("netcat")

    def show_wireshark_panel(self):
        self.activate_tool("wireshark")

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
