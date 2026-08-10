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


class NetworkPageBettercapBehaviorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_bettercap_tool_panel_activation(self):
        page = NetworkPage()
        page.show()

        button = page._tool_buttons["bettercap"]
        QTest.mouseClick(button.icon_btn, Qt.MouseButton.LeftButton)
        self.assertEqual(page._selected_tool, "bettercap")

    def test_bettercap_command_generation(self):
        page = NetworkPage()
        page.show()

        commands = []
        page.run_command.connect(lambda cmd: commands.append(cmd))

        page.bettercap_iface_input.setText("eth0")
        page.bettercap_autostart_input.setText("events.stream")
        page.bettercap_eval_input.setText("net.show")
        page.chk_bettercap_silent.setChecked(True)

        page.build_bettercap()

        self.assertEqual(len(commands), 1)
        self.assertEqual(commands[0], 'bettercap -iface eth0 -autostart events.stream -eval "net.show" -silent')


class AuthPageWordlistsBehaviorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_wordlists_tool_panel_activation(self):
        page = AuthPage()
        page.show()

        button = page._tool_buttons["wordlists"]
        QTest.mouseClick(button.icon_btn, Qt.MouseButton.LeftButton)
        self.assertEqual(page._selected_tool, "wordlists")

    def test_wordlists_command_generation_list(self):
        page = AuthPage()
        page.show()

        commands = []
        page.run_command.connect(lambda cmd: commands.append(cmd))

        page.wordlist_action_combo.setCurrentIndex(0)  # List System Wordlists
        page.wordlist_target_path.setText("/usr/share/wordlists")
        page.build_wordlists()

        self.assertEqual(len(commands), 1)
        self.assertEqual(commands[0], 'ls -lh "/usr/share/wordlists"')

    def test_wordlists_command_generation_decompress(self):
        page = AuthPage()
        page.show()

        commands = []
        page.run_command.connect(lambda cmd: commands.append(cmd))

        page.wordlist_action_combo.setCurrentIndex(1)  # Decompress RockYou (.gz)
        page.wordlist_target_path.setText("/usr/share/wordlists/rockyou.txt.gz")
        page.build_wordlists()

        self.assertEqual(len(commands), 1)
        self.assertEqual(commands[0], 'gunzip -k "/usr/share/wordlists/rockyou.txt.gz"')

    def test_wordlists_command_generation_line_count(self):
        page = AuthPage()
        page.show()

        commands = []
        page.run_command.connect(lambda cmd: commands.append(cmd))

        page.wordlist_action_combo.setCurrentIndex(2)  # Wordlist Info / Line Count
        page.wordlist_target_path.setText("/usr/share/wordlists/rockyou.txt")
        page.build_wordlists()

        self.assertEqual(len(commands), 1)
        self.assertEqual(commands[0], 'wc -l "/usr/share/wordlists/rockyou.txt"')

    def test_wordlists_command_generation_install(self):
        page = AuthPage()
        page.show()

        commands = []
        page.run_command.connect(lambda cmd: commands.append(cmd))

        page.wordlist_action_combo.setCurrentIndex(4)  # Install Wordlists Package
        page.build_wordlists()

        self.assertEqual(len(commands), 1)
        self.assertEqual(commands[0], "sudo apt update && sudo apt install -y wordlists")


class AuthPageHashcatBehaviorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_hashcat_tool_panel_activation(self):
        page = AuthPage()
        page.show()

        button = page._tool_buttons["hashcat"]
        QTest.mouseClick(button.icon_btn, Qt.MouseButton.LeftButton)
        self.assertEqual(page._selected_tool, "hashcat")

    def test_hashcat_command_generation_benchmark(self):
        page = AuthPage()
        page.show()

        commands = []
        page.run_command.connect(lambda cmd: commands.append(cmd))

        page.hashcat_mode_combo.setCurrentIndex(1)  # Benchmark Mode (-b)
        page.chk_hashcat_optimized.setChecked(True)
        page.build_hashcat()

        self.assertEqual(len(commands), 1)
        self.assertEqual(commands[0], "hashcat -b -O")

    def test_hashcat_command_generation_dictionary_attack(self):
        page = AuthPage()
        page.show()

        commands = []
        page.run_command.connect(lambda cmd: commands.append(cmd))

        page.hashcat_hash_input.setText("example500.hash")
        page.hashcat_hash_type_combo.setCurrentText("500 - md5crypt, MD5 (Unix)")
        page.hashcat_wordlist_input.setText("/usr/share/wordlists/sqlmap.txt")
        page.build_hashcat()

        self.assertEqual(len(commands), 1)
        self.assertEqual(commands[0], 'hashcat -a 0 -m 500 "example500.hash" "/usr/share/wordlists/sqlmap.txt"')

    def test_hashcat_command_generation_mask_attack(self):
        page = AuthPage()
        page.show()

        commands = []
        page.run_command.connect(lambda cmd: commands.append(cmd))

        page.hashcat_hash_input.setText("example0.hash")
        page.hashcat_hash_type_combo.setCurrentText("0 - MD5")
        page.hashcat_attack_mode_combo.setCurrentText("3 | Brute-force / Mask")
        page.hashcat_mask_rule_input.setText("?a?a?a?a?a?a")
        page.build_hashcat()

        self.assertEqual(len(commands), 1)
        self.assertEqual(commands[0], 'hashcat -a 3 -m 0 "example0.hash" "?a?a?a?a?a?a"')

    def test_hashcat_validation_error_when_hash_missing(self):
        page = AuthPage()
        page.show()

        errors = []
        page.validation_error.connect(lambda err: errors.append(err))

        page.build_hashcat()

        self.assertEqual(len(errors), 1)
        self.assertIn("Hashcat target hash or hash file is required", errors[0])


if __name__ == "__main__":
    unittest.main()


