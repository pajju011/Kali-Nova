from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel
from datetime import datetime


class Console(QWidget):
    def __init__(self, panel_title="Console", output_height=150):
        super().__init__()

        self.setObjectName("consolePanel")

        layout = QVBoxLayout()
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(4)

        # Header with Title and Toggle Button
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        self.title_label = QLabel(panel_title)
        self.title_label.setObjectName("consoleTitle")
        
        self.toggle_btn = QPushButton("Expand Logs")
        self.toggle_btn.setObjectName("consoleToggleBtn")
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setChecked(True)  # True means collapsed by default
        self.toggle_btn.clicked.connect(self.toggle_collapsed)
        self.toggle_btn.setStyleSheet("""
            QPushButton#consoleToggleBtn {
                padding: 3px 8px;
                font-size: 10px;
                font-weight: 600;
                background-color: #1a2438;
                border: 1px solid #3a4a6c;
                border-radius: 4px;
                color: #8ea2c5;
            }
            QPushButton#consoleToggleBtn:hover {
                background-color: #24324f;
                color: #d7e5ff;
                border-color: #4d89ff;
            }
            QPushButton#consoleToggleBtn:checked {
                background-color: #111a2e;
                color: #8ea2c5;
            }
        """)
        
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.toggle_btn)

        # Status bar (Always Visible)
        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("consoleStatus")
        self.status_label.setStyleSheet(
            "color: #2ecc71; font-weight: bold; padding: 2px 5px;"
        )

        # Output console (Collapsible)
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

        layout.addLayout(header_layout)
        layout.addWidget(self.status_label)
        layout.addWidget(self.output)
        self.setLayout(layout)

        # Collapse by default on launch to save space
        self.output.hide()

    def toggle_collapsed(self):
        is_collapsed = self.toggle_btn.isChecked()
        self.output.setVisible(not is_collapsed)
        if is_collapsed:
            self.toggle_btn.setText("Expand Logs")
        else:
            self.toggle_btn.setText("Collapse")

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
