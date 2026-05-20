from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel
from datetime import datetime


class Console(QWidget):
    def __init__(self, panel_title="Console", output_height=150):
        super().__init__()

        self.setObjectName("consolePanel")

        layout = QVBoxLayout()
        layout.setContentsMargins(12, 8, 12, 10)
        layout.setSpacing(6)

        self.title_label = QLabel(panel_title)
        self.title_label.setObjectName("consoleTitle")

        # Status bar
        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("consoleStatus")
        self.status_label.setStyleSheet(
            "color: #2ecc71; font-weight: bold; padding: 5px;"
        )

        # Output console
        self.output = QTextEdit()
        self.output.setObjectName("consoleOutput")
        self.output.setReadOnly(True)
        if output_height is not None:
            self.output.setFixedHeight(output_height)
        self.output.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #00ff00;
                font-family: 'Courier New';
                font-size: 10px;
            }
        """)

        layout.addWidget(self.title_label)
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
