"""
HydraParser — Parses Hydra CLI output into structured data.

Handles Hydra's text output for brute-force login results
including successful credentials and attack statistics.
"""

import re
import logging
from typing import List

from kalinova.parsers.base_parser import BaseParser, Finding

logger = logging.getLogger(__name__)


class HydraParser(BaseParser):
    """Parser for Hydra brute-force output."""

    def parse(self, raw_output: str) -> dict:
        """
        Parse Hydra output into structured dictionary.

        Returns:
            {
                "target": str,
                "service": str,
                "port": int,
                "found_credentials": [
                    {"host": str, "port": int, "service": str,
                     "username": str, "password": str}
                ],
                "total_found": int,
                "total_attempts": int,
                "status": str,  # "completed", "found", "no_results"
                "scan_time": str,
                "raw_output": str
            }
        """
        if self.is_empty_output(raw_output):
            return self._empty_result(raw_output)

        result = {
            "target": "",
            "service": "",
            "port": 0,
            "found_credentials": [],
            "total_found": 0,
            "total_attempts": 0,
            "status": "completed",
            "scan_time": "",
            "raw_output": raw_output,
        }

        try:
            result["target"] = self._extract_target(raw_output)
            result["service"] = self._extract_service(raw_output)
            result["port"] = self._extract_port(raw_output)
            result["found_credentials"] = self._extract_credentials(raw_output)
            result["total_found"] = len(result["found_credentials"])
            result["total_attempts"] = self._extract_attempts(raw_output)
            result["scan_time"] = self._extract_scan_time(raw_output)

            if result["total_found"] > 0:
                result["status"] = "found"
            else:
                result["status"] = "no_results"

        except Exception as e:
            logger.warning(f"Hydra parsing encountered issues: {e}")

        return result

    def get_findings(self, parsed_data: dict) -> List[Finding]:
        """Extract findings from Hydra results."""
        findings = []

        for cred in parsed_data.get("found_credentials", []):
            username = cred.get("username", "")
            password = cred.get("password", "")
            service = cred.get("service", "")
            host = cred.get("host", "")

            findings.append(Finding(
                description=(
                    f"Valid credentials found — "
                    f"{username}:{password} on {service}://{host}"
                ),
                severity="critical",
                category="credential",
                details=cred,
                explanation=(
                    f"Hydra successfully logged in with username '{username}' and "
                    f"password '{password}' on the {service} service. This means "
                    "the account uses weak or known credentials and is vulnerable "
                    "to unauthorized access."
                ),
            ))

        if not findings and parsed_data.get("status") == "no_results":
            findings.append(Finding(
                description="No valid credentials found.",
                severity="info",
                category="credential",
                details={},
                explanation=(
                    "Hydra tested all provided username/password combinations "
                    "but none worked. The service may have strong passwords, "
                    "rate limiting, or account lockout in place."
                ),
            ))

        return findings

    # ---------- Private extraction methods ----------

    def _extract_target(self, output: str) -> str:
        """Extract target from Hydra output."""
        # "[DATA] attacking ssh://192.168.1.1:22/"
        match = re.search(r"attacking\s+\S+://(\S+?)(?::\d+)?/", output)
        if match:
            return match.group(1)
        return ""

    def _extract_service(self, output: str) -> str:
        """Extract service type from Hydra output."""
        match = re.search(r"attacking\s+(\S+)://", output)
        if match:
            return match.group(1)
        return ""

    def _extract_port(self, output: str) -> int:
        """Extract port from Hydra output."""
        match = re.search(r"attacking\s+\S+://\S+?:(\d+)", output)
        if match:
            return int(match.group(1))
        return 0

    def _extract_credentials(self, output: str) -> list:
        """Extract successful login credentials."""
        credentials = []

        # Hydra success format: "[22][ssh] host: 192.168.1.1   login: admin   password: password123"
        pattern = re.compile(
            r"\[(\d+)\]\[(\S+)\]\s+host:\s*(\S+)\s+login:\s*(\S+)\s+password:\s*(.*)"
        )

        for match in pattern.finditer(output):
            credentials.append({
                "port": int(match.group(1)),
                "service": match.group(2),
                "host": match.group(3),
                "username": match.group(4),
                "password": match.group(5).strip(),
            })

        return credentials

    def _extract_attempts(self, output: str) -> int:
        """Extract total number of login attempts."""
        # "[STATUS] 64.00 tries/min" or "X of Y [child ..."
        match = re.search(r"(\d+)\s+of\s+(\d+)", output)
        if match:
            return int(match.group(2))

        match = re.search(r"(\d+)\s+valid password", output)
        if match:
            return 0  # Only found count, not total

        return 0

    def _extract_scan_time(self, output: str) -> str:
        """Extract scan duration."""
        match = re.search(r"(\d+:\d+:\d+)", output)
        if match:
            return match.group(1)
        return ""

    def _empty_result(self, raw_output: str) -> dict:
        """Return empty result structure."""
        return {
            "target": "",
            "service": "",
            "port": 0,
            "found_credentials": [],
            "total_found": 0,
            "total_attempts": 0,
            "status": "no_results",
            "scan_time": "",
            "raw_output": raw_output or "",
        }
