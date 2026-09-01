"""
System and OS Utilities for Kali-Nova.
Handles privilege management, root/sudo elevation detection, and dynamic network/wireless interface discovery.
"""

import os
import shutil
import shlex
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple, Optional


def is_root() -> bool:
    """Check if the current process is running with root/superuser privileges."""
    if os.name == "nt":
        # On Windows, check for admin token
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False
    else:
        # On Linux/Unix, check UID
        return hasattr(os, "geteuid") and os.geteuid() == 0


def needs_root_privileges(command: str) -> bool:
    """
    Determines whether a given security command requires root/sudo privileges.
    Identifies tools and flags that open raw sockets, put interfaces in monitor mode,
    or perform packet injection.
    """
    if not command:
        return False

    try:
        args = shlex.split(command, posix=os.name != "nt")
    except Exception:
        args = command.split()

    if not args:
        return False

    binary = os.path.basename(args[0]).lower()
    if binary.endswith(".exe"):
        binary = binary[:-4]

    # Tools that unconditionally require root on Linux
    ROOT_REQUIRED_TOOLS = {
        "wifite", "wash", "reaver", "aircrack-ng", "airodump-ng", "aireplay-ng",
        "airmon-ng", "sparrowwifi", "wireshark", "tshark", "tcpdump", "masscan",
        "ettercap", "bettercap", "arp-scan", "hping3", "dsniff", "macchanger",
        "responder", "scapy", "kismet"
    }

    if binary in ROOT_REQUIRED_TOOLS:
        return True

    # Nmap flags requiring root/raw sockets: -sS (SYN), -sU (UDP), -O (OS), -sN, -sF, -sX, -sA, -sW, -sM
    if binary == "nmap":
        raw_socket_flags = {
            "-sS", "-sU", "-O", "-sN", "-sF", "-sX", "-sA", "-sW", "-sM",
            "--traceroute", "-sP", "-sn"
        }
        for arg in args[1:]:
            if arg in raw_socket_flags:
                return True

    # Scapy / Netcat listening on privileged ports (< 1024)
    if binary in {"nc", "netcat", "ncat"}:
        for i, arg in enumerate(args[1:], 1):
            if arg in {"-l", "-lvnp", "-lvn", "-lp", "-p"} and i + 1 < len(args):
                try:
                    port_val = int(args[i + 1])
                    if port_val < 1024:
                        return True
                except ValueError:
                    pass

    return False


def wrap_with_privilege_escalation(
    command: str,
    method: str = "auto",
    explicit_sudo: bool = False
) -> Tuple[str, bool]:
    """
    Wraps a command with privilege escalation (pkexec or sudo) if needed.
    
    Parameters:
        command: Raw CLI command.
        method: 'auto', 'pkexec', 'sudo', or 'none'.
        explicit_sudo: Force elevation regardless of tool heuristics.
        
    Returns:
        (elevated_command_str, was_elevated_bool)
    """
    clean_cmd = command.strip()
    if not clean_cmd:
        return clean_cmd, False

    # Already running as root or escalation disabled
    if is_root() or method == "none":
        return clean_cmd, False

    # Check if command already starts with sudo / pkexec
    if clean_cmd.startswith("sudo ") or clean_cmd.startswith("pkexec "):
        return clean_cmd, False

    # Check if tool requires root or explicitly requested
    requires_root = explicit_sudo or needs_root_privileges(clean_cmd)
    if not requires_root:
        return clean_cmd, False

    # Windows environment: keep original command (handled via UAC or simulation)
    if os.name == "nt":
        return clean_cmd, False

    # Linux / Unix elevation selection
    method_clean = method.lower()

    if method_clean == "pkexec" or (method_clean == "auto" and shutil.which("pkexec") and os.environ.get("DISPLAY")):
        # Use PolicyKit graphical prompt when in desktop GUI environment
        return f"pkexec env DISPLAY={os.environ.get('DISPLAY', ':0')} XAUTHORITY={os.environ.get('XAUTHORITY', '')} {clean_cmd}", True

    # Fallback to sudo (supports -S via interactive stdin or cached credentials)
    return f"sudo {clean_cmd}", True


def get_network_interfaces() -> List[Dict[str, str]]:
    """
    Discovers all active network and wireless interfaces on the system.
    
    Returns:
        List of dicts: [{"name": "wlan0", "type": "wireless", "state": "up"}, ...]
    """
    interfaces = []

    # Linux /sys/class/net inspection
    sys_net = Path("/sys/class/net")
    if sys_net.exists() and sys_net.is_dir():
        try:
            for iface_path in sys_net.iterdir():
                if not iface_path.is_symlink() and not iface_path.is_dir():
                    continue
                iface_name = iface_path.name
                if iface_name == "lo":
                    continue

                is_wireless = (iface_path / "wireless").exists() or (iface_path / "phy80211").exists()
                
                # Check operational state
                operstate = "unknown"
                operstate_file = iface_path / "operstate"
                if operstate_file.exists():
                    try:
                        operstate = operstate_file.read_text(encoding="utf-8").strip()
                    except Exception:
                        pass

                interfaces.append({
                    "name": iface_name,
                    "type": "wireless" if is_wireless else "ethernet",
                    "state": operstate
                })
        except Exception:
            pass

    # Fallback / additional check via iw dev on Linux
    if os.name != "nt" and shutil.which("iw"):
        try:
            result = subprocess.run(["iw", "dev"], capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    line = line.strip()
                    if line.startswith("Interface "):
                        iw_name = line.split()[1]
                        # Ensure interface is in the list
                        if not any(i["name"] == iw_name for i in interfaces):
                            interfaces.append({
                                "name": iw_name,
                                "type": "wireless",
                                "state": "up"
                            })
        except Exception:
            pass

    # Fallback if no interfaces discovered (e.g. running on Windows or restricted container)
    if not interfaces:
        interfaces = [
            {"name": "wlan0mon", "type": "wireless", "state": "monitor"},
            {"name": "wlan0", "type": "wireless", "state": "up"},
            {"name": "eth0", "type": "ethernet", "state": "up"},
        ]

    return interfaces


def get_wireless_interfaces() -> List[str]:
    """
    Returns a sorted list of wireless interface names (e.g., ['wlan0mon', 'wlan0']).
    Prioritizes monitor mode interfaces first.
    """
    all_ifaces = get_network_interfaces()
    wireless_ifaces = [i["name"] for i in all_ifaces if i.get("type") == "wireless"]

    if not wireless_ifaces:
        # Fallback to standard wireless interface names
        wireless_ifaces = ["wlan0mon", "wlan0", "wlan1"]

    # Sort monitor interfaces first
    def sort_key(name: str):
        if "mon" in name.lower():
            return (0, name)
        return (1, name)

    return sorted(list(dict.fromkeys(wireless_ifaces)), key=sort_key)
