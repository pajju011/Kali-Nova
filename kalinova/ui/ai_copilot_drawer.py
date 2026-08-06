import os
from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextEdit, QLineEdit, QWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from core.app_state import app_state
from core.ai_copilot import AICopilot, AIWorkerThread


class AICopilotDrawer(QFrame):
    """
    On-Demand Sliding/Floating AI Copilot Drawer.
    Opened via TopBar AI Sparkle Button ('✦ AI Copilot').
    Automatically harvests active tool setup, form inputs, open ports, and threat score,
    offering dynamic AI analysis and interactive follow-up chat.
    """

    def __init__(self, workspace=None, parent=None):
        super().__init__(parent)
        self.workspace = workspace
        self.setObjectName("aiCopilotDrawer")
        self.active_context = {}
        self.ai_worker = None

        self.setStyleSheet("""
            QFrame#aiCopilotDrawer {
                background-color: #0b1424;
                border-left: 2px solid #00f0ff;
                border-top: 1px solid #1c2a47;
                border-bottom: 1px solid #1c2a47;
                border-radius: 0px;
            }
            QLabel#drawerTitle {
                color: #00f0ff;
                font-weight: bold;
                font-size: 14px;
                letter-spacing: 1px;
            }
            QLabel#contextBanner {
                background-color: #0d1a30;
                color: #8ea2c5;
                font-family: 'Courier New', monospace;
                font-size: 11px;
                border: 1px solid #1e2e4a;
                border-radius: 6px;
                padding: 8px;
            }
            QPushButton#reanalyzeBtn {
                background: linear-gradient(135deg, #00f0ff 0%, #3b82f6 100%);
                color: #050b14;
                font-weight: bold;
                font-size: 12px;
                border-radius: 6px;
                padding: 8px 14px;
                border: none;
            }
            QPushButton#reanalyzeBtn:hover {
                background: linear-gradient(135deg, #38bdf8 0%, #60a5fa 100%);
            }
            QTextEdit#drawerOutput {
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
            QLineEdit#drawerInput {
                background-color: #0d1a30;
                border: 1px solid #1e2e4a;
                border-radius: 6px;
                color: #e2e8f0;
                padding: 8px;
                font-size: 11px;
            }
            QPushButton#drawerAskBtn {
                background-color: #00f0ff;
                color: #0b1220;
                font-weight: bold;
                border-radius: 6px;
                padding: 8px 14px;
                font-size: 11px;
                border: none;
            }
            QPushButton#drawerAskBtn:hover {
                background-color: #38bdf8;
            }
            QPushButton#closeDrawerBtn {
                background: transparent;
                color: #64748b;
                font-weight: bold;
                font-size: 14px;
                border: none;
            }
            QPushButton#closeDrawerBtn:hover {
                color: #f43f5e;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        # Header bar
        header_layout = QHBoxLayout()
        self.title_label = QLabel("✦ AI COPILOT ASSISTANT")
        self.title_label.setObjectName("drawerTitle")

        self.status_label = QLabel("● READY")
        self.status_label.setStyleSheet("color: #10b981; font-size: 10px; font-weight: bold;")

        self.close_btn = QPushButton("✖")
        self.close_btn.setObjectName("closeDrawerBtn")
        self.close_btn.setToolTip("Close AI Copilot Drawer (Esc)")
        self.close_btn.clicked.connect(self.hide)

        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.status_label)
        header_layout.addWidget(self.close_btn)
        layout.addLayout(header_layout)

        # Context Banner readout
        self.context_label = QLabel("Active Screen: Dashboard | Target: Localhost")
        self.context_label.setObjectName("contextBanner")
        self.context_label.setWordWrap(True)
        layout.addWidget(self.context_label)

        # Re-Analyze Action Button
        self.reanalyze_btn = QPushButton("🤖 Re-Analyze Screen Setup & Next Steps")
        self.reanalyze_btn.setObjectName("reanalyzeBtn")
        self.reanalyze_btn.clicked.connect(self.run_screen_analysis)
        layout.addWidget(self.reanalyze_btn)

        # Output Area
        self.output_text = QTextEdit()
        self.output_text.setObjectName("drawerOutput")
        self.output_text.setReadOnly(True)
        self.output_text.setText("Standing by for AI Copilot analysis...")
        layout.addWidget(self.output_text, 1)

        # Quick action chips
        chips_layout = QHBoxLayout()
        chips_layout.setSpacing(8)

        self.chip_usage = QPushButton("💡 Explain Usage")
        self.chip_usage.setProperty("class", "quickChip")
        self.chip_usage.clicked.connect(lambda: self.ask_question("How do I use this active tool?"))

        self.chip_flags = QPushButton("🚀 Recommend Flags")
        self.chip_flags.setProperty("class", "quickChip")
        self.chip_flags.clicked.connect(lambda: self.ask_question("What are the best execution flags for this setup?"))

        self.chip_remed = QPushButton("🛡️ Security Remediation")
        self.chip_remed.setProperty("class", "quickChip")
        self.chip_remed.clicked.connect(lambda: self.ask_question("How to fix vulnerabilities found during this scan?"))

        chips_layout.addWidget(self.chip_usage)
        chips_layout.addWidget(self.chip_flags)
        chips_layout.addWidget(self.chip_remed)
        chips_layout.addStretch()
        layout.addLayout(chips_layout)

        # Interactive Chat Row
        prompt_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setObjectName("drawerInput")
        self.input_field.setPlaceholderText("Ask AI Copilot follow-up questions...")
        self.input_field.returnPressed.connect(self._on_ask_clicked)

        self.ask_btn = QPushButton("Ask AI")
        self.ask_btn.setObjectName("drawerAskBtn")
        self.ask_btn.clicked.connect(self._on_ask_clicked)

        prompt_layout.addWidget(self.input_field)
        prompt_layout.addWidget(self.ask_btn)
        layout.addLayout(prompt_layout)

    def inspect_and_open(self):
        """Called when user opens AI Copilot from TopBar or shortcut."""
        self.show()
        self.raise_()
        self.run_screen_analysis()

    def run_screen_analysis(self):
        if self.workspace and hasattr(self.workspace, "get_active_context"):
            self.active_context = self.workspace.get_active_context()
        else:
            self.active_context = {"page_name": "General", "tool_name": "Security Tools", "inputs": {}}

        page_name = self.active_context.get("page_name", "Dashboard")
        tool_name = self.active_context.get("tool_name", page_name)
        inputs_dict = self.active_context.get("inputs", {})

        inputs_str = ", ".join([f"{k}={v}" for k, v in inputs_dict.items()]) if inputs_dict else "No custom inputs entered"
        self.context_label.setText(f"Active Page: {page_name} | Active Tool: {tool_name}\nInputs: {inputs_str}")

        query = f"Analyze my active setup on page {page_name} for tool {tool_name} with inputs: {inputs_str}. Suggest next steps."
        self.ask_question(query)

    def ask_question(self, question_text: str):
        page_name = self.active_context.get("page_name", "Dashboard")
        tool_name = self.active_context.get("tool_name", page_name)
        inputs_dict = self.active_context.get("inputs", {})
        inputs_str = ", ".join([f"{k}={v}" for k, v in inputs_dict.items()]) if inputs_dict else "No custom inputs entered"

        context_parts = [
            f"Active Page: {page_name}",
            f"Active Tool: {tool_name}",
            f"User Form Inputs: {inputs_str}",
            f"Global Threat Level: {app_state.global_risk} (Score: {app_state.risk_score}/100)",
            f"Discovered Open Ports: {app_state.open_ports}",
            f"Active Recommendation: {app_state.suggestion}"
        ]
        context = "\n".join(context_parts)

        self.status_label.setText("● THINKING...")
        self.status_label.setStyleSheet("color: #f59e0b; font-size: 10px; font-weight: bold;")
        self.ask_btn.setEnabled(False)
        self.reanalyze_btn.setEnabled(False)
        self.output_text.setText(f"🧠 AI Copilot is analyzing screen context for {tool_name}...")

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
            query = "What should I do next?"
        self.input_field.clear()
        self.ask_question(query)

    def _on_ai_finished(self, response: str):
        self.ask_btn.setEnabled(True)
        self.reanalyze_btn.setEnabled(True)
        self.status_label.setText("● READY")
        self.status_label.setStyleSheet("color: #10b981; font-size: 10px; font-weight: bold;")
        self.output_text.setText(response)

    def _on_ai_error(self, err_msg: str):
        self.ask_btn.setEnabled(True)
        self.reanalyze_btn.setEnabled(True)
        self.status_label.setText("● ERROR")
        self.status_label.setStyleSheet("color: #f43f5e; font-size: 10px; font-weight: bold;")
        self.output_text.setText(f"❌ AI Error: {err_msg}")
