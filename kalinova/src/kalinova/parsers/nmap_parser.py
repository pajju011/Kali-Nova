"""
NmapParser — Parses Nmap CLI output into structured data.

Handles standard Nmap text output including host discovery,
port scanning, service detection, and OS detection results.
"""

import re
import logging
from typing import List

from kalinova.parsers.base_parser import BaseParser, Finding
from kalinova.core.exceptions import ParsingError

logger = logging.getLogger(__name__)


class NmapParser(BaseParser):
    """Parser for Nmap scan output."""

    def parse(self, raw_output: str) -> dict:
        """
        Parse Nmap output into structured dictionary.

        Returns:
            {
                "target": str,
                "scan_type": str,
                "hosts": [
                    {
                        "ip": str,
                        "hostname": str,
                        "status": str,
                        "ports": [
                            {
                                "port": int,
                                "protocol": str,
                                "state": str,
                                "service": str,
                                "version": str
                            }
                        ],
                        "os": str
                    }
                ],
                "open_ports": int,
                "closed_ports": int,
                "filtered_ports": int,
                "total_hosts_up": int,
                "scan_time": str,
                "raw_output": str
            }
        """
        if self.is_empty_output(raw_output):
            return self._empty_result(raw_output)

        result = {
            "target": "",
            "scan_type": "",
            "hosts": [],
            "open_ports": 0,
            "closed_ports": 0,
            "filtered_ports": 0,
            "total_hosts_up": 0,
            "scan_time": "",
            "raw_output": raw_output,
        }

        try:
            result["target"] = self._extract_target(raw_output)
            result["scan_type"] = self._extract_scan_type(raw_output)
            result["hosts"] = self._extract_hosts(raw_output)
            result["scan_time"] = self._extract_scan_time(raw_output)

            # Calculate totals
            for host in result["hosts"]:
                if host["status"] == "up":
                    result["total_hosts_up"] += 1
                for port in host["ports"]:
                    if port["state"] == "open":
                        result["open_ports"] += 1
                    elif port["state"] == "closed":
                        result["closed_ports"] += 1
                    elif port["state"] == "filtered":
                        result["filtered_ports"] += 1

        except Exception as e:
            logger.warning(f"Nmap parsing encountered issues: {e}")
            # Return partial results rather than failing completely
            if not result["hosts"]:
                result["hosts"] = self._fallback_port_parse(raw_output)
                for host in result["hosts"]:
                    for port in host.get("ports", []):
                        if port["state"] == "open":
                            result["open_ports"] += 1

        return result

    def get_findings(self, parsed_data: dict) -> List[Finding]:
        """Extract security findings from parsed Nmap data."""
        findings = []

        for host in parsed_data.get("hosts", []):
            for port in host.get("ports", []):
                if port["state"] != "open":
                    continue

                severity = self._classify_port_risk(port)
                explanation = self._explain_port(port)

                findings.append(Finding(
                    description=(
                        f"Port {port['port']}/{port['protocol']} is open — "
                        f"Service: {port['service']}"
                        + (f" ({port['version']})" if port.get("version") else "")
                    ),
                    severity=severity,
                    category="open_port",
                    details={
                        "port": port["port"],
                        "protocol": port["protocol"],
                        "service": port["service"],
                        "version": port.get("version", ""),
                        "host": host.get("ip", ""),
                    },
                    explanation=explanation,
                ))

        # Sort by severity
        findings.sort(key=lambda f: f.severity_order)
        return findings

    # ---------- Private extraction methods ----------

    def _extract_target(self, output: str) -> str:
        """Extract the scan target from Nmap output."""
        # "Nmap scan report for 192.168.1.1"
        match = re.search(r"Nmap scan report for (.+)", output)
        if match:
            return match.group(1).strip()
        # "Starting Nmap ... scan initiated ... against 192.168.1.1"
        match = re.search(r"against\s+(\S+)", output)
        if match:
            return match.group(1)
        return ""

    def _extract_scan_type(self, output: str) -> str:
        """Extract scan type from Nmap output."""
        scan_types = {
            "SYN Stealth Scan": "SYN",
            "Connect Scan": "TCP",
            "UDP Scan": "UDP",
            "Ping Scan": "PING",
            "ACK Scan": "ACK",
            "FIN Scan": "FIN",
        }
        for pattern, stype in scan_types.items():
            if pattern in output:
                return stype
        return "Unknown"

    def _extract_hosts(self, output: str) -> list:
        """Extract host information including ports."""
        hosts = []

        # Split by host sections
        host_sections = re.split(r"Nmap scan report for", output)

        for section in host_sections[1:]:  # Skip text before first host
            host = {
                "ip": "",
                "hostname": "",
                "status": "up",
                "ports": [],
                "os": "",
            }

            # Extract IP and hostname
            # "hostname (192.168.1.1)" or just "192.168.1.1"
            header = section.split("\n")[0].strip()
            ip_match = re.search(r"(\d+\.\d+\.\d+\.\d+)", header)
            if ip_match:
                host["ip"] = ip_match.group(1)
                # Check for hostname before IP
                hostname_match = re.match(r"(.+?)\s*\(", header)
                if hostname_match:
                    host["hostname"] = hostname_match.group(1).strip()
            else:
                host["ip"] = header.strip()

            # Check host status
            if "Host is up" not in section and "host up" not in section.lower():
                if "Host seems down" in section:
                    host["status"] = "down"
                    hosts.append(host)
                    continue

            # Extract ports
            # Pattern: "22/tcp   open  ssh     OpenSSH 8.9p1"
            port_pattern = re.compile(
                r"(\d+)/(tcp|udp)\s+(open|closed|filtered)\s+(\S+)\s*(.*)"
            )
            for match in port_pattern.finditer(section):
                port_info = {
                    "port": int(match.group(1)),
                    "protocol": match.group(2),
                    "state": match.group(3),
                    "service": match.group(4),
                    "version": match.group(5).strip() if match.group(5) else "",
                }
                host["ports"].append(port_info)

            # Extract OS
            os_match = re.search(r"OS details?:\s*(.+)", section)
            if os_match:
                host["os"] = os_match.group(1).strip()
            else:
                os_match = re.search(r"Running:\s*(.+)", section)
                if os_match:
                    host["os"] = os_match.group(1).strip()

            hosts.append(host)

        return hosts

    def _extract_scan_time(self, output: str) -> str:
        """Extract total scan time."""
        match = re.search(r"Nmap done.*in\s+([\d.]+)\s+seconds", output)
        if match:
            return f"{match.group(1)}s"
        return ""

    def _fallback_port_parse(self, output: str) -> list:
        """Fallback parser for non-standard Nmap output."""
        host = {
            "ip": "",
            "hostname": "",
            "status": "up",
            "ports": [],
            "os": "",
        }

        port_pattern = re.compile(
            r"(\d+)/(tcp|udp)\s+(open|closed|filtered)\s+(\S+)"
        )
        for match in port_pattern.finditer(output):
            host["ports"].append({
                "port": int(match.group(1)),
                "protocol": match.group(2),
                "state": match.group(3),
                "service": match.group(4),
                "version": "",
            })

        return [host] if host["ports"] else []

    def _classify_port_risk(self, port: dict) -> str:
        """Classify risk level of an open port."""
        port_num = port.get("port", 0)
        service = port.get("service", "").lower()

        # High risk services
        high_risk = {"telnet", "ftp", "rlogin", "rsh", "rexec"}
        if service in high_risk:
            return "high"

        # Medium risk — common attack surfaces
        medium_risk = {"ssh", "rdp", "smb", "mysql", "mssql", "postgresql",
                       "vnc", "snmp", "smtp"}
        if service in medium_risk or port_num in (22, 3389, 445, 3306, 1433, 5432):
            return "medium"

        # Web services — info level
        if service in ("http", "https") or port_num in (80, 443, 8080, 8443):
            return "info"

        return "low"

    def _explain_port(self, port: dict) -> str:
        """Generate beginner-friendly explanation for a port finding."""
        service = port.get("service", "").lower()
        port_num = port.get("port", 0)

        explanations = {
            "ssh": (
                f"Port {port_num} (SSH) is open. SSH allows remote login to this "
                "machine. An attacker could try brute-forcing the login credentials."
            ),
            "http": (
                f"Port {port_num} (HTTP) is open. A web server is running here. "
                "It could have vulnerabilities — consider running Nikto for a detailed scan."
            ),
            "https": (
                f"Port {port_num} (HTTPS) is open. A secure web server is running. "
                "SSL certificate issues or web app vulnerabilities may still exist."
            ),
            "ftp": (
                f"Port {port_num} (FTP) is open. FTP is an old file transfer protocol "
                "that often transmits credentials in plaintext. Check for anonymous login."
            ),
            "telnet": (
                f"Port {port_num} (Telnet) is open. Telnet is insecure — all data "
                "including passwords is sent in plaintext. This is a high-risk finding."
            ),
            "smb": (
                f"Port {port_num} (SMB) is open. Windows file sharing service. "
                "SMB has had critical vulnerabilities like EternalBlue."
            ),
            "mysql": (
                f"Port {port_num} (MySQL) is open. A database is exposed to the "
                "network. Check if it requires authentication."
            ),
            "rdp": (
                f"Port {port_num} (RDP) is open. Remote Desktop Protocol allows "
                "graphical remote access. Could be targeted for brute-force attacks."
            ),
        }

        # Map common port numbers to service names
        port_to_service = {
            22: "ssh", 80: "http", 443: "https", 21: "ftp",
            23: "telnet", 445: "smb", 3306: "mysql", 3389: "rdp",
        }

        key = service if service in explanations else port_to_service.get(port_num, "")

        if key in explanations:
            return explanations[key]

        return (
            f"Port {port_num} ({service or 'unknown'}) is open. "
            "An open port means a service is listening and potentially accessible."
        )

    def _empty_result(self, raw_output: str) -> dict:
        """Return empty result structure."""
        return {
            "target": "",
            "scan_type": "",
            "hosts": [],
            "open_ports": 0,
            "closed_ports": 0,
            "filtered_ports": 0,
            "total_hosts_up": 0,
            "scan_time": "",
            "raw_output": raw_output or "",
        }
