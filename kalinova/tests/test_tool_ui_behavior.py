import os
import unittest

from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication

from ui.recon_page import ReconPage
from ui.network_page import NetworkPage


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

    def test_autopsy_tool_panel_activation(self):
        page = ReconPage()
        page.show()

        button = page._tool_buttons["autopsy"]
        QTest.mouseClick(button.icon_btn, Qt.MouseButton.LeftButton)
        self.assertEqual(page._selected_tool, "autopsy")

    def test_autopsy_command_generation(self):
        page = ReconPage()
        page.show()

        commands = []
        page.run_command.connect(lambda cmd: commands.append(cmd))

        page.autopsy_locker_input.setText("/var/lib/evidence")
        page.autopsy_port_spin.setValue(8888)
        page.autopsy_cookie_combo.setCurrentIndex(1)  # Force Cookie (-c)

        page.build_autopsy()

        self.assertEqual(len(commands), 1)
        self.assertEqual(commands[0], "autopsy -c -d /var/lib/evidence -p 8888 localhost")

    def test_autopsy_live_analysis_validation(self):
        page = ReconPage()
        page.show()

        errors = []
        page.validation_error.connect(lambda err: errors.append(err))

        page.chk_live_analysis.setChecked(True)
        page.build_autopsy()

        self.assertEqual(len(errors), 1)
        self.assertIn("Live analysis requires", errors[0])


class NetworkPageWifiteBehaviorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_wifite_tool_panel_activation(self):
        page = NetworkPage()
        page.show()

        button = page._tool_buttons["wifite"]
        QTest.mouseClick(button.icon_btn, Qt.MouseButton.LeftButton)
        self.assertEqual(page._selected_tool, "wifite")

    def test_wifite_command_generation_default_scan(self):
        page = NetworkPage()
        page.show()

        commands = []
        page.run_command.connect(lambda cmd: commands.append(cmd))

        page.wifite_interface_input.setText("wlan0mon")
        page.wifite_channel_input.setText("6")
        page.chk_wpa.setChecked(True)
        page.chk_kill.setChecked(True)

        page.build_wifite()

        self.assertEqual(len(commands), 1)
        self.assertEqual(commands[0], "wifite -i wlan0mon -c 6 --kill --wpa")

    def test_wifite_check_file_validation_error(self):
        page = NetworkPage()
        page.show()

        errors = []
        page.validation_error.connect(lambda err: errors.append(err))

        page.wifite_mode_combo.setCurrentIndex(3)  # Check .cap file
        page.build_wifite()

        self.assertEqual(len(errors), 1)
        self.assertIn(".cap file", errors[0])


class NetworkPageWashAndReaverBehaviorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_wash_tool_panel_activation(self):
        page = NetworkPage()
        page.show()

        button = page._tool_buttons["wash"]
        QTest.mouseClick(button.icon_btn, Qt.MouseButton.LeftButton)
        self.assertEqual(page._selected_tool, "wash")

    def test_wash_command_generation(self):
        page = NetworkPage()
        page.show()

        commands = []
        page.run_command.connect(lambda cmd: commands.append(cmd))

        page.wash_interface_input.setText("wlan0mon")
        page.wash_channel_input.setText("6")
        page.chk_wash_ignore_fcs.setChecked(True)

        page.build_wash()

        self.assertEqual(len(commands), 1)
        self.assertEqual(commands[0], "wash -i wlan0mon -c 6 -C")

    def test_wash_validation_error(self):
        page = NetworkPage()
        page.show()

        errors = []
        page.validation_error.connect(lambda err: errors.append(err))

        page.build_wash()

        self.assertEqual(len(errors), 1)
        self.assertIn("Monitor interface is required", errors[0])

    def test_reaver_tool_panel_activation(self):
        page = NetworkPage()
        page.show()

        button = page._tool_buttons["reaver"]
        QTest.mouseClick(button.icon_btn, Qt.MouseButton.LeftButton)
        self.assertEqual(page._selected_tool, "reaver")

    def test_reaver_command_generation_with_pixie(self):
        page = NetworkPage()
        page.show()

        commands = []
        page.run_command.connect(lambda cmd: commands.append(cmd))

        page.reaver_interface_input.setText("wlan0mon")
        page.reaver_bssid_input.setText("E0:3F:49:6A:57:78")
        page.chk_reaver_pixie.setChecked(True)
        page.chk_reaver_verbose.setChecked(True)

        page.build_reaver()

        self.assertEqual(len(commands), 1)
        self.assertEqual(commands[0], "reaver -i wlan0mon -b E0:3F:49:6A:57:78 -K -v")

    def test_reaver_validation_error(self):
        page = NetworkPage()
        page.show()

        errors = []
        page.validation_error.connect(lambda err: errors.append(err))

        page.reaver_interface_input.setText("wlan0mon")
        page.build_reaver()

        self.assertEqual(len(errors), 1)
        self.assertIn("Target BSSID is required", errors[0])


if __name__ == "__main__":
    unittest.main()


