import os
import unittest

from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication

from ui.recon_page import ReconPage
from ui.network_page import NetworkPage
from ui.auth_page import AuthPage


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

    def test_photon_tool_panel_activation(self):
        page = ReconPage()
        page.show()

        button = page._tool_buttons["photon"]
        QTest.mouseClick(button.icon_btn, Qt.MouseButton.LeftButton)
        self.assertEqual(page._selected_tool, "photon")

    def test_photon_command_generation(self):
        page = ReconPage()
        page.show()

        commands = []
        page.run_command.connect(lambda cmd: commands.append(cmd))

        page.photon_url_input.setText("http://example.com")
        page.photon_level_spin.setValue(3)
        page.chk_photon_dns.setChecked(True)
        page.chk_photon_keys.setChecked(True)

        page.build_photon()

        self.assertEqual(len(commands), 1)
        self.assertEqual(commands[0], "photon -u http://example.com -l 3 --dns --keys")

    def test_photon_validation_error_when_url_missing(self):
        page = ReconPage()
        page.show()

        errors = []
        page.validation_error.connect(lambda err: errors.append(err))

        page.build_photon()

        self.assertEqual(len(errors), 1)
        self.assertIn("Target URL is required", errors[0])

    def test_photon_complex_command_generation(self):
        page = ReconPage()
        page.show()

        commands = []
        page.run_command.connect(lambda cmd: commands.append(cmd))

        page.photon_url_input.setText("https://target.org")
        page.photon_level_spin.setValue(4)
        page.photon_threads_spin.setValue(20)
        page.photon_delay_spin.setValue(2)
        page.photon_output_input.setText("/tmp/photon_out")
        page.photon_regex_input.setText("[a-z0-9_-]+@example\\.com")
        page.photon_cookie_input.setText("sessionid=xyz123")
        page.photon_user_agent_input.setText("Mozilla/5.0")
        page.photon_export_combo.setCurrentIndex(2)  # json
        page.chk_photon_dns.setChecked(True)
        page.chk_photon_keys.setChecked(True)
        page.chk_photon_wayback.setChecked(True)
        page.chk_photon_clone.setChecked(True)
        page.chk_photon_ninja.setChecked(True)

        page.build_photon()

        self.assertEqual(len(commands), 1)
        expected_cmd = "photon -u https://target.org -l 4 -t 20 -d 2 -o /tmp/photon_out -r [a-z0-9_-]+@example\\.com -c sessionid=xyz123 --user-agent Mozilla/5.0 -e json --dns --keys --wayback --clone --ninja"
        self.assertEqual(commands[0], expected_cmd)


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

    def test_ncrack_tool_panel_activation(self):
        page = AuthPage()
        page.show()

        button = page._tool_buttons["ncrack"]
        QTest.mouseClick(button.icon_btn, Qt.MouseButton.LeftButton)
        self.assertEqual(page._selected_tool, "ncrack")

    def test_ncrack_command_generation(self):
        page = AuthPage()
        page.show()

        commands = []
        page.run_command.connect(lambda cmd: commands.append(cmd))

        page.ncrack_target_input.setText("192.168.1.200")
        page.ncrack_service_combo.setCurrentText("rdp")
        page.ncrack_user_input.setText("victim")
        page.ncrack_pass_file.setText("passes.txt")
        page.ncrack_cl_input.setText("1")

        page.build_ncrack()

        self.assertEqual(len(commands), 1)
        self.assertEqual(commands[0], 'ncrack -v --user victim -P "passes.txt" -p rdp CL=1 192.168.1.200')

    def test_ncrack_validation_error(self):
        page = AuthPage()
        page.show()

        errors = []
        page.validation_error.connect(lambda err: errors.append(err))

        page.build_ncrack()

        self.assertEqual(len(errors), 1)
        self.assertIn("target IP / Host is required", errors[0])


if __name__ == "__main__":
    unittest.main()


