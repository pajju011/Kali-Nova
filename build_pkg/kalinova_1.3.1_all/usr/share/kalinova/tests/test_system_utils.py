import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Ensure kalinova is in Python path for test execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.system_utils import (
    is_root,
    needs_root_privileges,
    wrap_with_privilege_escalation,
    get_network_interfaces,
    get_wireless_interfaces
)


class SystemUtilsTests(unittest.TestCase):

    def test_needs_root_privileges_for_wireless_tools(self):
        self.assertTrue(needs_root_privileges("wifite -i wlan0mon"))
        self.assertTrue(needs_root_privileges("wash -i wlan0mon -C"))
        self.assertTrue(needs_root_privileges("reaver -i wlan0mon -b 00:11:22:33:44:55"))
        self.assertTrue(needs_root_privileges("aircrack-ng hs.cap"))
        self.assertTrue(needs_root_privileges("wireshark"))
        self.assertTrue(needs_root_privileges("tcpdump -i eth0"))

    def test_needs_root_privileges_for_nmap_raw_scans(self):
        self.assertTrue(needs_root_privileges("nmap -sS 192.168.1.1"))
        self.assertTrue(needs_root_privileges("nmap -sU 192.168.1.1"))
        self.assertTrue(needs_root_privileges("nmap -O 192.168.1.1"))
        self.assertTrue(needs_root_privileges("nmap -sN 192.168.1.1"))
        self.assertTrue(needs_root_privileges("nmap -sF 192.168.1.1"))
        self.assertTrue(needs_root_privileges("nmap -sX 192.168.1.1"))
        self.assertFalse(needs_root_privileges("nmap -sV 192.168.1.1"))
        self.assertFalse(needs_root_privileges("whois example.com"))
        self.assertFalse(needs_root_privileges("nikto -h http://example.com"))

    def test_needs_root_privileges_for_privileged_netcat_ports(self):
        self.assertTrue(needs_root_privileges("nc -lvnp 80"))
        self.assertTrue(needs_root_privileges("nc -lvnp 443"))
        self.assertFalse(needs_root_privileges("nc -lvnp 8080"))
        self.assertFalse(needs_root_privileges("nc 192.168.1.1 80"))

    @patch("core.system_utils.is_root", return_value=False)
    @patch("core.system_utils.os.name", "posix")
    def test_wrap_with_privilege_escalation_sudo(self, mock_is_root):
        cmd, elevated = wrap_with_privilege_escalation("wifite -i wlan0mon", method="sudo")
        self.assertTrue(elevated)
        self.assertEqual(cmd, "sudo wifite -i wlan0mon")

    @patch("core.system_utils.is_root", return_value=False)
    @patch("core.system_utils.os.name", "posix")
    @patch("core.system_utils.shutil.which", return_value="/usr/bin/pkexec")
    def test_wrap_with_privilege_escalation_pkexec(self, mock_which, mock_is_root):
        with patch.dict(os.environ, {"DISPLAY": ":0", "XAUTHORITY": "/home/user/.Xauthority"}):
            cmd, elevated = wrap_with_privilege_escalation("wash -i wlan0mon", method="pkexec")
            self.assertTrue(elevated)
            self.assertTrue(cmd.startswith("pkexec env DISPLAY=:0"))

    @patch("core.system_utils.is_root", return_value=False)
    def test_wrap_with_privilege_escalation_disabled(self, mock_is_root):
        cmd, elevated = wrap_with_privilege_escalation("wifite -i wlan0mon", method="none")
        self.assertFalse(elevated)
        self.assertEqual(cmd, "wifite -i wlan0mon")

    @patch("core.system_utils.is_root", return_value=True)
    def test_wrap_when_already_root(self, mock_is_root):
        cmd, elevated = wrap_with_privilege_escalation("wifite -i wlan0mon", method="sudo")
        self.assertFalse(elevated)
        self.assertEqual(cmd, "wifite -i wlan0mon")

    def test_get_wireless_interfaces_returns_list(self):
        interfaces = get_wireless_interfaces()
        self.assertIsInstance(interfaces, list)
        self.assertTrue(len(interfaces) > 0)
        self.assertTrue(any("wlan" in iface.lower() for iface in interfaces))


if __name__ == "__main__":
    unittest.main()
