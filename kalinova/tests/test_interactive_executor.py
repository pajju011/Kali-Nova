import unittest
import os
import sys
from unittest.mock import patch, MagicMock
from PyQt6.QtWidgets import QApplication

# Ensure kalinova is in Python path for test execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Create QApplication instance if not already running for GUI tests
app = QApplication.instance()
if app is None:
    app = QApplication([])

from core.executor import CommandThread
from ui.console import Console
from ui.network_page import InterfaceComboBox


class InteractiveExecutorTests(unittest.TestCase):

    def test_send_input_to_running_process(self):
        thread = CommandThread("mock tool")
        fake_process = MagicMock()
        fake_process.poll.return_value = None  # Process is running
        fake_stdin = MagicMock()
        fake_process.stdin = fake_stdin
        thread._process = fake_process

        outputs = []
        thread.output_signal.connect(lambda msg: outputs.append(msg))

        thread.send_input("Y")

        fake_stdin.write.assert_called_once_with("Y\n")
        fake_stdin.flush.assert_called_once()
        self.assertTrue(any("> [INPUT] Y" in msg for msg in outputs))

    def test_send_input_without_active_process_handles_gracefully(self):
        thread = CommandThread("mock tool")
        thread._process = None

        outputs = []
        thread.output_signal.connect(lambda msg: outputs.append(msg))

        thread.send_input("test input")
        self.assertTrue(any("> [INPUT] test input (No active subprocess)" in msg for msg in outputs))

    def test_console_input_submitted_signal(self):
        console = Console(panel_title="Interactive Console", output_height=None)
        submitted = []
        console.input_submitted.connect(lambda text: submitted.append(text))

        console.input_edit.setText("yes")
        console._handle_send_input()

        self.assertEqual(submitted, ["yes"])
        self.assertEqual(console.input_edit.text(), "")

    def test_interface_combobox_api(self):
        combo = InterfaceComboBox()
        combo.addItems(["wlan0mon", "wlan0", "eth0"])

        # Test backward-compatible setText
        combo.setText("wlan0mon")
        self.assertEqual(combo.text(), "wlan0mon")
        self.assertEqual(combo.currentText(), "wlan0mon")

        # Test custom entry
        combo.setText("custom0")
        self.assertEqual(combo.text(), "custom0")


if __name__ == "__main__":
    unittest.main()
