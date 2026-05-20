import os
import shlex
import subprocess
from PyQt6.QtCore import QThread, pyqtSignal
from datetime import datetime
import time

from core.log_manager import LogManager
from core.port_parser import PortParser
from core.risk_engine import RiskEngine
from core.suggestion_engine import SuggestionEngine
from core.app_state import app_state


class CommandThread(QThread):

    output_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()
    status_signal = pyqtSignal(str, str)  # (status_text, status_type)

    def __init__(self, command):
        super().__init__()
        self.command = command
        self.start_time = None
        self.line_count = 0
        self._process = None
        self._stop_requested = False

    def stop(self):
        self._stop_requested = True
        if self._process is not None and self._process.poll() is None:
            try:
                self._process.terminate()
            except Exception:
                pass

    def run(self):
        try:
            command_args = shlex.split(self.command, posix=os.name != "nt")
            if not command_args:
                raise ValueError("No command provided.")

            # Log command
            LogManager.log_command(self.command)
            self.start_time = time.time()

            # Extract tool name from command
            tool_name = command_args[0].upper()
            self.status_signal.emit(f"Running {tool_name}...", "running")
            self.output_signal.emit(f"\n{'='*60}")
            self.output_signal.emit(f"Starting: {self.command}")
            self.output_signal.emit(f"{'='*60}\n")

            startupinfo = None
            creationflags = 0
            if os.name == "nt":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                creationflags = subprocess.CREATE_NO_WINDOW

            process = subprocess.Popen(
                command_args,
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                startupinfo=startupinfo,
                creationflags=creationflags,
            )
            self._process = process

            for line in process.stdout:
                clean = line.strip()
                if clean:  # Only emit non-empty lines
                    self.output_signal.emit(clean)
                    self.line_count += 1

                LogManager.log_output(clean)
                PortParser.extract_ports(clean)

                # ========================
                # 🔥 EVENT DETECTION
                # ========================

                lower_line = clean.lower()

                # SQL Injection Detection
                if "sql injection" in lower_line:
                    app_state.add_event("SQL_INJECTION")
                    self.output_signal.emit("[ALERT] SQL Injection vulnerability detected!")

                # Hydra / Brute Force Detection
                if "hydra" in lower_line or "login:" in lower_line:
                    app_state.add_event("BRUTE_FORCE")
                    self.output_signal.emit("[ALERT] Brute force attempt detected!")

                # Gobuster Directory Enumeration
                if "found:" in lower_line:
                    app_state.add_event("DIR_ENUM")

                # Email Enumeration (Harvester)
                if "@" in clean and "." in clean and len(clean) > 5:
                    app_state.add_event("EMAIL_ENUM")

            process.wait()
            
            # Calculate execution time
            elapsed_time = time.time() - self.start_time
            
            self.output_signal.emit(f"\n{'='*60}")
            if self._stop_requested:
                self.output_signal.emit("Tool execution stopped by user.")
                self.status_signal.emit(f"{tool_name} stopped", "info")
            elif process.returncode == 0:
                self.output_signal.emit("Tool completed successfully!")
                self.output_signal.emit(f"Execution time: {elapsed_time:.2f}s | Lines: {self.line_count}")
                self.status_signal.emit(f"{tool_name} completed ({elapsed_time:.1f}s)", "success")
            else:
                self.output_signal.emit(f"Tool exited with code: {process.returncode}")
                self.status_signal.emit(f"{tool_name} failed", "error")
            self.output_signal.emit(f"{'='*60}\n")

            # Calculate risk after execution
            RiskEngine.calculate()

            # Generate suggestions
            SuggestionEngine.generate()

        except Exception as e:
            self.output_signal.emit(f"\nERROR: {str(e)}")
            self.status_signal.emit("Error executing tool", "error")
            LogManager.log_output(str(e))
        finally:
            self._process = None

        self.finished_signal.emit()
