import unittest
import os
import sys
from unittest.mock import MagicMock, patch

# Ensure kalinova is in Python path for test execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.executor import CommandThread


class CommandThreadBehaviorTests(unittest.TestCase):
    @patch("core.executor.subprocess.Popen")
    def test_executor_launches_without_shell(self, mock_popen):
        fake_process = MagicMock()
        fake_process.stdout = iter(["mock output\n"])
        fake_process.returncode = 0
        fake_process.wait.return_value = 0
        mock_popen.return_value = fake_process

        thread = CommandThread('sqlmap -u "http://example.com/?id=1" --batch')

        with patch("core.executor.LogManager.log_command"), patch(
            "core.executor.LogManager.log_output"
        ), patch("core.executor.PortParser.extract_ports"), patch(
            "core.executor.RiskEngine.calculate"
        ), patch(
            "core.executor.SuggestionEngine.generate"
        ), patch(
            "core.executor.shutil.which", return_value="sqlmap"
        ):
            thread.run()

        args, kwargs = mock_popen.call_args
        self.assertIsInstance(args[0], list)
        self.assertEqual(args[0][0], "sqlmap")
        self.assertFalse(kwargs.get("shell", True))

    def test_wash_and_reaver_fallback_on_nonzero_exit(self):
        thread = CommandThread("wash -i wlan0mon")
        outputs = []
        statuses = []
        thread.output_signal.connect(lambda s: outputs.append(s))
        thread.status_signal.connect(lambda txt, st: statuses.append((txt, st)))

        fake_process = MagicMock()
        fake_process.stdout = iter(["Error: root required\n"])
        fake_process.returncode = 1
        fake_process.wait.return_value = 1

        with patch("core.executor.subprocess.Popen", return_value=fake_process), patch(
            "core.executor.shutil.which", return_value="/usr/bin/wash"
        ), patch("core.executor.LogManager.log_command"), patch(
            "core.executor.LogManager.log_output"
        ), patch(
            "core.executor.PortParser.extract_ports"
        ), patch(
            "core.executor.RiskEngine.calculate"
        ), patch(
            "core.executor.SuggestionEngine.generate"
        ):
            thread.run()

        self.assertTrue(any("Switching to Simulation Mode" in s for s in outputs))
        self.assertTrue(any("WASH completed" in s[0] and s[1] == "success" for s in statuses))

    def test_photon_simulation_execution(self):
        thread = CommandThread("photon -u http://example.com --dns --keys")
        outputs = []
        statuses = []
        thread.output_signal.connect(lambda s: outputs.append(s))
        thread.status_signal.connect(lambda txt, st: statuses.append((txt, st)))

        with patch("core.executor.shutil.which", return_value=None), patch(
            "core.executor.LogManager.log_command"
        ), patch("core.executor.LogManager.log_output"), patch(
            "core.executor.PortParser.extract_ports"
        ), patch(
            "core.executor.RiskEngine.calculate"
        ), patch(
            "core.executor.SuggestionEngine.generate"
        ):
            thread.run()

        self.assertTrue(any("Root target URL: http://example.com" in s for s in outputs))
        self.assertTrue(any("PHOTON completed" in s[0] and s[1] == "success" for s in statuses))

    def test_photon_events_and_advanced_flags_simulation(self):
        thread = CommandThread("photon -u http://target.local -l 3 -t 15 -o /tmp/out -c session=123 --ninja --wayback --clone")
        outputs = []
        statuses = []
        thread.output_signal.connect(lambda s: outputs.append(s))
        thread.status_signal.connect(lambda txt, st: statuses.append((txt, st)))

        with patch("core.executor.shutil.which", return_value=None), patch(
            "core.executor.LogManager.log_command"
        ), patch("core.executor.LogManager.log_output"), patch(
            "core.executor.PortParser.extract_ports"
        ), patch(
            "core.executor.RiskEngine.calculate"
        ), patch(
            "core.executor.SuggestionEngine.generate"
        ):
            thread.run()

        self.assertTrue(any("level: 3, threads: 15" in s for s in outputs))
        self.assertTrue(any("Stealth/Ninja mode active" in s for s in outputs))
        self.assertTrue(any("Output directory configured: /tmp/out" in s for s in outputs))
        self.assertTrue(any("Secret API key or sensitive token detected" in s for s in outputs))
        self.assertTrue(any("PHOTON completed" in s[0] and s[1] == "success" for s in statuses))


if __name__ == "__main__":
    unittest.main()

