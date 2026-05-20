import os
import unittest
from unittest.mock import patch

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication

from ui.main_window import MainWindow


os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


class DummyCommandThread(QObject):
    output_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str, str)
    finished_signal = pyqtSignal()

    def __init__(self, command):
        super().__init__()
        self.command = command
        self._running = True

    def start(self):
        return

    def isRunning(self):
        return self._running

    def stop(self):
        self._running = False

    def wait(self, _timeout):
        return True

    def terminate(self):
        self._running = False


class MainWindowBehaviorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_side_console_hidden_by_default_and_for_validation(self):
        window = MainWindow()
        window.show()

        self.assertTrue(hasattr(window, "side_console"))
        self.assertFalse(window.side_console.isVisible())

        window.handle_validation_error("Example validation message")

        self.assertIn("Example validation message", window.console.status_label.text())
        self.assertFalse(window.side_console.isVisible())

    def test_handle_suggested_tool_opens_gobuster_panel(self):
        window = MainWindow()
        window.show()

        window.handle_suggested_tool("Gobuster")

        current_page = window.workspace.currentWidget()
        web_page = window.workspace.pages["Web"]

        self.assertIs(current_page, web_page)
        self.assertEqual(web_page._selected_tool, "gobuster")

    def test_side_console_stays_visible_after_command_execution(self):
        window = MainWindow()
        window.show()

        self.assertFalse(window.side_console.isVisible())

        with patch("ui.main_window.CommandThread", DummyCommandThread):
            window.execute("echo test")
            self.app.processEvents()

            self.assertTrue(window.side_console.isVisible())
            self.assertEqual(window.side_tabs.count(), 1)

            window.thread.finished_signal.emit()
            self.app.processEvents()

        self.assertTrue(window.side_console.isVisible())

    def test_execute_allows_multiple_simultaneous_runs(self):
        window = MainWindow()
        window.show()

        with patch("ui.main_window.CommandThread") as command_thread_cls:
            first_thread = DummyCommandThread("echo first")
            second_thread = DummyCommandThread("echo second")
            command_thread_cls.side_effect = [first_thread, second_thread]

            window.execute("echo first")
            window.execute("echo second")

        self.assertEqual(command_thread_cls.call_count, 2)
        self.assertEqual(window.side_tabs.count(), 2)
        self.assertEqual(len(window._threads), 2)

    def test_each_tool_tab_remembers_its_own_output(self):
        window = MainWindow()
        window.show()

        with patch("ui.main_window.CommandThread") as command_thread_cls:
            first_thread = DummyCommandThread("nmap localhost")
            second_thread = DummyCommandThread("sqlmap -u http://example.com")
            command_thread_cls.side_effect = [first_thread, second_thread]

            window.execute("nmap localhost")
            first_thread.output_signal.emit("nmap line 1")
            self.app.processEvents()

            window.execute("sqlmap -u http://example.com")
            second_thread.output_signal.emit("sqlmap line 1")
            self.app.processEvents()

        self.assertEqual(window.side_tabs.count(), 2)
        first_tab_console = window.side_tabs.widget(0)
        second_tab_console = window.side_tabs.widget(1)
        self.assertIn("nmap line 1", first_tab_console.output.toPlainText().lower())
        self.assertIn("sqlmap line 1", second_tab_console.output.toPlainText().lower())

    def test_close_event_stops_running_threads_before_exit(self):
        class StoppableThread:
            def __init__(self):
                self.stopped = False
                self.waited = False
                self.terminated = False
                self._running = True

            def isRunning(self):
                return self._running

            def stop(self):
                self.stopped = True
                self._running = False

            def wait(self, _timeout):
                self.waited = True
                return True

            def terminate(self):
                self.terminated = True
                self._running = False

        window = MainWindow()
        window.show()
        stub_thread_1 = StoppableThread()
        stub_thread_2 = StoppableThread()
        window._threads = [stub_thread_1, stub_thread_2]
        window.thread = stub_thread_2

        window.close()
        self.app.processEvents()

        self.assertTrue(stub_thread_1.stopped)
        self.assertTrue(stub_thread_1.waited)
        self.assertTrue(stub_thread_2.stopped)
        self.assertTrue(stub_thread_2.waited)
        self.assertEqual(window._threads, [])

    def test_closeing_a_tab_stops_running_thread(self):
        window = MainWindow()
        window.show()

        with patch("ui.main_window.CommandThread") as command_thread_cls:
            running_thread = DummyCommandThread("echo tab close")
            command_thread_cls.return_value = running_thread
            window.execute("echo test")
            self.assertEqual(window.side_tabs.count(), 1)
            window._close_output_tab(0)
            self.app.processEvents()
            self.assertEqual(window.side_tabs.count(), 0)
            self.assertFalse(window.side_console.isVisible())


if __name__ == "__main__":
    unittest.main()
