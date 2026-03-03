"""
CommandBuilder — Constructs CLI command strings from GUI inputs.

Takes structured parameter dictionaries from the GUI layer and
converts them into proper CLI command lists for QProcess execution.
"""

import logging
import shutil
from typing import Optional

from kalinova.core.exceptions import ToolNotFoundError, ValidationError

logger = logging.getLogger(__name__)


class CommandBuilder:
    """
    Builds CLI command lists from structured parameter dictionaries.

    Each tool has a dedicated build method that understands
    the tool's CLI flags and options.
    """

    @staticmethod
    def find_tool_path(tool_name: str) -> str:
        """
        Find the full path of a CLI tool on the system.

        Args:
            tool_name: Name of the tool binary (e.g., "nmap").

        Returns:
            Full path to the tool binary.

        Raises:
            ToolNotFoundError: If the tool is not installed.
        """
        path = shutil.which(tool_name)
        if path is None:
            raise ToolNotFoundError(tool_name)
        return path

    @staticmethod
    def build_nmap(params: dict) -> list[str]:
        """
        Build Nmap command from parameters.

        Expected params:
            target (str): Target IP or hostname (required).
            scan_type (str): "SYN", "TCP", "UDP", "PING" (optional).
            port_range (str): Port range like "1-1000" (optional).
            service_detection (bool): Enable -sV (optional).
            os_detection (bool): Enable -O (optional).
            aggressive (bool): Enable -A (optional).
            timing (int): Timing template 0-5 (optional).
            scripts (str): NSE scripts to run (optional).
            extra_args (str): Additional raw arguments (optional).
        """
        target = params.get("target", "").strip()
        if not target:
            raise ValidationError("target", "Target IP or hostname is required.")

        cmd = ["nmap"]

        # Scan type
        scan_type = params.get("scan_type", "").upper()
        scan_flags = {
            "SYN": "-sS",
            "TCP": "-sT",
            "UDP": "-sU",
            "PING": "-sn",
            "ACK": "-sA",
            "FIN": "-sF",
            "XMAS": "-sX",
            "NULL": "-sN",
        }
        if scan_type and scan_type in scan_flags:
            cmd.append(scan_flags[scan_type])

        # Port range
        port_range = params.get("port_range", "").strip()
        if port_range:
            cmd.extend(["-p", port_range])

        # Service detection
        if params.get("service_detection", False):
            cmd.append("-sV")

        # OS detection
        if params.get("os_detection", False):
            cmd.append("-O")

        # Aggressive scan
        if params.get("aggressive", False):
            cmd.append("-A")

        # Timing template
        timing = params.get("timing")
        if timing is not None and 0 <= int(timing) <= 5:
            cmd.append(f"-T{int(timing)}")

        # NSE scripts
        scripts = params.get("scripts", "").strip()
        if scripts:
            cmd.extend(["--script", scripts])

        # Extra arguments (raw)
        extra = params.get("extra_args", "").strip()
        if extra:
            cmd.extend(extra.split())

        # Target always last
        cmd.append(target)

        logger.info(f"Built Nmap command: {' '.join(cmd)}")
        return cmd

    @staticmethod
    def build_nikto(params: dict) -> list[str]:
        """
        Build Nikto command from parameters.

        Expected params:
            target (str): Target URL or host (required).
            port (int): Port number (optional).
            ssl (bool): Use SSL (optional).
            tuning (str): Tuning options (optional).
            output_format (str): Output format (optional).
            extra_args (str): Additional raw arguments (optional).
        """
        target = params.get("target", "").strip()
        if not target:
            raise ValidationError("target", "Target URL or hostname is required.")

        cmd = ["nikto", "-h", target]

        # Port
        port = params.get("port")
        if port:
            cmd.extend(["-p", str(port)])

        # SSL
        if params.get("ssl", False):
            cmd.append("-ssl")

        # Tuning
        tuning = params.get("tuning", "").strip()
        if tuning:
            cmd.extend(["-Tuning", tuning])

        # Timeout
        timeout = params.get("timeout")
        if timeout:
            cmd.extend(["-timeout", str(timeout)])

        # Extra arguments
        extra = params.get("extra_args", "").strip()
        if extra:
            cmd.extend(extra.split())

        logger.info(f"Built Nikto command: {' '.join(cmd)}")
        return cmd

    @staticmethod
    def build_john(params: dict) -> list[str]:
        """
        Build John the Ripper command from parameters.

        Expected params:
            hash_file (str): Path to hash file (required).
            wordlist (str): Path to wordlist file (optional).
            format (str): Hash format e.g. "raw-md5" (optional).
            rules (str): Rules to apply (optional).
            incremental (bool): Use incremental mode (optional).
            show (bool): Show cracked passwords (optional).
            extra_args (str): Additional raw arguments (optional).
        """
        hash_file = params.get("hash_file", "").strip()
        if not hash_file:
            raise ValidationError("hash_file", "Hash file path is required.")

        # If showing cracked results
        if params.get("show", False):
            cmd = ["john", "--show", hash_file]
            fmt = params.get("format", "").strip()
            if fmt:
                cmd.insert(2, f"--format={fmt}")
            return cmd

        cmd = ["john"]

        # Wordlist
        wordlist = params.get("wordlist", "").strip()
        if wordlist:
            cmd.append(f"--wordlist={wordlist}")

        # Format
        fmt = params.get("format", "").strip()
        if fmt:
            cmd.append(f"--format={fmt}")

        # Rules
        rules = params.get("rules", "").strip()
        if rules:
            cmd.append(f"--rules={rules}")

        # Incremental mode
        if params.get("incremental", False):
            cmd.append("--incremental")

        # Extra arguments
        extra = params.get("extra_args", "").strip()
        if extra:
            cmd.extend(extra.split())

        # Hash file always last
        cmd.append(hash_file)

        logger.info(f"Built John command: {' '.join(cmd)}")
        return cmd

    @staticmethod
    def build_hydra(params: dict) -> list[str]:
        """
        Build Hydra command from parameters.

        Expected params:
            target (str): Target IP or hostname (required).
            service (str): Service to attack e.g. "ssh" (required).
            username (str): Single username (optional if username_file given).
            username_file (str): Path to username list (optional).
            password_file (str): Path to password list (required).
            port (int): Service port (optional).
            threads (int): Number of parallel threads (optional).
            verbose (bool): Enable verbose mode (optional).
            extra_args (str): Additional raw arguments (optional).
        """
        target = params.get("target", "").strip()
        if not target:
            raise ValidationError("target", "Target IP or hostname is required.")

        service = params.get("service", "").strip()
        if not service:
            raise ValidationError("service", "Service type is required (e.g., ssh, ftp).")

        password_file = params.get("password_file", "").strip()
        if not password_file:
            raise ValidationError("password_file", "Password file path is required.")

        cmd = ["hydra"]

        # Username or username file
        username = params.get("username", "").strip()
        username_file = params.get("username_file", "").strip()

        if username_file:
            cmd.extend(["-L", username_file])
        elif username:
            cmd.extend(["-l", username])
        else:
            raise ValidationError("username", "Username or username file is required.")

        # Password file
        cmd.extend(["-P", password_file])

        # Port
        port = params.get("port")
        if port:
            cmd.extend(["-s", str(port)])

        # Threads
        threads = params.get("threads")
        if threads:
            cmd.extend(["-t", str(threads)])

        # Verbose
        if params.get("verbose", False):
            cmd.append("-v")

        # Extra arguments
        extra = params.get("extra_args", "").strip()
        if extra:
            cmd.extend(extra.split())

        # Target and service (hydra format: target service)
        cmd.append(target)
        cmd.append(service)

        logger.info(f"Built Hydra command: {' '.join(cmd)}")
        return cmd

    @classmethod
    def build(cls, tool_name: str, params: dict) -> list[str]:
        """
        Build command for any registered tool by name.

        Args:
            tool_name: Name of the tool (e.g., "nmap").
            params: Parameter dictionary for the tool.

        Returns:
            List of command parts ready for QProcess.
        """
        builders = {
            "nmap": cls.build_nmap,
            "nikto": cls.build_nikto,
            "john": cls.build_john,
            "hydra": cls.build_hydra,
        }

        builder = builders.get(tool_name.lower())
        if builder is None:
            raise ValueError(f"No command builder registered for tool: {tool_name}")

        return builder(params)
