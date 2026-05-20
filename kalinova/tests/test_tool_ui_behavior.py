import os
import unittest

from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication

from ui.recon_page import ReconPage


os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


class ReconPageUiBehaviorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_repeated_tool_click_keeps_panel_open(self):
        page = ReconPage()
        page.show()

        button = page._tool_buttons["nmap"]
        QTest.mouseClick(button.icon_btn, Qt.MouseButton.LeftButton)
        self.assertEqual(page._selected_tool, "nmap")
        selected_panel_index = page.panel_stack.currentIndex()

        QTest.mouseClick(button.icon_btn, Qt.MouseButton.LeftButton)

        self.assertEqual(page._selected_tool, "nmap")
        self.assertEqual(page.panel_stack.currentIndex(), selected_panel_index)

    def test_nmap_validation_error_emits_when_target_missing(self):
        page = ReconPage()
        page.show()

        errors = []
        page.validation_error.connect(lambda message: errors.append(message))

        page.build_nmap()

        self.assertEqual(len(errors), 1)
        self.assertIn("target", errors[0].lower())


if __name__ == "__main__":
    unittest.main()
