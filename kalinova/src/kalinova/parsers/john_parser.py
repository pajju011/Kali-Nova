"""
JohnParser — Parses John the Ripper output into structured data.

Handles John's text output for password cracking results,
progress status, and cracked credential summaries.
"""

import re
import logging
from typing import List

from kalinova.parsers.base_parser import BaseParser, Finding

logger = logging.getLogger(__name__)


class JohnParser(BaseParser):
    """Parser for John the Ripper output."""

    def parse(self, raw_output: str) -> dict:
        """
        Parse John output into structured dictionary.

        Returns:
            {
                "cracked": [
                    {"hash": str, "password": str, "format": str}
                ],
                "total_cracked": int,
                "total_hashes": int,
                "format_detected": str,
                "status": str,  # "completed", "running", "no_cracks"
                "session": str,
                "raw_output": str
            }
        """
        if self.is_empty_output(raw_output):
            return self._empty_result(raw_output)

        result = {
            "cracked": [],
            "total_cracked": 0,
            "total_hashes": 0,
            "format_detected": "",
            "status": "completed",
            "session": "",
            "raw_output": raw_output,
        }

        try:
            result["cracked"] = self._extract_cracked(raw_output)
            result["total_cracked"] = len(result["cracked"])
            result["total_hashes"] = self._extract_total_hashes(raw_output)
            result["format_detected"] = self._extract_format(raw_output)
            result["session"] = self._extract_session(raw_output)

            if result["total_cracked"] == 0:
                if "Session completed" in raw_output or "No password hashes" in raw_output:
                    result["status"] = "no_cracks"
                elif "guesses:" in raw_output.lower():
                    result["status"] = "running"

        except Exception as e:
            logger.warning(f"John parsing encountered issues: {e}")

        return result

    def get_findings(self, parsed_data: dict) -> List[Finding]:
        """Extract findings from John results."""
        findings = []

        for cred in parsed_data.get("cracked", []):
            password = cred.get("password", "")
            hash_val = cred.get("hash", "")

            severity = self._classify_password_strength(password)

            findings.append(Finding(
                description=f"Password cracked: '{password}' (hash: {hash_val[:20]}...)",
                severity=severity,
                category="credential",
                details=cred,
                explanation=self._explain_password(password),
            ))

        if not findings and parsed_data.get("status") == "no_cracks":
            findings.append(Finding(
                description="No passwords were cracked.",
                severity="info",
                category="credential",
                details={},
                explanation=(
                    "John was unable to crack any hashes. This could mean "
                    "the passwords are strong, or a larger wordlist is needed."
                ),
            ))

        return findings

    # ---------- Private extraction methods ----------

    def _extract_cracked(self, output: str) -> list:
        """Extract cracked passwords from John output."""
        cracked = []

        # John --show format: "user:password" or "hash:password"
        # John cracking format: "password    (user)" or similar
        lines = output.strip().split("\n")

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Skip status/info lines
            if any(skip in line for skip in [
                "Loaded", "Press", "guesses:", "Using default",
                "Proceeding", "Session", "Warning", "Note:",
                "password hash", "Cost", "Will run"
            ]):
                continue

            # Format from --show: "user:password" or just "hash:password"
            if ":" in line and "password hashes cracked" not in line.lower():
                parts = line.split(":")
                if len(parts) >= 2:
                    # Filter out empty or header-like entries
                    potential_password = parts[1].strip()
                    if potential_password and len(potential_password) < 200:
                        cracked.append({
                            "hash": parts[0].strip(),
                            "password": potential_password,
                            "format": "",
                        })
                continue

            # Format during cracking: "password     (username)"
            match = re.match(r"^(\S+)\s+\((.+)\)$", line)
            if match:
                cracked.append({
                    "hash": match.group(2),
                    "password": match.group(1),
                    "format": "",
                })

        return cracked

    def _extract_total_hashes(self, output: str) -> int:
        """Extract total number of hashes loaded."""
        match = re.search(r"Loaded\s+(\d+)\s+password", output)
        if match:
            return int(match.group(1))
        return 0

    def _extract_format(self, output: str) -> str:
        """Extract detected hash format."""
        match = re.search(r'Loaded\s+\d+\s+password.*?\((.+?)\)', output)
        if match:
            return match.group(1).strip()
        return ""

    def _extract_session(self, output: str) -> str:
        """Extract session name."""
        match = re.search(r"Session\s+(\S+)", output)
        if match:
            return match.group(1).strip()
        return ""

    def _classify_password_strength(self, password: str) -> str:
        """Classify the risk based on cracked password strength."""
        if not password:
            return "info"
        if len(password) <= 4:
            return "critical"
        if len(password) <= 6:
            return "high"
        if password.isdigit() or password.isalpha():
            return "high"
        if len(password) <= 8:
            return "medium"
        return "low"

    def _explain_password(self, password: str) -> str:
        """Generate explanation for a cracked password."""
        if len(password) <= 4:
            return (
                f"The password '{password}' is extremely weak — only "
                f"{len(password)} characters. It can be cracked in seconds."
            )
        if len(password) <= 6:
            return (
                f"The password '{password}' is very short. Passwords under "
                "8 characters are easily cracked with modern hardware."
            )
        if password.isdigit():
            return (
                f"The password '{password}' is numbers-only. Numeric-only "
                "passwords are weak because they have a very small key space."
            )
        return (
            f"The password was cracked. Consider using longer passwords "
            "with a mix of uppercase, lowercase, numbers, and symbols."
        )

    def _empty_result(self, raw_output: str) -> dict:
        """Return empty result structure."""
        return {
            "cracked": [],
            "total_cracked": 0,
            "total_hashes": 0,
            "format_detected": "",
            "status": "no_cracks",
            "session": "",
            "raw_output": raw_output or "",
        }
