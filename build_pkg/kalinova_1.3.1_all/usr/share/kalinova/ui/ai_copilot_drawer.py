import os
import re
import html
from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextEdit, QLineEdit, QWidget, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from core.app_state import app_state
from core.ai_copilot import AICopilot, AIWorkerThread


def format_ai_markdown_html(md_text: str) -> str:
    """
    Renders raw Markdown from AI Copilot into styled, cyber-dark HTML with syntax highlighting,
    clean headers, glowing badges, and styled pre/code blocks.
    """
    if not md_text:
        return ""

    # Escape HTML special characters in code blocks safely
    escaped_blocks = []
    def save_code_block(match):
        lang = match.group(1) or ""
        code = match.group(2)
        code_esc = html.escape(code.strip())
        tag = f'<div style="background: #030712; border: 1px solid #1e2e4a; border-radius: 6px; padding: 10px; margin: 8px 0; font-family: monospace; font-size: 11px; color: #10b981; white-space: pre-wrap;"><div style="color: #64748b; font-size: 9px; font-weight: bold; margin-bottom: 4px; text-transform: uppercase;">[{lang or "CODE"}]</div><code>{code_esc}</code></div>'
        escaped_blocks.append(tag)
        return f"__CODE_BLOCK_{len(escaped_blocks)-1}__"

    # Replace triple backtick code blocks
    processed = re.sub(r'```(\w*)\n(.*?)```', save_code_block, md_text, flags=re.DOTALL)

    # Process inline code `code`
    processed = re.sub(
        r'`([^`]+)`',
        r'<span style="background: #111d33; color: #38bdf8; padding: 2px 6px; border-radius: 4px; font-family: monospace; font-size: 11px;">\1</span>',
        processed
    )

    # Convert headers
    processed = re.sub(
        r'^### (.*?)$',
        r'<div style="color: #38bdf8; font-size: 12px; font-weight: bold; margin-top: 10px; margin-bottom: 4px;">\1</div>',
        processed,
        flags=re.MULTILINE
    )
    processed = re.sub(
        r'^## (.*?)$',
        r'<div style="color: #00f0ff; font-size: 13px; font-weight: bold; margin-top: 12px; margin-bottom: 6px; border-bottom: 1px solid #1e2e4a; padding-bottom: 2px;">\1</div>',
        processed,
        flags=re.MULTILINE
    )
    processed = re.sub(
        r'^# (.*?)$',
        r'<div style="color: #00f0ff; font-size: 14px; font-weight: 800; margin-top: 14px; margin-bottom: 6px;">\1</div>',
        processed,
        flags=re.MULTILINE
    )

    # Process bold **text**
    processed = re.sub(r'\*\*(.*?)\*\*', r'<b style="color: #f8fafc;">\1</b>', processed)

    # Process bullet points
    processed = re.sub(
        r'^[•\-\*]\s+(.*?)$',
        r'<div style="margin-left: 8px; margin-bottom: 3px; color: #cbd5e1;"><span style="color: #00f0ff; font-weight: bold;">▸</span> \1</div>',
        processed,
        flags=re.MULTILINE
    )

    # Convert line breaks
    processed = processed.replace('\n', '<br/>')

    # Restore code blocks
    for idx, block_html in enumerate(escaped_blocks):
        processed = processed.replace(f"__CODE_BLOCK_{idx}__", block_html)

    # Style severity & warning chips
    processed = re.sub(
        r'\[CRITICAL\]',
        r'<span style="background: #e11d48; color: #ffffff; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 10px;">CRITICAL</span>',
        processed
    )
    processed = re.sub(
        r'\[HIGH\]',
        r'<span style="background: #f97316; color: #ffffff; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 10px;">HIGH</span>',
        processed
    )
    processed = re.sub(
        r'\[MEDIUM\]',
        r'<span style="background: #eab308; color: #0b1220; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 10px;">MEDIUM</span>',
        processed
    )
    processed = re.sub(
        r'\[LOW\]',
        r'<span style="background: #10b981; color: #0b1220; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 10px;">LOW</span>',
        processed
    )

    return f"""
    <div style="color: #94a3b8; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 12px; line-height: 1.5;">
        {processed}
    </div>
    """


