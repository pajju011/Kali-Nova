"""
BaseToolWindow — Abstract base for all tool GUI windows.

Provides common layout structure, input validation,
process execution, output display, and ML suggestion
panel. All specific tool GUIs extend this class.
"""

import logging
from datetime import datetime
from typing import Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QGroupBox, QFormLayout, QProgressBar,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QFileDialog, QSplitter, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor

from kalinova.core.process_runner import ProcessRunner
from kalinova.core.command_builder import CommandBuilder
from kalinova.core.tool_registry import ToolInfo
from kalinova.core.database import Database
from kalinova.parsers.base_parser import BaseParser, Finding
from kalinova.handlers.type_handler import TypeHandler, ScanResult
from kalinova.ml.feature_extractor import FeatureExtractor
from kalinova.ml.predictor import Predictor
from kalinova.reporting.report_generator import ReportGenerator

logger = logging.getLogger(__name__)


class BaseToolWindow(QWidget):
    """
    Abstract base class for all tool GUI windows.

    Subclasses must implement:
        - _build_input_form() -> QGroupBox
        - _collect_params() -> dict
        - _get_parser() -> BaseParser
    """

    def __init__(
        self,
        tool_info: ToolInfo,
        database: Database,
        predictor: Predictor,
        parent=None,
    ):
        super().__init__(parent)
        self._tool_info = tool_info
        self._db = database
        self._predictor = predictor
        self._runner = ProcessRunner(self)
        self._feature_extractor = FeatureExtractor()
        self._report_gen = ReportGenerator()
        self._started_at: Optional[datetime] = None
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        """Build the complete tool window layout."""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header = self._build_header()
        main_layout.addWidget(header)

        # Splitter: input/output
        splitter = QSplitter(Qt.Orientation.Vertical)

        # Top section: input form
        input_group = self._build_input_form()
        splitter.addWidget(input_group)

        # Bottom section: results area
        results_widget = self._build_results_area()
        splitter.addWidget(results_widget)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)

        main_layout.addWidget(splitter)

        # Action buttons
        actions = self._build_action_bar()
        main_layout.addLayout(actions)

    def _build_header(self) -> QWidget:
        """Build the tool header with name and description."""
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a1a2e, stop:1 #16213e);
                border: 1px solid #0f3460;
                border-radius: 12px;
                padding: 16px;
            }
        """)
        layout = QVBoxLayout(header)
        layout.setSpacing(6)

        title = QLabel(f"🛡️ {self._tool_info.display_name}")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #00d4ff; background: transparent;")
        layout.addWidget(title)

        desc = QLabel(self._tool_info.description)
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #8899aa; font-size: 13px; background: transparent;")
        layout.addWidget(desc)

        # Type badge
        type_label = QLabel(f"Type: {self._tool_info.tool_type.upper()}")
        type_label.setStyleSheet(
            "color: #00d4ff; font-size: 12px; font-weight: bold; background: transparent;"
        )
        layout.addWidget(type_label)

        return header

    def _build_input_form(self) -> QGroupBox:
        """Override in subclasses — build tool-specific input form."""
        group = QGroupBox("Configuration")
        layout = QFormLayout(group)
        layout.addRow(QLabel("(No parameters)"))
        return group

    def _build_results_area(self) -> QWidget:
        """Build the results display area."""
        results = QWidget()
        layout = QVBoxLayout(results)
        layout.setSpacing(8)

        # Status bar
        status_layout = QHBoxLayout()

        self._status_label = QLabel("Ready")
        self._status_label.setStyleSheet(
            "color: #8899aa; font-size: 13px; font-weight: bold;"
        )
        status_layout.addWidget(self._status_label)

        status_layout.addStretch()

        self._progress_bar = QProgressBar()
        self._progress_bar.setRange(0, 0)  # Indeterminate
        self._progress_bar.setVisible(False)
        self._progress_bar.setMaximumWidth(200)
        status_layout.addWidget(self._progress_bar)

        layout.addLayout(status_layout)

        # Findings table
        self._findings_table = QTableWidget()
        self._findings_table.setColumnCount(4)
        self._findings_table.setHorizontalHeaderLabels(
            ["Severity", "Category", "Description", "Explanation"]
        )
        header = self._findings_table.horizontalHeader()
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self._findings_table.setVisible(False)
        layout.addWidget(self._findings_table)

        # ML Suggestion panel
        self._suggestion_frame = QFrame()
        self._suggestion_frame.setStyleSheet("""
            QFrame {
                background-color: #0f3460;
                border: 1px solid #1a5a9e;
                border-radius: 10px;
                padding: 16px;
            }
        """)
        suggestion_layout = QVBoxLayout(self._suggestion_frame)

        self._suggestion_title = QLabel("🤖 ML Suggestion")
        self._suggestion_title.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: #00d4ff; background: transparent;"
        )
        suggestion_layout.addWidget(self._suggestion_title)

        self._suggestion_text = QLabel("")
        self._suggestion_text.setWordWrap(True)
        self._suggestion_text.setStyleSheet(
            "font-size: 14px; color: #e0e0e0; background: transparent;"
        )
        suggestion_layout.addWidget(self._suggestion_text)

        self._confidence_label = QLabel("")
        self._confidence_label.setStyleSheet(
            "font-size: 13px; color: #8899aa; background: transparent;"
        )
        suggestion_layout.addWidget(self._confidence_label)

        self._suggestion_frame.setVisible(False)
        layout.addWidget(self._suggestion_frame)

        # Raw output
        self._raw_output = QTextEdit()
        self._raw_output.setReadOnly(True)
        self._raw_output.setPlaceholderText("Tool output will appear here...")
        self._raw_output.setMaximumHeight(200)
        self._raw_output.setStyleSheet("""
            QTextEdit {
                font-family: 'Courier New', 'Monospace', monospace;
                font-size: 12px;
                background-color: #0a0a14;
                border: 1px solid #2a2a4e;
                border-radius: 8px;
            }
        """)
        layout.addWidget(self._raw_output)

        return results

    def _build_action_bar(self) -> QHBoxLayout:
        """Build the action buttons bar."""
        layout = QHBoxLayout()

        self._run_btn = QPushButton("▶  Run Scan")
        self._run_btn.setObjectName("primary")
        self._run_btn.setMinimumHeight(44)
        self._run_btn.setMinimumWidth(160)
        self._run_btn.clicked.connect(self._on_run_clicked)
        layout.addWidget(self._run_btn)

        self._cancel_btn = QPushButton("⏹  Cancel")
        self._cancel_btn.setObjectName("danger")
        self._cancel_btn.setMinimumHeight(44)
        self._cancel_btn.setEnabled(False)
        self._cancel_btn.clicked.connect(self._on_cancel_clicked)
        layout.addWidget(self._cancel_btn)

        layout.addStretch()

        self._export_btn = QPushButton("📄  Export Report")
        self._export_btn.setObjectName("success")
        self._export_btn.setMinimumHeight(44)
        self._export_btn.setEnabled(False)
        self._export_btn.setVisible(self._tool_info.report_enabled)
        self._export_btn.clicked.connect(self._on_export_clicked)
        layout.addWidget(self._export_btn)

        self._back_btn = QPushButton("← Back to Dashboard")
        self._back_btn.setMinimumHeight(44)
        self._back_btn.clicked.connect(self._on_back_clicked)
        layout.addWidget(self._back_btn)

        return layout

    def _connect_signals(self):
        """Connect ProcessRunner signals."""
        self._runner.output_received.connect(self._on_output_received)
        self._runner.error_received.connect(self._on_error_received)
        self._runner.process_finished.connect(self._on_process_finished)
        self._runner.process_error.connect(self._on_process_error)
        self._runner.progress_updated.connect(self._on_progress_updated)

    # ---------- Subclass hooks ----------

    def _collect_params(self) -> dict:
        """Override to collect parameters from form inputs."""
        return {}

    def _get_parser(self) -> BaseParser:
        """Override to return the tool-specific parser."""
        raise NotImplementedError("Subclass must implement _get_parser()")

    # ---------- Action handlers ----------

    def _on_run_clicked(self):
        """Execute the tool."""
        try:
            params = self._collect_params()
            command = CommandBuilder.build(self._tool_info.name, params)

            self._started_at = datetime.now()
            self._set_running_state(True)
            self._raw_output.clear()
            self._findings_table.setRowCount(0)
            self._findings_table.setVisible(False)
            self._suggestion_frame.setVisible(False)
            self._export_btn.setEnabled(False)

            self._runner.start(command)

        except Exception as e:
            self._status_label.setText(f"Error: {str(e)}")
            self._status_label.setStyleSheet(
                "color: #ff4757; font-size: 13px; font-weight: bold;"
            )
            logger.error(f"Failed to start {self._tool_info.name}: {e}")

    def _on_cancel_clicked(self):
        """Cancel running tool."""
        self._runner.cancel()
        self._set_running_state(False)
        self._status_label.setText("Cancelled")

    def _on_export_clicked(self):
        """Export HTML report."""
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Save Report", f"kalinova_report_{self._tool_info.name}.html",
            "HTML Files (*.html)"
        )
        if filepath and hasattr(self, "_last_result"):
            handler_result = self._last_handler_result
            html = self._report_gen.generate(
                tool_name=self._tool_info.name,
                target=self._last_result.target,
                findings=self._last_result.findings,
                parsed_data=self._last_result.parsed_data,
                severity_counts=handler_result.get("severity_counts", {}),
                raw_output=self._last_result.raw_output,
                duration=str(self._last_result.duration_ms) + "ms",
            )
            saved_path = self._report_gen.save(html, filepath)
            self._status_label.setText(f"Report saved: {saved_path}")

    def _on_back_clicked(self):
        """Go back to dashboard."""
        # Navigate to parent (Dashboard will handle this)
        parent = self.parent()
        if parent and hasattr(parent, "show_dashboard"):
            parent.show_dashboard()

    # ---------- Signal handlers ----------

    def _on_output_received(self, text: str):
        """Append real-time stdout to output area."""
        self._raw_output.insertPlainText(text)
        # Auto-scroll
        cursor = self._raw_output.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self._raw_output.setTextCursor(cursor)

    def _on_error_received(self, text: str):
        """Append stderr to output area."""
        self._raw_output.insertPlainText(f"[STDERR] {text}")

    def _on_process_finished(self, exit_code: int, full_output: str):
        """Handle tool completion — parse, display, suggest."""
        completed_at = datetime.now()
        duration_ms = int(
            (completed_at - self._started_at).total_seconds() * 1000
        ) if self._started_at else 0

        self._set_running_state(False)

        try:
            # Parse output
            parser = self._get_parser()
            parsed_data = parser.parse(full_output)
            findings = parser.get_findings(parsed_data)

            # Create ScanResult
            scan_result = ScanResult(
                tool_name=self._tool_info.name,
                tool_type=self._tool_info.tool_type,
                target=parsed_data.get("target", ""),
                status="completed" if exit_code == 0 else "error",
                exit_code=exit_code,
                raw_output=full_output,
                parsed_data=parsed_data,
                findings=findings,
                started_at=self._started_at or datetime.now(),
                completed_at=completed_at,
                duration_ms=duration_ms,
                ml_enabled=self._tool_info.ml_enabled,
                report_enabled=self._tool_info.report_enabled,
            )

            # Route through TypeHandler
            handler_result = TypeHandler.process(scan_result)

            # Store for export
            self._last_result = scan_result
            self._last_handler_result = handler_result

            # Display findings
            self._display_findings(findings)

            # ML suggestion (if assessment tool)
            if handler_result.get("show_ml_suggestion"):
                self._show_ml_suggestion(parsed_data)

            # Enable export
            if handler_result.get("enable_report_export"):
                self._export_btn.setEnabled(True)

            # Save to database
            self._save_to_db(scan_result, findings)

            # Update status
            self._status_label.setText(handler_result.get("summary", "Completed"))
            self._status_label.setStyleSheet(
                "color: #2ed573; font-size: 13px; font-weight: bold;"
            )

        except Exception as e:
            self._status_label.setText(f"Parse error: {str(e)}")
            self._status_label.setStyleSheet(
                "color: #ffa502; font-size: 13px; font-weight: bold;"
            )
            logger.error(f"Error processing results: {e}")

    def _on_process_error(self, error_msg: str):
        """Handle process-level errors."""
        self._set_running_state(False)
        self._status_label.setText(f"Error: {error_msg}")
        self._status_label.setStyleSheet(
            "color: #ff4757; font-size: 13px; font-weight: bold;"
        )

    def _on_progress_updated(self, message: str):
        """Update progress status."""
        self._status_label.setText(message)

    # ---------- Display methods ----------

    def _display_findings(self, findings: list):
        """Display findings in the table."""
        if not findings:
            return

        self._findings_table.setVisible(True)
        self._findings_table.setRowCount(len(findings))

        severity_colors = {
            "critical": "#ff4757",
            "high": "#ff6b6b",
            "medium": "#ffa502",
            "low": "#2ed573",
            "info": "#1e90ff",
        }

        for row, finding in enumerate(findings):
            # Severity
            sev_item = QTableWidgetItem(finding.severity.upper())
            sev_item.setForeground(QColor(
                severity_colors.get(finding.severity, "#e0e0e0")
            ))
            sev_item.setFont(QFont("", -1, QFont.Weight.Bold))
            self._findings_table.setItem(row, 0, sev_item)

            # Category
            self._findings_table.setItem(
                row, 1, QTableWidgetItem(finding.category)
            )

            # Description
            self._findings_table.setItem(
                row, 2, QTableWidgetItem(finding.description)
            )

            # Explanation
            self._findings_table.setItem(
                row, 3, QTableWidgetItem(finding.explanation)
            )

    def _show_ml_suggestion(self, parsed_data: dict):
        """Display ML prediction panel."""
        features = self._feature_extractor.extract(
            self._tool_info.name, parsed_data
        )
        if not features:
            return

        prediction = self._predictor.predict(features, self._tool_info.name)

        if prediction.recommended_tool:
            self._suggestion_frame.setVisible(True)
            self._suggestion_text.setText(
                f"Recommended next tool: <b>{prediction.recommended_tool.upper()}</b>"
                f"<br>{prediction.reasoning}"
            )

            # Confidence color coding
            color_map = {"high": "#2ed573", "medium": "#ffa502", "low": "#ff6b6b"}
            confidence_color = color_map.get(prediction.confidence_label, "#8899aa")

            self._confidence_label.setText(
                f"Confidence: {prediction.confidence:.0%} "
                f"({prediction.confidence_label})"
            )
            self._confidence_label.setStyleSheet(
                f"font-size: 13px; color: {confidence_color}; "
                f"font-weight: bold; background: transparent;"
            )

    # ---------- State management ----------

    def _set_running_state(self, running: bool):
        """Update UI state for running/idle."""
        self._run_btn.setEnabled(not running)
        self._cancel_btn.setEnabled(running)
        self._progress_bar.setVisible(running)

        if running:
            self._status_label.setText("Running...")
            self._status_label.setStyleSheet(
                "color: #00d4ff; font-size: 13px; font-weight: bold;"
            )

    def _save_to_db(self, scan_result: ScanResult, findings: list):
        """Persist scan results to database."""
        try:
            scan_id = self._db.save_scan(
                tool_name=scan_result.tool_name,
                tool_type=scan_result.tool_type,
                target=scan_result.target,
                parameters={},
                status=scan_result.status,
                exit_code=scan_result.exit_code,
                raw_output=scan_result.raw_output,
                parsed_data=scan_result.parsed_data,
                started_at=scan_result.started_at,
                completed_at=scan_result.completed_at,
                duration_ms=scan_result.duration_ms,
            )
            self._db.save_findings(scan_id, findings)
        except Exception as e:
            logger.error(f"Failed to save to database: {e}")

    def cleanup(self):
        """Clean up resources."""
        self._runner.cleanup()
