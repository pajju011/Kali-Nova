import os
import unittest

from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication

from ui.recon_page import ReconPage
from ui.network_page import NetworkPage
from ui.web_page import WebPage


os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


class ReconPageUiBehaviorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_get_active_tool_context_harvests_form_inputs(self):
        page = ReconPage()
        page.show()
        page.activate_tool("nmap")
        page.nmap_target.setText("192.168.1.100")
        page.port_input.setText("80,443")

        ctx = page.get_active_tool_context()
        self.assertEqual(ctx["tool_id"], "nmap")
        self.assertIn("192.168.1.100", str(ctx["inputs"]))
        self.assertIn("80,443", str(ctx["inputs"]))

    def test_in_tool_header_ai_assist_emits_signal(self):
        page = ReconPage()
        page.show()
        page.activate_tool("nmap")
        page.nmap_target.setText("10.0.0.1")

        received_ctx = []
        page.ai_assist_requested.connect(lambda ctx: received_ctx.append(ctx))

        page._on_header_ai_assist_clicked()

        self.assertEqual(len(received_ctx), 1)
        self.assertEqual(received_ctx[0]["tool_id"], "nmap")
        self.assertIn("10.0.0.1", str(received_ctx[0]["inputs"]))

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


class NetworkPageSparrowWifiBehaviorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_sparrowwifi_tool_panel_activation(self):
        page = NetworkPage()
        page.show()

        button = page._tool_buttons["sparrowwifi"]
        QTest.mouseClick(button.icon_btn, Qt.MouseButton.LeftButton)
        self.assertEqual(page._selected_tool, "sparrowwifi")

    def test_sparrowwifi_gui_command_generation(self):
        page = NetworkPage()
        page.show()

        commands = []
        page.run_command.connect(lambda cmd: commands.append(cmd))

        page.build_sparrowwifi()

        self.assertEqual(len(commands), 1)
        self.assertEqual(commands[0], "sparrow-wifi")

    def test_sparrowwifi_agent_command_generation(self):
        page = NetworkPage()
        page.show()

        commands = []
        page.run_command.connect(lambda cmd: commands.append(cmd))

        page.sparrow_mode_combo.setCurrentIndex(1)  # Agent Mode
        page.sparrow_port_spin.setValue(9090)
        page.sparrow_allowed_ips_input.setText("192.168.1.10")
        page.sparrow_static_coord_input.setText("40.1,-75.3,150")
        page.sparrow_mavlink_input.setText("sitl")
        page.chk_sparrow_announce.setChecked(True)
        page.chk_sparrow_cors.setChecked(True)

        page.build_sparrowwifi()

        self.assertEqual(len(commands), 1)
        expected_cmd = "sparrowwifiagent --port 9090 --allowedips 192.168.1.10 --staticcoord 40.1,-75.3,150 --mavlinkgps sitl --sendannounce --allowcors"
        self.assertEqual(commands[0], expected_cmd)


class WebPageWhatWebBehaviorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_whatweb_tool_panel_activation(self):
        page = WebPage()
        page.show()

        button = page._tool_buttons["whatweb"]
        QTest.mouseClick(button.icon_btn, Qt.MouseButton.LeftButton)
        self.assertEqual(page._selected_tool, "whatweb")

    def test_whatweb_command_generation_stealthy(self):
        page = WebPage()
        page.show()

        commands = []
        page.run_command.connect(lambda cmd: commands.append(cmd))

        page.whatweb_url.setText("192.168.0.102")
        page.build_whatweb()

        self.assertEqual(len(commands), 1)
        self.assertEqual(commands[0], "whatweb -a 1 -v 192.168.0.102")

    def test_whatweb_command_generation_aggressive(self):
        page = WebPage()
        page.show()

        commands = []
        page.run_command.connect(lambda cmd: commands.append(cmd))

        page.whatweb_url.setText("http://example.com")
        page.whatweb_aggression.setCurrentIndex(1)  # Aggressive (Level 3)
        page.whatweb_user_agent.setText("CustomAgent/1.0")
        page.whatweb_header.setText("Foo:Bar")
        page.whatweb_cookie.setText("session=123")
        page.chk_whatweb_no_errors.setChecked(True)

        page.build_whatweb()

        self.assertEqual(len(commands), 1)
        expected_cmd = 'whatweb -a 3 -U "CustomAgent/1.0" -H "Foo:Bar" -c "session=123" -v --no-errors http://example.com'
        self.assertEqual(commands[0], expected_cmd)

    def test_whatweb_validation_error(self):
        page = WebPage()
        page.show()

        errors = []
        page.validation_error.connect(lambda err: errors.append(err))

        page.build_whatweb()

        self.assertEqual(len(errors), 1)
        self.assertIn("WhatWeb target URL", errors[0])


if __name__ == "__main__":
    unittest.main()




