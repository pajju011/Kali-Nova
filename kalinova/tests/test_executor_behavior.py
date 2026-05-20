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


if __name__ == "__main__":
    unittest.main()
