"""
Input validators for Kalinova GUI forms.

Validates user inputs before passing to CommandBuilder.
"""

import re
import os
from kalinova.core.exceptions import ValidationError


def validate_ip(ip: str) -> bool:
    """Validate an IPv4 address."""
    pattern = re.compile(
        r"^(\d{1,3}\.){3}\d{1,3}$"
    )
    if not pattern.match(ip):
        return False
    parts = ip.split(".")
    return all(0 <= int(p) <= 255 for p in parts)


def validate_hostname(hostname: str) -> bool:
    """Validate a hostname."""
    if not hostname or len(hostname) > 255:
        return False
    pattern = re.compile(
        r"^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?"
        r"(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$"
    )
    return bool(pattern.match(hostname))


def validate_target(target: str) -> bool:
    """Validate a scan target (IP, hostname, or CIDR)."""
    target = target.strip()
    if not target:
        return False

    # CIDR notation
    if "/" in target:
        parts = target.split("/")
        if len(parts) == 2:
            return validate_ip(parts[0]) and 0 <= int(parts[1]) <= 32

    # IP or hostname
    return validate_ip(target) or validate_hostname(target)


def validate_port_range(port_range: str) -> bool:
    """Validate a port range like '1-1000' or '22,80,443'."""
    if not port_range:
        return True  # Empty is OK (use default)

    # Single port
    if port_range.isdigit():
        return 1 <= int(port_range) <= 65535

    # Range: "1-1000"
    if "-" in port_range and "," not in port_range:
        parts = port_range.split("-")
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            return 1 <= int(parts[0]) <= int(parts[1]) <= 65535

    # Comma-separated: "22,80,443"
    if "," in port_range:
        ports = port_range.split(",")
        return all(p.strip().isdigit() and 1 <= int(p.strip()) <= 65535 for p in ports)

    return False


def validate_file_path(path: str, must_exist: bool = True) -> bool:
    """Validate a file path."""
    if not path:
        return False
    if must_exist:
        return os.path.isfile(path)
    # Check if directory exists
    return os.path.isdir(os.path.dirname(path) or ".")


def validate_url(url: str) -> bool:
    """Validate a URL (basic)."""
    pattern = re.compile(
        r"^https?://[a-zA-Z0-9][a-zA-Z0-9\-]*(\.[a-zA-Z0-9\-]+)*(:\d+)?(/.*)?$"
    )
    return bool(pattern.match(url))
