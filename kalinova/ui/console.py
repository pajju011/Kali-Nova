from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel
from datetime import datetime


class Console(QWidget):
    def __init__(self, panel_title="Console", output_height=150):
        super().__init__()

        self.setObjectName("consolePanel")
        self.font_size = 13  # Default readable font size

        layout = QVBoxLayout()
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(6)

        # Header with Title, Zoom Controls, and Toggle Button
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(4)
        
        self.title_label = QLabel(panel_title)
        self.title_label.setObjectName("consoleTitle")
        self.title_label.setStyleSheet("font-size: 13px; font-weight: 700; color: #bcd0f5;")

        # Zoom controls
        self.zoom_out_btn = QPushButton("A-")
        self.zoom_out_btn.setToolTip("Decrease Font Size")
        self.zoom_out_btn.setFixedWidth(28)
        self.zoom_out_btn.clicked.connect(self.zoom_out)
        
        self.zoom_in_btn = QPushButton("A+")
        self.zoom_in_btn.setToolTip("Increase Font Size")
        self.zoom_in_btn.setFixedWidth(28)
        self.zoom_in_btn.clicked.connect(self.zoom_in)

        btn_style = """
            QPushButton {
                padding: 3px 6px;
                font-size: 11px;
                font-weight: bold;
                background-color: #1a2438;
                border: 1px solid #3a4a6c;
                border-radius: 4px;
                color: #8ea2c5;
            }
            QPushButton:hover {
                background-color: #24324f;
                color: #d7e5ff;
                border-color: #4d89ff;
            }
        """
        self.zoom_out_btn.setStyleSheet(btn_style)
        self.zoom_in_btn.setStyleSheet(btn_style)

        self.toggle_btn = QPushButton("Collapse" if output_height is None else "Expand Logs")
        self.toggle_btn.setObjectName("consoleToggleBtn")
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setChecked(output_height is not None)  # True = collapsed for bottom console, False = expanded for side output
        self.toggle_btn.clicked.connect(self.toggle_collapsed)
        self.toggle_btn.setStyleSheet("""
            QPushButton#consoleToggleBtn {
                padding: 4px 10px;
                font-size: 11px;
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
        header_layout.addWidget(self.zoom_out_btn)
        header_layout.addWidget(self.zoom_in_btn)
        header_layout.addWidget(self.toggle_btn)

        # Status bar (Always Visible)
        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("consoleStatus")
        self.status_label.setStyleSheet(
            "color: #2ecc71; font-weight: bold; padding: 2px 5px; font-size: 12px;"
        )

        # Output console
        self.output = QTextEdit()
        self.output.setObjectName("consoleOutput")
        self.output.setReadOnly(True)
        if output_height is not None:
            self.output.setFixedHeight(output_height)
        
        self.update_output_style()

        layout.addLayout(header_layout)
        layout.addWidget(self.status_label)
        layout.addWidget(self.output)
        self.setLayout(layout)

        # Bottom console starts collapsed, side tool output tabs start expanded
        if output_height is not None:
            self.output.hide()
        else:
            self.output.show()

    def zoom_in(self):
        if self.font_size < 26:
            self.font_size += 1
            self.update_output_style()

    def zoom_out(self):
        if self.font_size > 9:
            self.font_size -= 1
            self.update_output_style()

    def update_output_style(self):
        self.output.setStyleSheet(f"""
            QTextEdit {{
                background-color: #08100f;
                color: #6cff9a;
                font-family: 'Consolas', 'Cascadia Code', 'Courier New', monospace;
                font-size: {self.font_size}px;
                line-height: 1.5;
                padding: 8px;
            }}
        """)

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
        colors = {
            "info": "#2ecc71",      # Green
            "running": "#f39c12",   # Orange
            "success": "#27ae60",   # Dark Green
            "error": "#e74c3c"      # Red
        }
        
        color = colors.get(status_type, "#2ecc71")
        self.status_label.setText(status)
        self.status_label.setStyleSheet(
            f"color: {color}; font-weight: bold; padding: 4px; font-size: 12px;"
        )

    def clear(self):
        self.output.clear()
        self.set_status("Ready", "info")

