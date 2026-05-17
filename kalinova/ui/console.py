from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel
from PyQt6.QtCore import Qt
from datetime import datetime


class Console(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # Status bar
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet(
            "color: #2ecc71; font-weight: bold; padding: 5px;"
        )

        # Output console
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setFixedHeight(150)
        self.output.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #00ff00;
                font-family: 'Courier New';
                font-size: 10px;
            }
        """)

        layout.addWidget(self.status_label)
        layout.addWidget(self.output)
        self.setLayout(layout)

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] {message}"
        self.output.append(formatted_msg)

    def set_status(self, status, status_type="info"):
        """
        status_type: 'info', 'running', 'success', 'error'
        """
        colors = {
            "info": "#2ecc71",      # Green
            "running": "#f39c12",   # Orange
            "success": "#27ae60",   # Dark Green
            "error": "#e74c3c"      # Red
        }
        
        color = colors.get(status_type, "#2ecc71")
        self.status_label.setText(status)
        self.status_label.setStyleSheet(
            f"color: {color}; font-weight: bold; padding: 5px;"
        )

    def clear(self):
        self.output.clear()
        self.set_status("Ready", "info")