class AICopilotDrawer(QFrame):
    """
    On-Demand Sliding/Floating Real-Time AI Copilot Drawer.
    Supports real-time live stdout event monitoring, dynamic context auto-syncing,
    CVSS diagnostics, and AI interactive chat.
    """

    def __init__(self, workspace=None, parent=None):
        super().__init__(parent)
        self.workspace = workspace
        self.setObjectName("aiCopilotDrawer")
        self.active_context = {}
        self.ai_worker = None
        self.live_findings = []
        self._is_scan_running = False

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
                font-weight: 800;
                font-size: 13px;
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
            QFrame#liveStreamBox {
                background-color: #050b14;
                border: 1px solid #1e3a5f;
                border-radius: 6px;
                padding: 6px 10px;
            }
            QLabel#liveStreamLabel {
                color: #38bdf8;
                font-size: 10px;
                font-weight: bold;
                font-family: 'Courier New', monospace;
            }
            QPushButton#reanalyzeBtn {
                background-color: #0c2038;
                color: #00f0ff;
                font-weight: bold;
                font-size: 11px;
                border-radius: 6px;
                padding: 7px 12px;
                border: 1px solid #00f0ff;
            }
            QPushButton#reanalyzeBtn:hover {
                background-color: #00f0ff;
                color: #050b14;
                border: 1px solid #38bdf8;
            }
            QTextEdit#drawerOutput {
                background-color: #060c18;
                border: 1px solid #142238;
                border-radius: 6px;
                padding: 10px;
            }
            QPushButton.quickChip {
                background-color: #16243b;
                color: #8ea2c5;
                border: 1px solid #233758;
                border-radius: 4px;
                padding: 4px 8px;
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
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Header bar
        header_layout = QHBoxLayout()
        self.title_label = QLabel("⚡ AI COPILOT ASSISTANT")
        self.title_label.setObjectName("drawerTitle")

        self.status_label = QLabel("● REAL-TIME READY")
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

        # Real-time Live Stream Box
        self.live_stream_box = QFrame()
        self.live_stream_box.setObjectName("liveStreamBox")
        live_box_layout = QHBoxLayout(self.live_stream_box)
        live_box_layout.setContentsMargins(4, 4, 4, 4)
        self.live_stream_label = QLabel("📡 Telemetry: Monitoring live scan events in real time")
        self.live_stream_label.setObjectName("liveStreamLabel")
        self.live_stream_label.setWordWrap(True)
        live_box_layout.addWidget(self.live_stream_label)
        layout.addWidget(self.live_stream_box)

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
        self.output_text.setHtml(format_ai_markdown_html("⚡ **Real-Time AI Copilot Active.** Select any tool or run a scan to see real-time diagnostics."))
        layout.addWidget(self.output_text, 1)

        # Quick action chips
        chips_layout = QHBoxLayout()
        chips_layout.setSpacing(6)

        self.chip_usage = QPushButton("💡 Explain Usage")
        self.chip_usage.setProperty("class", "quickChip")
        self.chip_usage.clicked.connect(self._on_chip_usage_clicked)

        self.chip_flags = QPushButton("🚀 Recommend Flags")
        self.chip_flags.setProperty("class", "quickChip")
        self.chip_flags.clicked.connect(self._on_chip_flags_clicked)

        self.chip_remed = QPushButton("🛡️ Security Fixes")
        self.chip_remed.setProperty("class", "quickChip")
        self.chip_remed.clicked.connect(self._on_chip_remed_clicked)

        self.chip_live = QPushButton("⚡ Live Stream")
        self.chip_live.setProperty("class", "quickChip")
        self.chip_live.clicked.connect(self._on_chip_live_clicked)

        chips_layout.addWidget(self.chip_usage)
        chips_layout.addWidget(self.chip_flags)
        chips_layout.addWidget(self.chip_remed)
        chips_layout.addWidget(self.chip_live)
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

    # =========================================================
    # Real-Time Live Telemetry & Event Hooks
    # =========================================================

    def update_active_context_realtime(self, page_name: str, tool_name: str, inputs_dict: dict):
        """Called dynamically whenever user changes tools or types inputs in real-time."""
        self.active_context = {
            "page_name": page_name,
            "tool_name": tool_name,
            "inputs": inputs_dict or {}
        }
        inputs_str = ", ".join([f"{k}={v}" for k, v in inputs_dict.items()]) if inputs_dict else "Ready"
        self.context_label.setText(f"Active Page: {page_name} | Active Tool: {tool_name}\nInputs: {inputs_str}")

    def handle_live_event(self, event_type: str, detail: str = "", tool_name: str = ""):
        """Invoked in real time whenever an event/port is detected during execution."""
        diag = AICopilot.analyze_realtime_event(event_type, detail=detail, tool_name=tool_name)
        finding_str = f"[{diag['severity']}] {diag['title']}: {diag['summary']}"
        if finding_str not in self.live_findings:
            self.live_findings.append(finding_str)

        self.live_stream_label.setText(f"🔴 Live Finding: {diag['title']} ({diag['severity']}) -> {diag['remediation']}")
        self.live_stream_box.setStyleSheet("background-color: #1a0b18; border: 1px solid #f43f5e; border-radius: 6px; padding: 6px 10px;")

    def handle_live_status(self, status: str, status_type: str):
        """Invoked when command execution status changes in real time."""
        if status_type == "running":
            self._is_scan_running = True
            self.status_label.setText("● SCANNING (LIVE)")
            self.status_label.setStyleSheet("color: #38bdf8; font-size: 10px; font-weight: bold;")
            self.live_stream_label.setText(f"📡 Real-Time Output: {status}")
            self.live_stream_box.setStyleSheet("background-color: #051428; border: 1px solid #00f0ff; border-radius: 6px; padding: 6px 10px;")
        elif status_type == "success":
            self._is_scan_running = False
            self.status_label.setText("● SCAN COMPLETED")
            self.status_label.setStyleSheet("color: #10b981; font-size: 10px; font-weight: bold;")
        else:
            self._is_scan_running = False
            self.status_label.setText("● REAL-TIME READY")
            self.status_label.setStyleSheet("color: #10b981; font-size: 10px; font-weight: bold;")

    def handle_scan_completed(self, tool_name: str, stdout_text: str):
        """Auto-diagnoses completed scan in real time."""
        summary = AICopilot.get_realtime_stream_summary(
            tool_name=tool_name,
            active_ports=app_state.open_ports,
            active_events=app_state.events,
            target=getattr(app_state, "next_target", "") or ""
        )
        self.live_stream_label.setText(f"✅ {tool_name.upper()} scan completed. Telemetry updated.")
        self.live_stream_box.setStyleSheet("background-color: #051a14; border: 1px solid #10b981; border-radius: 6px; padding: 6px 10px;")
        
        # If drawer is open, show fresh live stream summary
        if not self.isHidden() and not self.ai_worker:
            self.output_text.setHtml(format_ai_markdown_html(summary))

    def inspect_and_open(self, custom_ctx=None):
        """Called when user opens AI Copilot from TopBar, shortcut, or in-tool AI Assist button."""
        self.show()
        self.raise_()
        if custom_ctx:
            self.active_context = custom_ctx
            page_name = custom_ctx.get("page_name", "Web")
            tool_name = custom_ctx.get("tool_name", custom_ctx.get("tool_id", page_name))
            inputs_dict = custom_ctx.get("inputs", {})
            inputs_str = ", ".join([f"{k}={v}" for k, v in inputs_dict.items()]) if inputs_dict else "No custom inputs entered"
            self.context_label.setText(f"Active Page: {page_name} | Active Tool: {tool_name}\nInputs: {inputs_str}")
            query = f"Analyze active setup for tool {tool_name} with inputs: {inputs_str}. What are the recommended next steps?"
            self.ask_question(query)
        else:
            self.run_screen_analysis()

    def _on_chip_usage_clicked(self):
        tool_name = self.active_context.get("tool_name", "active tool")
        self.ask_question(f"Explain usage and step-by-step workflow for {tool_name}.")

    def _on_chip_flags_clicked(self):
        tool_name = self.active_context.get("tool_name", "active tool")
        self.ask_question(f"Recommend best execution flags and parameters for {tool_name}.")

    def _on_chip_remed_clicked(self):
        tool_name = self.active_context.get("tool_name", "active tool")
        self.ask_question(f"Provide security remediation and defensive code patches for vulnerabilities associated with {tool_name}.")

    def _on_chip_live_clicked(self):
        tool_name = self.active_context.get("tool_name", "Scanner")
        summary = AICopilot.get_realtime_stream_summary(
            tool_name=tool_name,
            active_ports=app_state.open_ports,
            active_events=app_state.events,
            target=getattr(app_state, "next_target", "") or ""
        )
        self.output_text.setHtml(format_ai_markdown_html(summary))

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
            f"Discovered Events: {app_state.events}",
            f"Active Recommendation: {app_state.suggestion}"
        ]
        context = "\n".join(context_parts)

        self.status_label.setText("● THINKING...")
        self.status_label.setStyleSheet("color: #f59e0b; font-size: 10px; font-weight: bold;")
        self.ask_btn.setEnabled(False)
        self.reanalyze_btn.setEnabled(False)
        self.output_text.setHtml(format_ai_markdown_html(f"🧠 **AI Copilot is analyzing screen context for `{tool_name}`...**"))

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
        self.status_label.setText("● REAL-TIME READY" if not self._is_scan_running else "● SCANNING (LIVE)")
        self.status_label.setStyleSheet("color: #10b981; font-size: 10px; font-weight: bold;")
        self.output_text.setHtml(format_ai_markdown_html(response))
        self.ai_worker = None

    def _on_ai_error(self, err_msg: str):
        self.ask_btn.setEnabled(True)
        self.reanalyze_btn.setEnabled(True)
        self.status_label.setText("● ERROR")
        self.status_label.setStyleSheet("color: #f43f5e; font-size: 10px; font-weight: bold;")
        self.output_text.setHtml(format_ai_markdown_html(f"❌ **AI Copilot Error:** {err_msg}"))
        self.ai_worker = None
