import re
import html
from datetime import datetime

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QLabel, QLineEdit
)
from PyQt6.QtCore import pyqtSignal

ANSI_REGEX = re.compile(r'\x1b\[([0-9;]*)m')
ANSI_COLORS = {
    "30": "#64748b", "31": "#ef4444", "32": "#22c55e", "33": "#eab308",
    "34": "#3b82f6", "35": "#d946ef", "36": "#06b6d4", "37": "#f8fafc",
    "90": "#94a3b8", "91": "#f87171", "92": "#4ade80", "93": "#fde047",
    "94": "#60a5fa", "95": "#e879f9", "96": "#22d3ee", "97": "#ffffff"
}

def ansi_to_html(text: str) -> str:
    """Converts terminal ANSI color escape codes into styled HTML spans."""
    if not text:
        return ""
    if "\x1b[" not in text:
        return html.escape(text)

    parts = []
    last_end = 0
    current_color = None
    is_bold = False

    for match in ANSI_REGEX.finditer(text):
        parts.append(html.escape(text[last_end:match.start()]))
        codes = match.group(1).split(';') if match.group(1) else ['0']
        for code in codes:
            if code in ('0', ''):
                if current_color or is_bold:
                    parts.append('</span>')
                    current_color = None
                    is_bold = False
            elif code == '1':
                is_bold = True
            elif code in ANSI_COLORS:
                if current_color or is_bold:
                    parts.append('</span>')
                current_color = ANSI_COLORS[code]
                style = f"color: {current_color};"
                if is_bold:
                    style += " font-weight: bold;"
                parts.append(f'<span style="{style}">')
        last_end = match.end()

    parts.append(html.escape(text[last_end:]))
    if current_color or is_bold:
        parts.append('</span>')

    return "".join(parts)


class Console(QWidget):

    input_submitted = pyqtSignal(str)

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

        # Interactive Terminal Input Bar (stdin)
        self.input_container = QWidget()
        input_layout = QHBoxLayout(self.input_container)
        input_layout.setContentsMargins(0, 2, 0, 0)
        input_layout.setSpacing(6)

        self.input_edit = QLineEdit()
        self.input_edit.setObjectName("consoleInputEdit")
        self.input_edit.setPlaceholderText("Type interactive terminal input (e.g. Y/n, password, flags) and press Enter...")
        self.input_edit.setStyleSheet("""
            QLineEdit#consoleInputEdit {
                background-color: #0b1426;
                color: #00f0ff;
                border: 1px solid #1e2e4a;
                border-radius: 4px;
                padding: 5px 8px;
                font-family: 'Consolas', 'Cascadia Code', monospace;
                font-size: 12px;
            }
            QLineEdit#consoleInputEdit:focus {
                border-color: #00f0ff;
            }
        """)
        self.input_edit.returnPressed.connect(self._handle_send_input)

        self.send_btn = QPushButton("Send ↵")
        self.send_btn.setObjectName("consoleSendBtn")
        self.send_btn.setToolTip("Send input to running tool (stdin)")
        self.send_btn.clicked.connect(self._handle_send_input)
        self.send_btn.setStyleSheet("""
            QPushButton#consoleSendBtn {
                background-color: #00f0ff;
                color: #030712;
                font-weight: 700;
                font-size: 11px;
                border: none;
                border-radius: 4px;
                padding: 5px 12px;
            }
            QPushButton#consoleSendBtn:hover {
                background-color: #38bdf8;
            }
            QPushButton#consoleSendBtn:pressed {
                background-color: #0284c7;
            }
        """)

        input_layout.addWidget(self.input_edit)
        input_layout.addWidget(self.send_btn)

        layout.addLayout(header_layout)
        layout.addWidget(self.status_label)
        layout.addWidget(self.output)
        layout.addWidget(self.input_container)
        self.setLayout(layout)

        # Bottom console starts collapsed, side tool output tabs start expanded
        if output_height is not None:
            self.output.hide()
            self.input_container.hide()
        else:
            self.output.show()
            self.input_container.show()

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
        self.input_container.setVisible(not is_collapsed)
        if is_collapsed:
            self.toggle_btn.setText("Expand Logs")
        else:
            self.toggle_btn.setText("Collapse")

    def _handle_send_input(self):
        text = self.input_edit.text()
        if text.strip():
            self.input_submitted.emit(text)
            self.input_edit.clear()

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        if "\x1b[" in message:
            rendered = ansi_to_html(message)
            formatted_html = f'<span style="color: #64748b;">[{timestamp}]</span> {rendered}'
            self.output.append(formatted_html)
        else:
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


