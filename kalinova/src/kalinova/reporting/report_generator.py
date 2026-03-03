"""
ReportGenerator — Generates HTML reports from scan results.

Uses Jinja2 templates to produce professional HTML reports
for assessment tool results.
"""

import os
import logging
from datetime import datetime
from typing import Optional, List

from jinja2 import Environment, FileSystemLoader, BaseLoader

from kalinova.parsers.base_parser import Finding

logger = logging.getLogger(__name__)

# Embedded HTML template (used when template file not found)
DEFAULT_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kalinova Report — {{ tool_name }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0f0f1a;
            color: #e0e0e0;
            line-height: 1.6;
            padding: 40px;
        }
        .report-header {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border: 1px solid #0f3460;
            border-radius: 12px;
            padding: 30px 40px;
            margin-bottom: 30px;
        }
        .report-header h1 {
            color: #00d4ff;
            font-size: 28px;
            margin-bottom: 10px;
        }
        .report-header .meta {
            color: #8899aa;
            font-size: 14px;
        }
        .report-header .meta span {
            margin-right: 20px;
        }
        .summary-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 16px;
            margin-bottom: 30px;
        }
        .card {
            background: #1a1a2e;
            border: 1px solid #2a2a4e;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }
        .card .count { font-size: 36px; font-weight: bold; }
        .card .label { font-size: 13px; color: #8899aa; margin-top: 5px; }
        .card.critical .count { color: #ff4757; }
        .card.high .count { color: #ff6b6b; }
        .card.medium .count { color: #ffa502; }
        .card.low .count { color: #2ed573; }
        .card.info .count { color: #1e90ff; }
        .findings-section {
            background: #1a1a2e;
            border: 1px solid #2a2a4e;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
        }
        .findings-section h2 {
            color: #00d4ff;
            margin-bottom: 20px;
            font-size: 20px;
        }
        .finding {
            border-left: 4px solid #2a2a4e;
            padding: 15px 20px;
            margin-bottom: 15px;
            background: #12121e;
            border-radius: 0 8px 8px 0;
        }
        .finding.critical { border-left-color: #ff4757; }
        .finding.high { border-left-color: #ff6b6b; }
        .finding.medium { border-left-color: #ffa502; }
        .finding.low { border-left-color: #2ed573; }
        .finding.info { border-left-color: #1e90ff; }
        .finding .severity-badge {
            display: inline-block;
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: bold;
            text-transform: uppercase;
            margin-bottom: 8px;
        }
        .severity-badge.critical { background: #ff4757; color: #fff; }
        .severity-badge.high { background: #ff6b6b; color: #fff; }
        .severity-badge.medium { background: #ffa502; color: #000; }
        .severity-badge.low { background: #2ed573; color: #000; }
        .severity-badge.info { background: #1e90ff; color: #fff; }
        .finding .description {
            font-size: 15px;
            margin-bottom: 6px;
        }
        .finding .explanation {
            font-size: 13px;
            color: #8899aa;
            font-style: italic;
        }
        .raw-output {
            background: #0a0a14;
            border: 1px solid #2a2a4e;
            border-radius: 8px;
            padding: 20px;
            margin-top: 20px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            white-space: pre-wrap;
            max-height: 400px;
            overflow-y: auto;
            color: #a0a0a0;
        }
        .footer {
            text-align: center;
            color: #555;
            font-size: 12px;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #2a2a4e;
        }
    </style>
</head>
<body>
    <div class="report-header">
        <h1>{{ tool_name | upper }} Scan Report</h1>
        <div class="meta">
            <span>🎯 Target: <strong>{{ target }}</strong></span>
            <span>📅 Date: {{ timestamp }}</span>
            <span>⏱️ Duration: {{ duration }}</span>
        </div>
    </div>

    <div class="summary-cards">
        <div class="card critical">
            <div class="count">{{ severity_counts.critical }}</div>
            <div class="label">Critical</div>
        </div>
        <div class="card high">
            <div class="count">{{ severity_counts.high }}</div>
            <div class="label">High</div>
        </div>
        <div class="card medium">
            <div class="count">{{ severity_counts.medium }}</div>
            <div class="label">Medium</div>
        </div>
        <div class="card low">
            <div class="count">{{ severity_counts.low }}</div>
            <div class="label">Low</div>
        </div>
        <div class="card info">
            <div class="count">{{ severity_counts.info }}</div>
            <div class="label">Informational</div>
        </div>
    </div>

    <div class="findings-section">
        <h2>Findings ({{ findings | length }})</h2>
        {% for finding in findings %}
        <div class="finding {{ finding.severity }}">
            <span class="severity-badge {{ finding.severity }}">{{ finding.severity }}</span>
            <div class="description">{{ finding.description }}</div>
            {% if finding.explanation %}
            <div class="explanation">💡 {{ finding.explanation }}</div>
            {% endif %}
        </div>
        {% endfor %}
        {% if not findings %}
        <p style="color: #8899aa;">No findings to report.</p>
        {% endif %}
    </div>

    {% if raw_output %}
    <div class="findings-section">
        <h2>Raw Tool Output</h2>
        <div class="raw-output">{{ raw_output }}</div>
    </div>
    {% endif %}

    <div class="footer">
        Generated by Kalinova v1.0 — Intelligent Security Suite for Kali Linux
    </div>
</body>
</html>"""


class ReportGenerator:
    """
    Generates HTML reports from assessment tool results.

    Uses Jinja2 for template rendering with a professional
    dark-themed design.
    """

    def __init__(self, template_dir: str = ""):
        self._template_dir = template_dir
        self._env: Optional[Environment] = None

        if template_dir and os.path.isdir(template_dir):
            self._env = Environment(
                loader=FileSystemLoader(template_dir),
                autoescape=True,
            )
        else:
            self._env = Environment(
                loader=BaseLoader(),
                autoescape=True,
            )

    def generate(
        self,
        tool_name: str,
        target: str,
        findings: List[Finding],
        parsed_data: dict,
        severity_counts: dict,
        raw_output: str = "",
        duration: str = "",
    ) -> str:
        """
        Generate an HTML report.

        Args:
            tool_name: Name of the tool.
            target: Scan target.
            findings: List of Finding objects.
            parsed_data: Full parsed data dictionary.
            severity_counts: Dictionary of severity → count.
            raw_output: Raw CLI output for inclusion.
            duration: Scan duration string.

        Returns:
            Complete HTML string.
        """
        template = self._env.from_string(DEFAULT_TEMPLATE)

        # Convert findings to template-friendly dicts
        finding_dicts = [
            {
                "severity": f.severity,
                "description": f.description,
                "explanation": f.explanation,
                "category": f.category,
            }
            for f in findings
        ]

        html = template.render(
            tool_name=tool_name,
            target=target,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            duration=duration or "N/A",
            findings=finding_dicts,
            severity_counts=severity_counts,
            raw_output=raw_output[:5000] if raw_output else "",
        )

        return html

    def save(self, html: str, filepath: str) -> str:
        """
        Save HTML report to file.

        Args:
            html: HTML content.
            filepath: Output file path.

        Returns:
            Absolute path to saved file.
        """
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)

        abs_path = os.path.abspath(filepath)
        logger.info(f"Report saved to: {abs_path}")
        return abs_path

    def generate_and_save(
        self,
        filepath: str,
        tool_name: str,
        target: str,
        findings: List[Finding],
        parsed_data: dict,
        severity_counts: dict,
        raw_output: str = "",
        duration: str = "",
    ) -> str:
        """Generate and save report in one call."""
        html = self.generate(
            tool_name=tool_name,
            target=target,
            findings=findings,
            parsed_data=parsed_data,
            severity_counts=severity_counts,
            raw_output=raw_output,
            duration=duration,
        )
        return self.save(html, filepath)
