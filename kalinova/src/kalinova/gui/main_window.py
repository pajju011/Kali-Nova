"""
MainWindow — Primary application window for Kalinova.

Manages navigation between Dashboard and Tool Windows using
a QStackedWidget. Initializes all shared services.
"""

import logging
from typing import Dict, Optional

from PyQt6.QtWidgets import (
    QMainWindow, QStackedWidget, QWidget, QVBoxLayout,
    QMessageBox, QStatusBar
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

from kalinova.core.tool_registry import ToolRegistry
from kalinova.core.database import Database
from kalinova.ml.predictor import Predictor
from kalinova.gui.dashboard import Dashboard
from kalinova.gui.disclaimer_dialog import DisclaimerDialog
from kalinova.gui.styles import STYLESHEET
from kalinova.gui.tools.nmap_window import NmapWindow
from kalinova.gui.tools.nikto_window import NiktoWindow
from kalinova.gui.tools.john_window import JohnWindow
from kalinova.gui.tools.hydra_window import HydraWindow
from kalinova.gui.tools.base_tool_window import BaseToolWindow

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """
    Primary Kalinova application window.

    Manages:
        - Dashboard display
        - Navigation to/from tool windows
        - Shared service initialization (DB, ML, Registry)
    """

    # Map tool names to their window classes
    TOOL_WINDOWS = {
        "nmap": NmapWindow,
        "nikto": NiktoWindow,
        "john": JohnWindow,
        "hydra": HydraWindow,
    }

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kalinova — Intelligent Security Suite")
        self.setMinimumSize(1100, 750)
        self.setStyleSheet(STYLESHEET)

        # Initialize shared services
        self._registry = ToolRegistry()
        self._db = Database()
        self._predictor = Predictor()
        self._tool_windows: Dict[str, BaseToolWindow] = {}

        # Try loading ML model (non-blocking)
        model_path = "/opt/kalinova/models/next_tool_model.pkl"
        self._predictor.load_model(model_path)

        self._init_ui()
        self._init_menu()
        self._init_statusbar()

    def _init_ui(self):
        """Initialize the main layout with stacked widget."""
        self._stack = QStackedWidget()
        self.setCentralWidget(self._stack)

        # Dashboard (index 0)
        self._dashboard = Dashboard(self._registry)
        self._dashboard.tool_selected.connect(self._on_tool_selected)
        self._stack.addWidget(self._dashboard)

        # Tool windows (lazy-created, added as needed)
        self._stack.setCurrentIndex(0)

    def _init_menu(self):
        """Initialize menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        refresh_action = QAction("Refresh Tools", self)
        refresh_action.triggered.connect(self._refresh_tools)
        file_menu.addAction(refresh_action)

        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View menu
        view_menu = menubar.addMenu("&View")

        dashboard_action = QAction("Dashboard", self)
        dashboard_action.setShortcut("Ctrl+D")
        dashboard_action.triggered.connect(self.show_dashboard)
        view_menu.addAction(dashboard_action)

        # Help menu
        help_menu = menubar.addMenu("&Help")

        about_action = QAction("About Kalinova", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _init_statusbar(self):
        """Initialize status bar."""
        status = QStatusBar()
        self.setStatusBar(status)

        total = self._registry.tool_count
        available = self._registry.available_count
        ml_status = "ML: Active" if self._predictor.is_model_loaded else "ML: Rule-based"

        status.showMessage(
            f"Tools: {available}/{total} available | {ml_status} | "
            f"Ready"
        )

    def _on_tool_selected(self, tool_name: str):
        """Navigate to a tool's GUI window."""
        logger.info(f"Tool selected: {tool_name}")

        # Get or create tool window
        if tool_name not in self._tool_windows:
            window_class = self.TOOL_WINDOWS.get(tool_name)
            if window_class is None:
                QMessageBox.warning(
                    self, "Not Available",
                    f"GUI for '{tool_name}' is not yet implemented."
                )
                return

            tool_info = self._registry.get(tool_name)
            if tool_info is None:
                return

            window = window_class(
                tool_info=tool_info,
                database=self._db,
                predictor=self._predictor,
                parent=self,
            )
            self._tool_windows[tool_name] = window
            self._stack.addWidget(window)

        # Switch to tool window
        self._stack.setCurrentWidget(self._tool_windows[tool_name])

    def show_dashboard(self):
        """Navigate back to the dashboard."""
        self._stack.setCurrentIndex(0)

    def _refresh_tools(self):
        """Refresh tool availability."""
        self._dashboard.refresh()
        self._init_statusbar()

    def _show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About Kalinova",
            "<h2>Kalinova v1.0</h2>"
            "<p>Intelligent GUI Security Suite for Kali Linux</p>"
            "<p>Terminal-free access to security tools with "
            "ML-powered next-step suggestions.</p>"
            "<hr>"
            "<p><b>Architecture:</b> Layered Modular Architecture</p>"
            "<p><b>Stack:</b> Python 3.10+ · PyQt6 · scikit-learn</p>"
            "<p><b>License:</b> MIT</p>"
        )

    def closeEvent(self, event):
        """Clean up on application close."""
        # Cleanup all tool windows
        for window in self._tool_windows.values():
            window.cleanup()

        # Close database
        self._db.close()

        event.accept()
