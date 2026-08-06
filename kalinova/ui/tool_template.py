import os
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QStackedWidget,
    QGroupBox,
    QPushButton,
    QScrollArea,
    QTextEdit,
    QLineEdit,
    QComboBox,
    QCheckBox,
)

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from ui.tool_icon_button import ToolIconButton
from core.app_state import app_state
from core.ai_copilot import AICopilot, AIWorkerThread


class ToolCopilotWidget(QFrame):
    """
    Embedded AI Copilot assistant panel presented alongside every security tool.
    Activates on-demand when user clicks 'Analyze Active Setup & Suggest Next Steps' or asks a question,
    automatically inspecting form field inputs, active target, and scan logs.
    """
    def __init__(self, parent_page=None):
        super().__init__()
        self._parent_page = parent_page
        self.setObjectName("toolCopilotWidget")
        self.active_tool_id = "general"
        self.active_tool_name = "Security Tools"
        self.ai_worker = None

        self.setStyleSheet("""
            QFrame#toolCopilotWidget {
                background-color: #0b1424;
                border: 1px solid #1c2a47;
                border-radius: 10px;
                padding: 12px;
                margin-top: 10px;
            }
            QLabel#copilotTitle {
                color: #00f0ff;
                font-weight: bold;
                font-size: 13px;
                letter-spacing: 0.5px;
            }
            QPushButton#analyzeBtn {
                background: linear-gradient(135deg, #00f0ff 0%, #3b82f6 100%);
                color: #050b14;
                font-weight: bold;
                font-size: 12px;
                border-radius: 6px;
                padding: 8px 16px;
                border: none;
            }
            QPushButton#analyzeBtn:hover {
                background: linear-gradient(135deg, #38bdf8 0%, #60a5fa 100%);
            }
            QTextEdit#copilotOutput {
                background-color: #060c18;
                color: #10b981;
                font-family: 'Courier New', monospace;
                font-size: 11px;
                border: 1px solid #142238;
                border-radius: 6px;
                padding: 10px;
            }
            QPushButton.quickChip {
                background-color: #16243b;
                color: #8ea2c5;
                border: 1px solid #233758;
                border-radius: 4px;
                padding: 4px 10px;
                font-size: 10px;
                font-weight: bold;
            }
            QPushButton.quickChip:hover {
                background-color: #24385a;
                color: #00f0ff;
                border-color: #3b82f6;
            }
            QLineEdit#copilotInput {
                background-color: #0d1a30;
                border: 1px solid #1e2e4a;
                border-radius: 6px;
                color: #e2e8f0;
                padding: 6px;
                font-size: 11px;
            }
            QPushButton#askBtn {
                background-color: #00f0ff;
                color: #0b1220;
                font-weight: bold;
                border-radius: 6px;
                padding: 6px 14px;
                font-size: 11px;
                border: none;
            }
            QPushButton#askBtn:hover {
                background-color: #38bdf8;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        # Header
        header_layout = QHBoxLayout()
        self.title_label = QLabel("🤖 AI COPILOT TOOL ASSISTANT")
        self.title_label.setObjectName("copilotTitle")
        
        self.status_label = QLabel("● STANDBY")
        self.status_label.setStyleSheet("color: #64748b; font-size: 10px; font-weight: bold;")
        
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.status_label)
        layout.addLayout(header_layout)

        # Primary Trigger Button: Analyze active setup
        self.btn_analyze = QPushButton("🤖 Analyze Active Setup & Suggest Next Steps")
        self.btn_analyze.setObjectName("analyzeBtn")
        self.btn_analyze.clicked.connect(self._on_analyze_clicked)
        layout.addWidget(self.btn_analyze)

        # Output text box
        self.output_text = QTextEdit()
        self.output_text.setObjectName("copilotOutput")
        self.output_text.setReadOnly(True)
        self.output_text.setMinimumHeight(110)
        self.output_text.setMaximumHeight(180)
        self.output_text.setText("💡 Enter your parameters above and click 'Analyze Active Setup & Suggest Next Steps' to get AI guidance.")
        layout.addWidget(self.output_text)

        # Quick action chips
        chips_layout = QHBoxLayout()
        chips_layout.setSpacing(8)
        
        self.btn_chip_usage = QPushButton("💡 Explain Usage")
        self.btn_chip_usage.setProperty("class", "quickChip")
        self.btn_chip_usage.clicked.connect(lambda: self.ask_question(f"How do I use {self.active_tool_name}?"))

        self.btn_chip_flags = QPushButton("🚀 Key Flags")
        self.btn_chip_flags.setProperty("class", "quickChip")
        self.btn_chip_flags.clicked.connect(lambda: self.ask_question(f"What are the best flags for {self.active_tool_name}?"))

        self.btn_chip_remed = QPushButton("🛡️ Hardening")
        self.btn_chip_remed.setProperty("class", "quickChip")
        self.btn_chip_remed.clicked.connect(lambda: self.ask_question(f"How to fix vulnerabilities found by {self.active_tool_name}?"))

        chips_layout.addWidget(self.btn_chip_usage)
        chips_layout.addWidget(self.btn_chip_flags)
        chips_layout.addWidget(self.btn_chip_remed)
        chips_layout.addStretch()
        layout.addLayout(chips_layout)

        # Input row
        prompt_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setObjectName("copilotInput")
        self.input_field.setPlaceholderText("Ask AI Copilot about this tool...")
        self.input_field.returnPressed.connect(self._on_ask_clicked)

        self.ask_btn = QPushButton("Ask AI")
        self.ask_btn.setObjectName("askBtn")
        self.ask_btn.clicked.connect(self._on_ask_clicked)

        prompt_layout.addWidget(self.input_field)
        prompt_layout.addWidget(self.ask_btn)
        layout.addLayout(prompt_layout)

    def set_tool(self, tool_id: str, tool_name: str):
        self.active_tool_id = tool_id
        self.active_tool_name = tool_name
        self.title_label.setText(f"🤖 AI COPILOT TOOL ASSISTANT — {tool_name.upper()}")
        self.input_field.setPlaceholderText(f"Ask AI about {tool_name} (e.g. flags, parameters)...")
        self.status_label.setText("● STANDBY")
        self.status_label.setStyleSheet("color: #64748b; font-size: 10px; font-weight: bold;")
        self.output_text.setText(f"💡 Click '🤖 Analyze Active Setup & Suggest Next Steps' to inspect {tool_name} parameters and receive recommendations.")

    def _on_analyze_clicked(self):
        self.ask_question(f"Analyze my active setup for {self.active_tool_name} and suggest next steps.")

    def ask_question(self, question_text: str):
        # Gather active form inputs from parent page
        form_context_str = ""
        if self._parent_page and hasattr(self._parent_page, "get_active_tool_context"):
            ctx_data = self._parent_page.get_active_tool_context()
            inputs_dict = ctx_data.get("inputs", {})
            if inputs_dict:
                form_context_str = ", ".join([f"{k}={v}" for k, v in inputs_dict.items()])
            else:
                form_context_str = "No custom form parameters entered yet"

        context_parts = [
            f"Active Tool: {self.active_tool_name} (ID: {self.active_tool_id})",
            f"User Form Inputs: {form_context_str}",
            f"Global Threat Level: {app_state.global_risk} (Score: {app_state.risk_score}/100)",
            f"Discovered Open Ports: {app_state.open_ports}",
            f"Current Recommendation: {app_state.suggestion}"
        ]
        context = "\n".join(context_parts)

        self.status_label.setText("● THINKING...")
        self.status_label.setStyleSheet("color: #f59e0b; font-size: 10px; font-weight: bold;")
        self.ask_btn.setEnabled(False)
        self.btn_analyze.setEnabled(False)
        self.output_text.setText(f"🧠 AI Copilot is inspecting {self.active_tool_name} parameters and crafting analysis...")

        if self.ai_worker is not None and self.ai_worker.isRunning():
            self.ai_worker.quit()
            self.ai_worker.wait(500)

        self.ai_worker = AIWorkerThread(context_info=context, user_prompt=question_text)
        self.ai_worker.finished_signal.connect(self._on_ai_finished)
        self.ai_worker.error_signal.connect(self._on_ai_error)
        self.ai_worker.start()

        if os.environ.get("QT_QPA_PLATFORM") == "offscreen":
            self.ai_worker.wait(2000)

    def _on_ask_clicked(self):
        query = self.input_field.text().strip()
        if not query:
            query = f"How to use {self.active_tool_name}?"
        self.input_field.clear()
        self.ask_question(query)

    def _on_ai_finished(self, response: str):
        self.ask_btn.setEnabled(True)
        self.btn_analyze.setEnabled(True)
        self.status_label.setText("● READY")
        self.status_label.setStyleSheet("color: #10b981; font-size: 10px; font-weight: bold;")
        self.output_text.setText(response)

    def _on_ai_error(self, err_msg: str):
        self.ask_btn.setEnabled(True)
        self.btn_analyze.setEnabled(True)
        self.status_label.setText("● ERROR")
        self.status_label.setStyleSheet("color: #f43f5e; font-size: 10px; font-weight: bold;")
        self.output_text.setText(f"❌ AI Error: {err_msg}")



class ToolModulePage(QScrollArea):
    """
    Shared module layout:
    - Header with title/subtitle
    - Horizontal tool cards
    - Empty state + stacked tool panels
    - Embedded AI Copilot Assistant Widget
    """

    validation_error = pyqtSignal(str)

    def __init__(self, title, accent_color, subtitle):
        super().__init__()

        self.accent_color = accent_color
        self._selected_tool = None
        self._tool_buttons = {}
        self._tool_panel_index = {}
        self._tool_focus_widget = {}
        self._tool_names = {}

        self.setObjectName("toolModulePage")
        self.setWidgetResizable(True)
        self.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        # Create a container widget for all the content
        self.container = QWidget()
        self.container.setObjectName("toolModulePageContainer")
        self.container.setStyleSheet("background: transparent;")

        main_layout = QVBoxLayout(self.container)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(16)

        # Header
        header = QFrame()
        header.setObjectName("toolModuleHeader")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(20, 16, 20, 16)
        header_layout.setSpacing(6)

        title_label = QLabel(title)
        title_label.setObjectName("toolModuleTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {accent_color};")

        subtitle_label = QLabel(subtitle)
        subtitle_label.setObjectName("toolModuleSubtitle")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setWordWrap(True)

        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        main_layout.addWidget(header)

        # Tool cards row
        tools_row = QFrame()
        tools_row.setObjectName("toolRow")
        self.tools_layout = QHBoxLayout(tools_row)
        self.tools_layout.setSpacing(14)
        self.tools_layout.setContentsMargins(8, 4, 8, 4)
        self.tools_layout.addStretch()
        main_layout.addWidget(tools_row)

        # Panel area
        panel_container = QFrame()
        panel_container.setObjectName("panelContainer")
        panel_layout = QVBoxLayout(panel_container)
        panel_layout.setContentsMargins(16, 16, 16, 16)
        panel_layout.setSpacing(12)

        self.panel_stack = QStackedWidget()
        self.empty_panel = self._build_empty_panel()
        self.panel_stack.addWidget(self.empty_panel)

        panel_layout.addWidget(self.panel_stack)

        # Integrated AI Copilot Tool Assistant widget
        self.copilot_widget = ToolCopilotWidget(parent_page=self)
        panel_layout.addWidget(self.copilot_widget)

        main_layout.addWidget(panel_container, 1)

        self.setWidget(self.container)

    def get_active_tool_context(self):
        tool_id = self._selected_tool
        if not tool_id or tool_id not in self._tool_panel_index:
            return {
                "tool_id": "none",
                "tool_name": "No Tool Selected",
                "inputs": {}
            }

        panel_index = self._tool_panel_index[tool_id]
        panel_widget = self.panel_stack.widget(panel_index)

        inputs = {}
        if panel_widget:
            for le in panel_widget.findChildren(QLineEdit):
                name = le.placeholderText() or le.objectName() or "Input"
                val = le.text().strip()
                if val:
                    inputs[name] = val
            for cb in panel_widget.findChildren(QComboBox):
                name = cb.objectName() or "Option"
                inputs[name] = cb.currentText()
            for chk in panel_widget.findChildren(QCheckBox):
                if chk.isChecked():
                    inputs[chk.text()] = "Enabled"

        return {
            "tool_id": tool_id,
            "tool_name": self._tool_names.get(tool_id, tool_id),
            "inputs": inputs
        }

    def _build_empty_panel(self):

        empty = QWidget()
        layout = QVBoxLayout(empty)
        layout.setContentsMargins(24, 40, 24, 40)
        layout.setSpacing(8)

        hint_title = QLabel("Select a tool to begin")
        hint_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint_title.setObjectName("emptyStateTitle")
        hint_title.setFont(QFont("Segoe UI", 16, QFont.Weight.DemiBold))

        hint_subtitle = QLabel(
            "Tool options and input fields appear here after you choose a tool card above."
        )
        hint_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint_subtitle.setWordWrap(True)
        hint_subtitle.setObjectName("emptyStateSubtitle")

        layout.addStretch()
        layout.addWidget(hint_title)
        layout.addWidget(hint_subtitle)
        layout.addStretch()

        return empty

    def create_panel(self, title):
        panel = QGroupBox(title)
        panel.setProperty("class", "toolPanelGroup")
        panel_layout = QVBoxLayout(panel)
        panel_layout.setSpacing(10)
        panel_layout.setContentsMargins(14, 18, 14, 14)
        return panel, panel_layout

    def create_primary_button(self, text):
        button = QPushButton(text)
        button.setProperty("role", "primary")
        button.setMinimumHeight(42)
        return button

    def create_secondary_button(self, text):
        button = QPushButton(text)
        button.setProperty("role", "secondary")
        button.setMinimumHeight(38)
        return button

    def add_tool(self, tool_id, icon, name, description, panel, focus_widget=None):
        tool_button = ToolIconButton(icon, name, description, self.accent_color)
        tool_button.clicked.connect(lambda key=tool_id: self.activate_tool(key))

        # Insert before stretch so cards stay left-aligned
        insert_index = max(self.tools_layout.count() - 1, 0)
        self.tools_layout.insertWidget(insert_index, tool_button)

        panel_index = self.panel_stack.addWidget(panel)

        self._tool_buttons[tool_id] = tool_button
        self._tool_panel_index[tool_id] = panel_index
        self._tool_focus_widget[tool_id] = focus_widget
        self._tool_names[tool_id] = name

    def activate_tool(self, tool_id):
        if tool_id not in self._tool_panel_index:
            return

        self._selected_tool = tool_id
        self.panel_stack.setCurrentIndex(self._tool_panel_index[tool_id])

        for key, button in self._tool_buttons.items():
            button.set_active(key == tool_id)

        if tool_id in self._tool_names:
            tool_name = self._tool_names[tool_id]
            self.copilot_widget.set_tool(tool_id, tool_name)

        focus_widget = self._tool_focus_widget.get(tool_id)
        if focus_widget is not None:
            focus_widget.setFocus()
            if hasattr(focus_widget, "selectAll"):
                focus_widget.selectAll()

    def emit_validation_error(self, message):
        self.validation_error.emit(message)

    def clear_tool_selection(self):
        self._selected_tool = None
        self.panel_stack.setCurrentIndex(0)
        self.copilot_widget.set_tool("general", "Security Tools")

        for button in self._tool_buttons.values():
            button.set_active(False)

