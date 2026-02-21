from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal


class Sidebar(QWidget):

    navigate = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        sections = [
            "Dashboard",
            "Recon",
            "Web Testing",
            "Authentication",
            "Network",
            "Reports",
            "Settings"
        ]

        for section in sections:
            btn = QPushButton(section)
            btn.clicked.connect(lambda checked, s=section: self.navigate.emit(s))
            layout.addWidget(btn)

        layout.addStretch()
        self.setLayout(layout)