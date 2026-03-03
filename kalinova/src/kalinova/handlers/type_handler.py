"""
TypeHandler — Routes parsed output based on tool type.

Determines how results are displayed and what additional
processing (ML suggestions, reports) should be triggered.
"""

import logging
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

from kalinova.parsers.base_parser import Finding

logger = logging.getLogger(__name__)


@dataclass
class ScanResult:
    """Complete result of a tool scan."""
    tool_name: str
    tool_type: str  # "assessment", "action", "utility"
    target: str
    status: str  # "completed", "cancelled", "error"
    exit_code: int
    raw_output: str
    parsed_data: dict
    findings: List[Finding]
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration_ms: int = 0
    ml_enabled: bool = False
    report_enabled: bool = False


class TypeHandler:
    """
    Routes parsed tool output based on tool type declaration.

    - assessment → full structured report + risk tags + ML suggestion + export
    - action → structured summary
    - utility → basic formatted output
    """

    @staticmethod
    def process(scan_result: ScanResult) -> dict:
        """
        Process a scan result and determine display/action behavior.

        Args:
            scan_result: Complete ScanResult object.

        Returns:
            Dictionary with display instructions:
                {
                    "display_mode": str,
                    "show_findings": bool,
                    "show_risk_tags": bool,
                    "show_ml_suggestion": bool,
                    "enable_report_export": bool,
                    "title": str,
                    "summary": str,
                    "findings": list,
                }
        """
        handler_map = {
            "assessment": TypeHandler._handle_assessment,
            "action": TypeHandler._handle_action,
            "utility": TypeHandler._handle_utility,
        }

        handler = handler_map.get(scan_result.tool_type, TypeHandler._handle_utility)
        return handler(scan_result)

    @staticmethod
    def _handle_assessment(scan_result: ScanResult) -> dict:
        """Handle assessment tool results — full report mode."""
        logger.info(f"Processing assessment result for {scan_result.tool_name}")

        findings = scan_result.findings
        severity_counts = TypeHandler._count_severities(findings)

        return {
            "display_mode": "full_report",
            "show_findings": True,
            "show_risk_tags": True,
            "show_ml_suggestion": scan_result.ml_enabled,
            "enable_report_export": scan_result.report_enabled,
            "title": f"{scan_result.tool_name.upper()} Scan Report",
            "summary": (
                f"Scan completed on {scan_result.target}. "
                f"Found {len(findings)} findings: "
                f"{severity_counts.get('critical', 0)} critical, "
                f"{severity_counts.get('high', 0)} high, "
                f"{severity_counts.get('medium', 0)} medium, "
                f"{severity_counts.get('low', 0)} low, "
                f"{severity_counts.get('info', 0)} informational."
            ),
            "findings": findings,
            "severity_counts": severity_counts,
            "parsed_data": scan_result.parsed_data,
        }

    @staticmethod
    def _handle_action(scan_result: ScanResult) -> dict:
        """Handle action tool results — summary mode."""
        logger.info(f"Processing action result for {scan_result.tool_name}")

        findings = scan_result.findings
        success_count = sum(
            1 for f in findings
            if f.category == "credential" and f.severity != "info"
        )

        return {
            "display_mode": "summary",
            "show_findings": True,
            "show_risk_tags": True,
            "show_ml_suggestion": False,
            "enable_report_export": False,
            "title": f"{scan_result.tool_name.upper()} Results",
            "summary": (
                f"Completed on {scan_result.target}. "
                f"Results: {success_count} credential(s) found."
                if success_count > 0 else
                f"Completed on {scan_result.target}. No credentials found."
            ),
            "findings": findings,
            "severity_counts": TypeHandler._count_severities(findings),
            "parsed_data": scan_result.parsed_data,
        }

    @staticmethod
    def _handle_utility(scan_result: ScanResult) -> dict:
        """Handle utility tool results — formatted text mode."""
        logger.info(f"Processing utility result for {scan_result.tool_name}")

        return {
            "display_mode": "formatted_text",
            "show_findings": False,
            "show_risk_tags": False,
            "show_ml_suggestion": False,
            "enable_report_export": False,
            "title": f"{scan_result.tool_name.upper()} Output",
            "summary": f"Tool completed on {scan_result.target}.",
            "findings": scan_result.findings,
            "severity_counts": {},
            "parsed_data": scan_result.parsed_data,
        }

    @staticmethod
    def _count_severities(findings: List[Finding]) -> dict:
        """Count findings by severity level."""
        counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
        for f in findings:
            if f.severity in counts:
                counts[f.severity] += 1
        return counts
