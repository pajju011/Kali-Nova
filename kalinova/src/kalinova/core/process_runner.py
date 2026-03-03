"""
ProcessRunner — QProcess wrapper for executing CLI tools.

Handles tool execution, output capture, cancellation, and
signal-based communication with the GUI layer. All tools
run as background processes with no visible terminal.
"""

import logging
from typing import Optional

from PyQt6.QtCore import QObject, QProcess, pyqtSignal, QByteArray

from kalinova.core.exceptions import ExecutionError, ToolNotFoundError

logger = logging.getLogger(__name__)


class ProcessRunner(QObject):
    """
    Wraps QProcess to execute CLI tools in the background.

    Signals:
        output_received(str): Emitted when stdout data is available.
        error_received(str): Emitted when stderr data is available.
        process_finished(int, str): Emitted on completion (exit_code, full_output).
        process_error(str): Emitted on process-level error.
        progress_updated(str): Emitted with status messages for the UI.
    """

    output_received = pyqtSignal(str)
    error_received = pyqtSignal(str)
    process_finished = pyqtSignal(int, str)
    process_error = pyqtSignal(str)
    progress_updated = pyqtSignal(str)

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self._process: Optional[QProcess] = None
        self._stdout_buffer: str = ""
        self._stderr_buffer: str = ""
        self._is_running: bool = False

    def start(self, command: list[str]) -> None:
        """
        Start executing a CLI tool.

        Args:
            command: List of command parts, e.g. ["nmap", "-sV", "192.168.1.1"]

        Raises:
            ToolNotFoundError: If the tool binary cannot be found.
            RuntimeError: If a process is already running.
        """
        if self._is_running:
            raise RuntimeError("A process is already running. Cancel it first.")

        if not command:
            raise ValueError("Command list cannot be empty.")

        program = command[0]
        args = command[1:] if len(command) > 1 else []

        logger.info(f"Starting process: {' '.join(command)}")

        # Reset buffers
        self._stdout_buffer = ""
        self._stderr_buffer = ""

        # Create QProcess
        self._process = QProcess(self)
        self._process.setProcessChannelMode(QProcess.ProcessChannelMode.SeparateChannels)

        # Connect signals
        self._process.readyReadStandardOutput.connect(self._on_stdout_ready)
        self._process.readyReadStandardError.connect(self._on_stderr_ready)
        self._process.finished.connect(self._on_finished)
        self._process.errorOccurred.connect(self._on_error)

        self._is_running = True
        self.progress_updated.emit(f"Starting {program}...")

        # Start the process
        self._process.start(program, args)

        if not self._process.waitForStarted(5000):
            self._is_running = False
            error_msg = self._process.errorString()
            if "No such file" in error_msg or "not found" in error_msg.lower():
                raise ToolNotFoundError(program)
            raise ExecutionError(program, -1, error_msg)

    def cancel(self) -> None:
        """Cancel the currently running process."""
        if self._process and self._is_running:
            logger.info("Cancelling process...")
            self.progress_updated.emit("Cancelling...")
            self._process.kill()
            self._process.waitForFinished(3000)
            self._is_running = False
            logger.info("Process cancelled.")

    def is_running(self) -> bool:
        """Check if a process is currently running."""
        return self._is_running

    def get_output(self) -> str:
        """Get accumulated stdout output."""
        return self._stdout_buffer

    def get_errors(self) -> str:
        """Get accumulated stderr output."""
        return self._stderr_buffer

    def _on_stdout_ready(self) -> None:
        """Handle stdout data availability."""
        if self._process:
            data = self._process.readAllStandardOutput()
            text = bytes(data).decode("utf-8", errors="replace")
            self._stdout_buffer += text
            self.output_received.emit(text)

    def _on_stderr_ready(self) -> None:
        """Handle stderr data availability."""
        if self._process:
            data = self._process.readAllStandardError()
            text = bytes(data).decode("utf-8", errors="replace")
            self._stderr_buffer += text
            self.error_received.emit(text)

    def _on_finished(self, exit_code: int, exit_status: QProcess.ExitStatus) -> None:
        """Handle process completion."""
        self._is_running = False

        if exit_status == QProcess.ExitStatus.CrashExit:
            logger.warning(f"Process crashed with exit code {exit_code}")
            self.process_error.emit(f"Process crashed (exit code: {exit_code})")
        else:
            logger.info(f"Process finished with exit code {exit_code}")

        self.progress_updated.emit("Completed.")
        self.process_finished.emit(exit_code, self._stdout_buffer)

    def _on_error(self, error: QProcess.ProcessError) -> None:
        """Handle process-level errors."""
        error_messages = {
            QProcess.ProcessError.FailedToStart: "Failed to start. Is the tool installed?",
            QProcess.ProcessError.Crashed: "Process crashed unexpectedly.",
            QProcess.ProcessError.Timedout: "Process timed out.",
            QProcess.ProcessError.WriteError: "Cannot write to the process.",
            QProcess.ProcessError.ReadError: "Cannot read from the process.",
            QProcess.ProcessError.UnknownError: "An unknown error occurred.",
        }

        msg = error_messages.get(error, "An unknown error occurred.")
        logger.error(f"Process error: {msg}")

        if error == QProcess.ProcessError.FailedToStart:
            self._is_running = False

        self.process_error.emit(msg)

    def cleanup(self) -> None:
        """Clean up the process resources."""
        if self._process:
            if self._is_running:
                self.cancel()
            self._process.deleteLater()
            self._process = None
