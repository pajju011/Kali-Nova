"""
NiktoParser — Parses Nikto CLI output into structured data.

Handles standard Nikto text output including vulnerability
findings, server information, and test results.
"""

import re
import logging
from typing import List

from kalinova.parsers.base_parser import BaseParser, Finding
from kalinova.core.exceptions import ParsingError

logger = logging.getLogger(__name__)


class NiktoParser(BaseParser):
    """Parser for Nikto web vulnerability scan output."""

    def parse(self, raw_output: str) -> dict:
        """
        Parse Nikto output into structured dictionary.

        Returns:
            {
                "target": str,
                "target_ip": str,
                "port": int,
                "server": str,
                "vulnerabilities": [
                    {
                        "id": str,
                        "method": str,
                        "uri": str,
                        "description": str
                    }
                ],
                "total_vulns": int,
                "total_items_tested": int,
                "total_errors": int,
                "scan_time": str,
                "raw_output": str
            }
        """
        if self.is_empty_output(raw_output):
            return self._empty_result(raw_output)

        result = {
            "target": "",
            "target_ip": "",
            "port": 0,
            "server": "",
            "vulnerabilities": [],
            "total_vulns": 0,
            "total_items_tested": 0,
            "total_errors": 0,
            "scan_time": "",
            "raw_output": raw_output,
        }

        try:
            result["target"] = self._extract_target(raw_output)
            result["target_ip"] = self._extract_target_ip(raw_output)
            result["port"] = self._extract_port(raw_output)
            result["server"] = self._extract_server(raw_output)
            result["vulnerabilities"] = self._extract_vulnerabilities(raw_output)
            result["total_vulns"] = len(result["vulnerabilities"])
            result["total_items_tested"] = self._extract_items_tested(raw_output)
            result["total_errors"] = self._extract_errors(raw_output)
            result["scan_time"] = self._extract_scan_time(raw_output)

        except Exception as e:
            logger.warning(f"Nikto parsing encountered issues: {e}")

        return result

    def get_findings(self, parsed_data: dict) -> List[Finding]:
        """Extract security findings from parsed Nikto data."""
        findings = []

        # Server info finding
        server = parsed_data.get("server", "")
        if server:
            findings.append(Finding(
                description=f"Web server identified: {server}",
                severity="info",
                category="server_info",
                details={"server": server},
                explanation=(
                    f"The web server is running {server}. Knowing the server "
                    "software and version helps identify known vulnerabilities."
                ),
            ))

        # Vulnerability findings
        for vuln in parsed_data.get("vulnerabilities", []):
            severity = self._classify_vuln_risk(vuln)
            explanation = self._explain_vuln(vuln)

            findings.append(Finding(
                description=vuln.get("description", "Unknown vulnerability"),
                severity=severity,
                category="vulnerability",
                details={
                    "id": vuln.get("id", ""),
                    "method": vuln.get("method", ""),
                    "uri": vuln.get("uri", ""),
                },
                explanation=explanation,
            ))

        # Sort by severity
        findings.sort(key=lambda f: f.severity_order)
        return findings

    # ---------- Private extraction methods ----------

    def _extract_target(self, output: str) -> str:
        """Extract target hostname."""
        match = re.search(r"\+\s*Target Hostname:\s*(.+)", output)
        if match:
            return match.group(1).strip()
        return ""

    def _extract_target_ip(self, output: str) -> str:
        """Extract target IP address."""
        match = re.search(r"\+\s*Target IP:\s*(\S+)", output)
        if match:
            return match.group(1).strip()
        return ""

    def _extract_port(self, output: str) -> int:
        """Extract target port."""
        match = re.search(r"\+\s*Target Port:\s*(\d+)", output)
        if match:
            return int(match.group(1))
        return 80

    def _extract_server(self, output: str) -> str:
        """Extract web server information."""
        match = re.search(r"\+\s*Server:\s*(.+)", output)
        if match:
            return match.group(1).strip()
        return ""

    def _extract_vulnerabilities(self, output: str) -> list:
        """Extract vulnerability findings from Nikto output."""
        vulns = []

        # Nikto findings typically start with "+ " or "- "
        # Format: "+ OSVDB-XXXX: /path: Description"
        # or: "+ /path: Description"
        lines = output.split("\n")

        for line in lines:
            line = line.strip()

            # Skip header/info lines
            if not line.startswith("+") and not line.startswith("-"):
                continue

            # Skip target/server info lines
            if any(skip in line for skip in [
                "Target Hostname:", "Target IP:", "Target Port:",
                "Server:", "Start Time:", "End Time:",
                "host(s) tested", "items checked:",
                "Nikto", "SSL Info:", "Retrieved"
            ]):
                continue

            # Parse the finding
            vuln = self._parse_vuln_line(line)
            if vuln:
                vulns.append(vuln)

        return vulns

    def _parse_vuln_line(self, line: str) -> dict | None:
        """Parse a single vulnerability line."""
        # Remove leading +/- marker
        line = re.sub(r"^[+\-]\s*", "", line)

        if not line or len(line) < 10:
            return None

        vuln = {
            "id": "",
            "method": "",
            "uri": "",
            "description": line,
        }

        # Extract OSVDB/CVE ID
        id_match = re.search(r"(OSVDB-\d+|CVE-\d+-\d+)", line)
        if id_match:
            vuln["id"] = id_match.group(1)

        # Extract URI path
        uri_match = re.search(r"(/\S*?):", line)
        if uri_match:
            vuln["uri"] = uri_match.group(1)

        # Extract HTTP method
        method_match = re.search(r"(GET|POST|PUT|DELETE|OPTIONS|HEAD)\s", line)
        if method_match:
            vuln["method"] = method_match.group(1)

        return vuln

    def _extract_items_tested(self, output: str) -> int:
        """Extract total items tested count."""
        match = re.search(r"(\d+)\s+items?\s+checked", output)
        if match:
            return int(match.group(1))
        return 0

    def _extract_errors(self, output: str) -> int:
        """Extract error count."""
        match = re.search(r"(\d+)\s+error", output)
        if match:
            return int(match.group(1))
        return 0

    def _extract_scan_time(self, output: str) -> str:
        """Extract total scan time."""
        match = re.search(r"(\d+)\s+seconds?", output)
        if match:
            return f"{match.group(1)}s"
        return ""

    def _classify_vuln_risk(self, vuln: dict) -> str:
        """Classify risk level of a vulnerability finding."""
        desc = vuln.get("description", "").lower()

        # Critical indicators
        critical_keywords = ["remote code execution", "rce", "backdoor", "shell upload"]
        if any(kw in desc for kw in critical_keywords):
            return "critical"

        # High risk indicators
        high_keywords = [
            "sql injection", "xss", "cross-site", "directory traversal",
            "file inclusion", "command injection", "default password",
            "default credentials", "admin panel"
        ]
        if any(kw in desc for kw in high_keywords):
            return "high"

        # Medium risk indicators
        medium_keywords = [
            "directory listing", "directory indexing", "information disclosure",
            "server version", "outdated", "deprecated", "clickjacking",
            "missing header", "x-frame"
        ]
        if any(kw in desc for kw in medium_keywords):
            return "medium"

        # Low risk indicators
        low_keywords = [
            "cookie", "robots.txt", "favicon", "etag",
            "allowed methods", "options method"
        ]
        if any(kw in desc for kw in low_keywords):
            return "low"

        return "info"

    def _explain_vuln(self, vuln: dict) -> str:
        """Generate beginner-friendly explanation for a vulnerability."""
        desc = vuln.get("description", "").lower()

        if "directory listing" in desc or "directory indexing" in desc:
            return (
                "The web server is showing the contents of directories. "
                "This can reveal sensitive files and application structure to attackers."
            )
        if "default" in desc and ("password" in desc or "credential" in desc):
            return (
                "Default login credentials were detected. These are publicly known "
                "and should be changed immediately to prevent unauthorized access."
            )
        if "x-frame" in desc or "clickjacking" in desc:
            return (
                "The X-Frame-Options header is missing. This could allow an attacker "
                "to trick users into clicking hidden buttons (clickjacking attack)."
            )
        if "server version" in desc or "outdated" in desc:
            return (
                "The server is revealing its version information. Outdated software "
                "may have known vulnerabilities that attackers can exploit."
            )
        if "robots.txt" in desc:
            return (
                "The robots.txt file may contain paths that the site owner wants "
                "hidden from search engines — these could be interesting targets."
            )

        return (
            "A potential security issue was detected. Review the details "
            "and assess whether this poses a risk to your target."
        )

    def _empty_result(self, raw_output: str) -> dict:
        """Return empty result structure."""
        return {
            "target": "",
            "target_ip": "",
            "port": 0,
            "server": "",
            "vulnerabilities": [],
            "total_vulns": 0,
            "total_items_tested": 0,
            "total_errors": 0,
            "scan_time": "",
            "raw_output": raw_output or "",
        }
