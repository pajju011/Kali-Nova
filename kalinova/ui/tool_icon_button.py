from PyQt6.QtWidgets import (
    QPushButton, QVBoxLayout, QWidget, QLabel
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont


class ToolIconButton(QWidget):
    """
    Custom tool icon button with emoji icon and label
    Emits a signal when clicked
    """
    clicked = pyqtSignal()

    def __init__(self, icon, tool_name, description=""):
        super().__init__()
        
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(10, 10, 10, 10)

        # Icon Button
        self.icon_btn = QPushButton(icon)
        self.icon_btn.setFixedSize(100, 100)
        self.icon_btn.setFont(QFont("Arial", 40))
        self.icon_btn.setStyleSheet("""
            QPushButton {
                background-color: #2c3e50;
                border: 2px solid #3498db;
                border-radius: 10px;
                color: white;
            }
            QPushButton:hover {
                background-color: #3498db;
                border: 2px solid #2980b9;
            }
            QPushButton:pressed {
                background-color: #2980b9;
            }
        """)
        self.icon_btn.clicked.connect(self.clicked.emit)

        # Tool Name Label
        name_label = QLabel(tool_name)
        name_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setStyleSheet("color: white;")

        # Description Label (optional)
        if description:
            desc_label = QLabel(description)
            desc_label.setFont(QFont("Arial", 8))
            desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            desc_label.setStyleSheet("color: #95a5a6; font-style: italic;")
            layout.addWidget(desc_label)

        layout.addWidget(self.icon_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(name_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(layout)
        self.setMaximumWidth(150)
