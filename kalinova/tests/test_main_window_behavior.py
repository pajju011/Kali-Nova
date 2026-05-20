import os
import unittest
from unittest.mock import patch

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication

from ui.main_window import MainWindow


os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


class DummyCommandThread(QObject):
    output_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str, str)
    finished_signal = pyqtSignal()

    def __init__(self, command):
        super().__init__()
        self.command = command

    def start(self):
        return


class MainWindowBehaviorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_side_console_hidden_by_default_and_for_validation(self):
        window = MainWindow()
        window.show()

        self.assertTrue(hasattr(window, "side_console"))
        self.assertFalse(window.side_console.isVisible())

        window.handle_validation_error("Example validation message")

        self.assertIn("Example validation message", window.console.status_label.text())
        self.assertFalse(window.side_console.isVisible())

    def test_handle_suggested_tool_opens_gobuster_panel(self):
        window = MainWindow()
        window.show()

        window.handle_suggested_tool("Gobuster")

        current_page = window.workspace.currentWidget()
        web_page = window.workspace.pages["Web"]

        self.assertIs(current_page, web_page)
        self.assertEqual(web_page._selected_tool, "gobuster")

    def test_side_console_visible_only_during_command_execution(self):
        window = MainWindow()
        window.show()

        self.assertFalse(window.side_console.isVisible())

        with patch("ui.main_window.CommandThread", DummyCommandThread):
            window.execute("echo test")
            self.app.processEvents()

            self.assertTrue(window.side_console.isVisible())

            window.thread.finished_signal.emit()
            self.app.processEvents()

        self.assertFalse(window.side_console.isVisible())


if __name__ == "__main__":
    unittest.main()
