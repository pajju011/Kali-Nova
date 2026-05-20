import os
import unittest

from PyQt6.QtWidgets import QApplication

from ui.main_window import MainWindow


os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


class MainWindowBehaviorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_side_console_exists_and_receives_validation_errors(self):
        window = MainWindow()
        window.show()

        self.assertTrue(hasattr(window, "side_console"))

        window.handle_validation_error("Example validation message")

        self.assertIn("Example validation message", window.console.status_label.text())
        self.assertIn(
            "Example validation message",
            window.side_console.status_label.text(),
        )

    def test_handle_suggested_tool_opens_gobuster_panel(self):
        window = MainWindow()
        window.show()

        window.handle_suggested_tool("Gobuster")

        current_page = window.workspace.currentWidget()
        web_page = window.workspace.pages["Web"]

        self.assertIs(current_page, web_page)
        self.assertEqual(web_page._selected_tool, "gobuster")


if __name__ == "__main__":
    unittest.main()
