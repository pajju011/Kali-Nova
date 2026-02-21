from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
)

from ui.topbar import TopBar
from ui.sidebar import Sidebar
from ui.console import Console
from ui.workspace import Workspace


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Kalinova Control Center")
        self.setGeometry(100, 100, 1400, 800)

        central = QWidget()
        main_layout = QVBoxLayout()

        self.topbar = TopBar()
        main_layout.addWidget(self.topbar)

        middle_layout = QHBoxLayout()

        self.sidebar = Sidebar()
        self.workspace = Workspace()

        middle_layout.addWidget(self.sidebar, 1)
        middle_layout.addWidget(self.workspace, 4)

        main_layout.addLayout(middle_layout)

        self.console = Console()
        main_layout.addWidget(self.console)

        central.setLayout(main_layout)
        self.setCentralWidget(central)

        # Connect sidebar navigation
        self.sidebar.navigate.connect(self.workspace.switch_page)