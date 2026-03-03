"""
Base parser interface for all Kalinova tool output parsers.

Every tool parser must extend BaseParser and implement
the parse() method. This ensures a consistent contract
across all tools as the library scales to 600+.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Finding:
    """A single security finding from a tool scan."""
    description: str
    severity: str  # "critical", "high", "medium", "low", "info"
    category: str  # "open_port", "vulnerability", "credential", etc.
    details: dict = field(default_factory=dict)
    explanation: str = ""  # Beginner-friendly explanation

    @property
    def severity_order(self) -> int:
        """Numeric severity for sorting (lower = more severe)."""
        order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
        return order.get(self.severity, 5)


class BaseParser(ABC):
    """
    Abstract base class for all tool output parsers.

    Subclasses must implement:
        - parse(raw_output) -> dict
        - get_findings(parsed_data) -> list[Finding]
    """

    @abstractmethod
    def parse(self, raw_output: str) -> dict:
        """
        Parse raw CLI output into a structured dictionary.

        Args:
            raw_output: Complete stdout string from QProcess.

        Returns:
            Structured dictionary with tool-specific data.

        Raises:
            ParsingError: If the output cannot be parsed.
        """
        raise NotImplementedError

    @abstractmethod
    def get_findings(self, parsed_data: dict) -> List[Finding]:
        """
        Extract risk-classified findings from parsed data.

        Args:
            parsed_data: Dictionary returned by parse().

        Returns:
            List of Finding objects with severity levels.
        """
        raise NotImplementedError

    def is_empty_output(self, raw_output: str) -> bool:
        """Check if the output is effectively empty."""
        return not raw_output or not raw_output.strip()
