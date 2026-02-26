from PyQt6.QtWidgets import (
    QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout
)

from ui.sidebar import Sidebar
from ui.topbar import TopBar
from ui.workspace import Workspace
from ui.console import Console
from core.executor import CommandThread


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Kalinova OS")
        self.setGeometry(100, 100, 1300, 800)

        # =========================
        # Central Layout
        # =========================
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        middle_layout = QHBoxLayout()

        # Create Components FIRST
        self.topbar = TopBar()
        self.sidebar = Sidebar()
        self.workspace = Workspace()
        self.console = Console()

        # =========================
        # Layout Structure
        # =========================
        main_layout.addWidget(self.topbar)

        middle_layout.addWidget(self.sidebar, 1)
        middle_layout.addWidget(self.workspace, 4)

        main_layout.addLayout(middle_layout)
        main_layout.addWidget(self.console)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # =========================
        # Navigation Connection
        # =========================
        self.sidebar.navigate.connect(self.workspace.switch_page)

        # =========================
        # Mode Change Connection
        # =========================
        self.topbar.mode_changed.connect(
            self.workspace.pages["Recon"].update_mode
        )

        # =========================
        # Tool Execution Connections
        # =========================

        recon = self.workspace.pages["Recon"]
        recon.run_command.connect(self.execute)

        web = self.workspace.pages["Web"]
        web.run_command.connect(self.execute)

        auth = self.workspace.pages["Auth"]
        auth.run_command.connect(self.execute)

        network = self.workspace.pages["Network"]
        network.run_command.connect(self.execute)

    # =========================
    # Command Execution
    # =========================
    def execute(self, command):

        self.thread = CommandThread(command)
        self.thread.output_signal.connect(self.console.log)
        self.thread.start()  