import os
import sys
from pathlib import Path
from datetime import datetime


class _LogManagerMeta(type):
    @property
    def LOG_DIR(cls) -> str:
        return str(cls.get_log_dir())


class LogManager(metaclass=_LogManagerMeta):
    """
    Session Log Manager for Kalinova.
    Persists command history and live console output into user-isolated log directories
    following XDG Base Directory specification on Linux / LOCALAPPDATA on Windows.
    """

    @staticmethod
    def get_log_dir() -> Path:
        """Returns user-writable logs directory adhering to XDG standards or LOCALAPPDATA."""
        env_dir = os.environ.get("KALINOVA_LOG_DIR")
        if env_dir:
            log_dir = Path(env_dir)
        elif os.name == "nt":
            base_dir = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
            log_dir = base_dir / "kalinova" / "logs"
        else:
            base_dir = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
            log_dir = base_dir / "kalinova" / "logs"

        try:
            log_dir.mkdir(parents=True, exist_ok=True)
        except Exception:
            try:
                import tempfile
                log_dir = Path(tempfile.gettempdir()) / "kalinova_logs"
                log_dir.mkdir(parents=True, exist_ok=True)
            except Exception:
                pass

        return log_dir

    @classmethod
    def get_log_file_path(cls) -> Path:
        filename = datetime.now().strftime("%Y-%m-%d_session.txt")
        return cls.get_log_dir() / filename

    @staticmethod
    def initialize():
        try:
            LogManager.get_log_dir()
        except Exception:
            pass

    @classmethod
    def log_command(cls, command: str):
        try:
            file_path = cls.get_log_file_path()
            with open(file_path, "a", encoding="utf-8") as f:
                f.write("\n")
                f.write("=" * 60 + "\n")
                f.write(f"Time: {datetime.now()}\n")
                f.write(f"Command: {command}\n")
                f.write("=" * 60 + "\n")
        except Exception as e:
            # Defensive: logging failure must never crash the application or executor thread
            print(f"[LogManager] Warning: failed to write command log: {e}", file=sys.stderr)

    @classmethod
    def log_output(cls, line: str):
        try:
            file_path = cls.get_log_file_path()
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            # Defensive: logging failure must never crash the application or executor thread
            pass