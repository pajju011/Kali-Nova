import os
# pyrefly: ignore [missing-import]
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QMessageBox, QTableWidget, QTableWidgetItem,
    QTextEdit, QScrollArea, QFrame, QFileDialog, QHeaderView
)
# pyrefly: ignore [missing-import]
from PyQt6.QtCore import Qt
# pyrefly: ignore [missing-import]
from PyQt6.QtGui import QFont, QColor

from core.database import DatabaseManager
from core.ai_copilot import AICopilot

class ReportsPage(QWidget):

    def __init__(self):
        super().__init__()

        self.setObjectName("reportsPageContainer")
        self.setStyleSheet("""
            QWidget#reportsPageContainer {
                background-color: #0b1220;
            }
            
            QFrame.reportsCard {
                background-color: #0e1728;
                border: 1px solid #1c2a47;
                border-radius: 12px;
            }
            
            QLabel#sectionHeader {
                color: #8ea2c5;
                font-family: 'Segoe UI', sans-serif;
                font-size: 10px;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                padding-bottom: 4px;
                border-bottom: 1px solid #1e2e4f;
            }
            
            QTableWidget {
                background-color: #0e1728;
                border: 1px solid #1c2a47;
                border-radius: 8px;
                color: #d6e2ff;
                gridline-color: #1e2e4f;
                font-family: 'Segoe UI', sans-serif;
            }
            
            QTableWidget::item {
                padding: 10px;
                background-color: transparent;
            }
            
            QHeaderView::section {
                background-color: #15223b;
                color: #8ea2c5;
                font-weight: bold;
                padding: 8px;
                border: 1px solid #1c2a47;
            }
            
            QTextEdit#terminalViewer {
                background-color: #050a12;
                border: 1px solid #14213d;
                border-radius: 8px;
                color: #38bdf8;
                font-family: 'Consolas', 'Cascadia Code', 'Courier New', monospace;
                font-size: 13px;
                padding: 8px;
            }
            
            QTextEdit#copilotAdviceBox {
                background-color: #070e17;
                border: 1px solid #1a2a42;
                border-radius: 8px;
                color: #10b981;
                font-family: 'Consolas', 'Cascadia Code', 'Courier New', monospace;
                font-size: 13px;
                padding: 8px;
            }
            
            QPushButton#exportBtn {
                background-color: #3b82f6;
                color: #ffffff;
                font-weight: bold;
                padding: 10px 16px;
                border-radius: 6px;
                border: 1px solid #2563eb;
            }
            QPushButton#exportBtn:hover {
                background-color: #60a5fa;
            }
            
            QPushButton#exportHtmlBtn {
                background-color: #8b5cf6;
                color: #ffffff;
                font-weight: bold;
                padding: 10px 16px;
                border-radius: 6px;
                border: 1px solid #7c3aed;
            }
            QPushButton#exportHtmlBtn:hover {
                background-color: #a78bfa;
            }

            QPushButton#deleteBtn {
                background-color: #3b1424;
                color: #f43f5e;
                font-weight: bold;
                padding: 10px 16px;
                border-radius: 6px;
                border: 1px solid #5c1b35;
            }
            QPushButton#deleteBtn:hover {
                background-color: #f43f5e;
                color: #ffffff;
            }
        """)

        # Main Layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(16)

        # Header Title
        title_layout = QVBoxLayout()
        header_title = QLabel("▲ KALINOVA // HISTORICAL DOSSIERS")
        header_title.setStyleSheet("font-size: 20px; font-weight: 800; color: #00f0ff; letter-spacing: 1px;")
        header_subtitle = QLabel("PERSISTENT SESSION LOGS, DIAGNOSTICS & CLIENT EXPORTERS")
        header_subtitle.setStyleSheet("font-size: 10px; font-weight: 600; color: #64748b; letter-spacing: 0.5px;")
        title_layout.addWidget(header_title)
        title_layout.addWidget(header_subtitle)
        main_layout.addLayout(title_layout)

        # =====================================================================
        # SPLIT VIEW LAYOUT
        # =====================================================================
        split_layout = QHBoxLayout()
        split_layout.setSpacing(16)

        # ------------------ LEFT SIDE: HISTORICAL TABLE ------------------
        left_frame = QFrame()
        left_frame.setProperty("class", "reportsCard")
        left_layout = QVBoxLayout(left_frame)
        left_layout.setContentsMargins(16, 16, 16, 16)
        left_layout.setSpacing(12)

        left_title = QLabel("Scan Registry Database")
        left_title.setObjectName("sectionHeader")
        left_layout.addWidget(left_title)

        self.scan_table = QTableWidget()
        self.scan_table.setColumnCount(5)
        self.scan_table.setHorizontalHeaderLabels(["ID", "Target Host", "Tool Module", "Threat Level", "Scanned Date"])
        self.scan_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.scan_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.scan_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.scan_table.itemSelectionChanged.connect(self.scan_selection_changed)
        left_layout.addWidget(self.scan_table)

        # Exporter controls at the bottom of the table
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(8)

        self.export_md_btn = QPushButton("Export MD Dossier")
        self.export_md_btn.setObjectName("exportBtn")
        self.export_md_btn.setEnabled(False)
        self.export_md_btn.clicked.connect(self.export_markdown)

        self.export_html_btn = QPushButton("Export HTML Dossier")
        self.export_html_btn.setObjectName("exportHtmlBtn")
        self.export_html_btn.setEnabled(False)
        self.export_html_btn.clicked.connect(self.export_html)

        self.delete_btn = QPushButton("Delete Session")
        self.delete_btn.setObjectName("deleteBtn")
        self.delete_btn.setEnabled(False)
        self.delete_btn.clicked.connect(self.delete_session)

        controls_layout.addWidget(self.export_md_btn)
        controls_layout.addWidget(self.export_html_btn)
        controls_layout.addWidget(self.delete_btn)
        left_layout.addLayout(controls_layout)

        split_layout.addWidget(left_frame, 4)

        # ------------------ RIGHT SIDE: LOGS & SECURITY ADVISORIES ------------------
        right_frame = QFrame()
        right_frame.setProperty("class", "reportsCard")
        right_layout = QVBoxLayout(right_frame)
        right_layout.setContentsMargins(16, 16, 16, 16)
        right_layout.setSpacing(12)

        right_title = QLabel("Session Inspector & Copilot")
        right_title.setObjectName("sectionHeader")
        right_layout.addWidget(right_title)

        # Monospaced Terminal Output Card
        terminal_label = QLabel("Console Stdout Inspector")
        terminal_label.setStyleSheet("font-size: 11px; font-weight: bold; color: #8ea2c5;")
        self.log_viewer = QTextEdit()
        self.log_viewer.setObjectName("terminalViewer")
        self.log_viewer.setReadOnly(True)
        
        # Heuristic Copilot Advisory Card
        copilot_label = QLabel("Heuristic Patching Diagnostics")
        copilot_label.setStyleSheet("font-size: 11px; font-weight: bold; color: #10b981;")
        self.copilot_box = QTextEdit()
        self.copilot_box.setObjectName("copilotAdviceBox")
        self.copilot_box.setReadOnly(True)

        right_layout.addWidget(terminal_label)
        right_layout.addWidget(self.log_viewer, 2)
        right_layout.addWidget(copilot_label)
        right_layout.addWidget(self.copilot_box, 1)

        split_layout.addWidget(right_frame, 3)

        main_layout.addLayout(split_layout)

        # Keep tracks of database list
        self.loaded_scans = []
        self.selected_scan = None

        # Load initial database rows
        self.load_scans_from_database()

    # ========================
    # DB Loader
    # ========================

    def load_scans_from_database(self):
        self.scan_table.clearSelection()
        self.scan_table.setRowCount(0)
        self.loaded_scans = DatabaseManager.get_all_scans()

        for idx, scan in enumerate(self.loaded_scans):
            self.scan_table.insertRow(idx)
            
            # Row Items
            id_item = QTableWidgetItem(str(scan["id"]))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            target_item = QTableWidgetItem(scan["target"])
            tool_item = QTableWidgetItem(scan["tool_name"])
            
            threat_item = QTableWidgetItem(scan["threat_level"])
            threat_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            # Dynamic colors based on threat
            if scan["threat_level"].upper() == "CRITICAL" or scan["threat_level"].upper() == "HIGH":
                threat_item.setForeground(QColor(244, 63, 94))  # Crimson
            elif scan["threat_level"].upper() == "MEDIUM":
                threat_item.setForeground(QColor(245, 158, 11))  # Amber
            else:
                threat_item.setForeground(QColor(16, 185, 129))  # Emerald

            date_item = QTableWidgetItem(scan["timestamp"])
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.scan_table.setItem(idx, 0, id_item)
            self.scan_table.setItem(idx, 1, target_item)
            self.scan_table.setItem(idx, 2, tool_item)
            self.scan_table.setItem(idx, 3, threat_item)
            self.scan_table.setItem(idx, 4, date_item)

        # Reset selection states
        self.selected_scan = None
        self.log_viewer.setText("Select a scan session in the registry database to inspect detailed logs.")
        self.copilot_box.setText("Standing by. Select a database entry to run heuristics.")
        self.export_md_btn.setEnabled(False)
        self.export_html_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)

    # ========================
    # Selection Handler
    # ========================

    def scan_selection_changed(self):
        selected_rows = self.scan_table.selectionModel().selectedRows()
        if not selected_rows:
            return

        row_idx = selected_rows[0].row()
        if row_idx >= len(self.loaded_scans):
            return

        self.selected_scan = self.loaded_scans[row_idx]
        
        # Load terminal logs
        self.log_viewer.setText(
            f"=== SESSION INSPECT: ID {self.selected_scan['id']} ===\n"
            f"TARGET HOST : {self.selected_scan['target']}\n"
            f"COMMAND RUN : {self.selected_scan['command']}\n"
            f"DATETIME    : {self.selected_scan['timestamp']}\n"
            f"THREAT LEVEL: {self.selected_scan['threat_level']} (Score: {self.selected_scan['risk_score']}/100)\n"
            f"{'='*50}\n\n"
            f"{self.selected_scan['stdout']}"
        )

        # Trigger Heuristic Copilot
        self.update_copilot_advisories()

        # Enable Exporters
        self.export_md_btn.setEnabled(True)
        self.export_html_btn.setEnabled(True)
        self.delete_btn.setEnabled(True)

    def update_copilot_advisories(self):
        if not self.selected_scan:
            return

        # Re-derive events from stdout
        events = []
        stdout_lower = self.selected_scan["stdout"].lower()
        if "sql injection" in stdout_lower:
            events.append("SQL_INJECTION")
        if "brute force" in stdout_lower or "hydra" in stdout_lower or "login:" in stdout_lower:
            events.append("BRUTE_FORCE")
        if "found:" in stdout_lower:
            events.append("DIR_ENUM")
        if "@" in stdout_lower and "." in stdout_lower:
            events.append("EMAIL_ENUM")

        # Parse ports
        ports = []
        import re
        port_matches = re.findall(r"(\d+)/tcp\s+open", self.selected_scan["stdout"])
        for p in port_matches:
            ports.append(int(p))

        # Direct mapped ports saved in DB
        db_ports = self.selected_scan["parsed_ports"]
        if db_ports:
            for p in db_ports.split(","):
                if p.strip() and p.strip().isdigit():
                    ports.append(int(p.strip()))

        # Deduplicate
        ports = list(set(ports))

        # Query Copilot
        findings = AICopilot.diagnose(events, ports)
        
        copilot_text = f"=== HEURISTIC SECURITY ADVISORY (DIAGNOSTICS ENGINE) ===\n"
        copilot_text += f"Threat Level: {self.selected_scan['threat_level']} | Target: {self.selected_scan['target']}\n"
        copilot_text += f"Total Vulnerabilities / Exposed Sockets Identified: {len(findings)}\n"
        copilot_text += f"{'='*60}\n\n"

        for idx, f in enumerate(findings):
            copilot_text += f"[{idx+1}] VULNERABILITY: {f['title'].upper()}\n"
            copilot_text += f"    CVSS SEVERITY: {f['cvss']} ({f['severity']})\n"
            copilot_text += f"    DESCRIPTION  : {f['description']}\n\n"
            copilot_text += f"    REMEDIATION DIRECTIVE (PYTHON TEMPLATE):\n"
            copilot_text += f"    ---\n"
            # Indent code blocks for visual clarity
            indented_py = "\n".join("    " + line for line in f['remediation_python'].split("\n"))
            copilot_text += f"{indented_py}\n"
            copilot_text += f"    ---\n\n"

        self.copilot_box.setText(copilot_text)

    # ========================
    # MD Exporter
    # ========================

    def export_markdown(self):
        if not self.selected_scan:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Markdown Report",
            f"Kalinova_Dossier_{self.selected_scan['id']}.md",
            "Markdown Files (*.md)"
        )
        if not file_path:
            return

        try:
            # Re-diagnose
            events = []
            stdout_lower = self.selected_scan["stdout"].lower()
            if "sql" in stdout_lower: events.append("SQL_INJECTION")
            if "brute" in stdout_lower or "hydra" in stdout_lower: events.append("BRUTE_FORCE")
            if "found:" in stdout_lower: events.append("DIR_ENUM")
            if "@" in stdout_lower and "." in stdout_lower: events.append("EMAIL_ENUM")
            
            ports = []
            db_ports = self.selected_scan["parsed_ports"]
            if db_ports:
                ports = [int(p) for p in db_ports.split(",") if p.strip().isdigit()]

            findings = AICopilot.diagnose(events, ports)

            md = f"""# Kalinova // Penetration Testing Assessment Report

An offline-first, professional cybersecurity audit dossier generated automatically by **Kalinova Security Command Suite**.

---

## 1. Executive Summary

| Security Metric | Value / Severity |
|---|---|
| **Target Host** | `{self.selected_scan['target']}` |
| **Audit Tool Used** | `{self.selected_scan['tool_name']}` |
| **Command Run** | `{self.selected_scan['command']}` |
| **Audit Timestamp** | `{self.selected_scan['timestamp']}` |
| **Assessed Threat Score** | **`{self.selected_scan['risk_score']} / 100`** |
| **Global Threat Rating** | **`{self.selected_scan['threat_level']}`** |

---

## 2. Threat Analysis & Copilot Advisories

Below is a parsed list of exposed ports and event anomalies discovered during this scan:

"""
            for idx, f in enumerate(findings):
                md += f"""### [{idx+1}] {f['title']}
* **CVSS Rating**: `{f['cvss']} / 10.0`
* **Vulnerability Severity**: `{f['severity']}`
* **Vulnerability Description**: {f['description']}

#### Technical Remediation Code:
```python
{f['remediation_python']}
```

```javascript
{f['remediation_node']}
```

---
"""

            md += f"""

## 3. Raw Scan Terminal Output

The following console log represents the exact raw output gathered during tool execution:

```text
{self.selected_scan['stdout']}
```
"""
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(md)

            QMessageBox.information(
                self, "Report Exported",
                f"Markdown dossier successfully saved at:\n{file_path}"
            )

        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to save Markdown dossier:\n{str(e)}")

    # ========================
    # HTML Exporter
    # ========================

    def export_html(self):
        if not self.selected_scan:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save HTML Report",
            f"Kalinova_Dossier_{self.selected_scan['id']}.html",
            "HTML Files (*.html)"
        )
        if not file_path:
            return

        try:
            # Re-diagnose
            events = []
            stdout_lower = self.selected_scan["stdout"].lower()
            if "sql" in stdout_lower: events.append("SQL_INJECTION")
            if "brute" in stdout_lower or "hydra" in stdout_lower: events.append("BRUTE_FORCE")
            if "found:" in stdout_lower: events.append("DIR_ENUM")
            if "@" in stdout_lower and "." in stdout_lower: events.append("EMAIL_ENUM")
            
            ports = []
            db_ports = self.selected_scan["parsed_ports"]
            if db_ports:
                ports = [int(p) for p in db_ports.split(",") if p.strip().isdigit()]

            findings = AICopilot.diagnose(events, ports)

            # Map threat rating color
            threat_color = "#10b981" # green
            if self.selected_scan['threat_level'].upper() == "CRITICAL" or self.selected_scan['threat_level'].upper() == "HIGH":
                threat_color = "#f43f5e" # crimson
            elif self.selected_scan['threat_level'].upper() == "MEDIUM":
                threat_color = "#f59e0b" # amber

            # Build HTML content
            html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kalinova Security Assessment - {self.selected_scan['target']}</title>
    <style>
        body {{
            background-color: #0b1220;
            color: #d6e2ff;
            font-family: 'Segoe UI', -apple-system, sans-serif;
            margin: 0;
            padding: 40px 20px;
        }}
        .container {{
            max-width: 1100px;
            margin: 0 auto;
        }}
        header {{
            border-bottom: 2px solid #1c2a47;
            padding-bottom: 20px;
            margin-bottom: 40px;
        }}
        h1 {{
            color: #00f0ff;
            font-size: 28px;
            font-weight: 800;
            margin: 0 0 5px 0;
            letter-spacing: 1px;
        }}
        .subtitle {{
            color: #64748b;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .grid {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }}
        .card {{
            background-color: #0e1728;
            border: 1px solid #1c2a47;
            border-radius: 12px;
            padding: 24px;
        }}
        h2 {{
            color: #8ea2c5;
            font-size: 14px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 0;
            margin-bottom: 20px;
            border-bottom: 1px solid #1e2e4f;
            padding-bottom: 6px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        td, th {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #1e2e4f;
        }}
        th {{
            color: #8ea2c5;
            font-weight: 600;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 11px;
        }}
        .badge-threat {{
            background-color: {threat_color}20;
            color: {threat_color};
            border: 1px solid {threat_color};
        }}
        .score {{
            font-size: 32px;
            font-weight: 900;
            color: #00f0ff;
            font-family: 'Courier New', monospace;
        }}
        .vulnerability-card {{
            background-color: #121d33;
            border: 1px solid #1f3254;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }}
        .vuln-title {{
            font-size: 16px;
            font-weight: bold;
            color: #f59e0b;
            margin-top: 0;
            margin-bottom: 8px;
        }}
        .vuln-meta {{
            font-size: 11px;
            color: #8ea2c5;
            margin-bottom: 12px;
        }}
        .vuln-meta span {{
            margin-right: 15px;
        }}
        .vuln-cvss {{
            background-color: #ef444420;
            color: #f87171;
            padding: 2px 6px;
            border-radius: 4px;
            font-weight: bold;
        }}
        pre {{
            background-color: #050a12;
            border: 1px solid #14213d;
            border-radius: 6px;
            padding: 15px;
            color: #38bdf8;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            overflow-x: auto;
            margin-bottom: 15px;
        }}
        .remediation-box {{
            margin-top: 15px;
        }}
        .remediation-header {{
            color: #10b981;
            font-size: 12px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }}
        .terminal-block {{
            background-color: #03070d;
            border: 1px solid #0f1826;
            color: #94a3b8;
            font-family: 'Courier New', monospace;
            font-size: 11px;
            padding: 20px;
            border-radius: 8px;
            white-space: pre-wrap;
            overflow-y: auto;
            max-height: 400px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>KALINOVA // SECURITY DOSSIER</h1>
            <div class="subtitle">Client Penetration Testing Assessment Report</div>
        </header>

        <div class="grid">
            <div class="card">
                <h2>1. Audit Assessment Context</h2>
                <table>
                    <tr><th>Audit Property</th><th>Scanned Context Value</th></tr>
                    <tr><td>Target System Host</td><td><code>{self.selected_scan['target']}</code></td></tr>
                    <tr><td>Audit Command Path</td><td><code>{self.selected_scan['command']}</code></td></tr>
                    <tr><td>Module Executed</td><td><code>{self.selected_scan['tool_name']}</code></td></tr>
                    <tr><td>Scan Timestamp</td><td>{self.selected_scan['timestamp']}</td></tr>
                </table>
            </div>

            <div class="card" style="text-align: center; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                <h2>2. Cyber Risk Rating</h2>
                <div class="score">{self.selected_scan['risk_score']} / 100</div>
                <div style="margin-top: 10px;">
                    <span class="badge badge-threat">{self.selected_scan['threat_level']} RISK</span>
                </div>
            </div>
        </div>

        <div class="card" style="margin-bottom: 30px;">
            <h2>3. Copilot Advisories & Concrete Remediations</h2>
            
            """
            for idx, f in enumerate(findings):
                html += f"""<div class="vulnerability-card">
                <div class="vuln-title">[{idx+1}] {f['title']}</div>
                <div class="vuln-meta">
                    <span>Severity: <strong style="color: #f87171;">{f['severity']}</strong></span>
                    <span>CVSS v3 Score: <span class="vuln-cvss">{f['cvss']}</span></span>
                </div>
                <p style="margin-top: 0; color: #cbd5e1; line-height: 1.5; font-size: 13px;">{f['description']}</p>
                
                <div class="remediation-box">
                    <div class="remediation-header">● Secure Python Implementation Pattern:</div>
                    <pre>{f['remediation_python']}</pre>
                    
                    <div class="remediation-header">● Secure Node.js Implementation Pattern:</div>
                    <pre>{f['remediation_node']}</pre>
                </div>
            </div>
            """

            html += f"""
        </div>

        <div class="card">
            <h2>4. Raw Audit Terminal Log</h2>
            <div class="terminal-block">{self.selected_scan['stdout']}</div>
        </div>
    </div>
</body>
</html>
"""
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html)

            QMessageBox.information(
                self, "Report Exported",
                f"HTML dossier successfully saved at:\n{file_path}"
            )

        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to save HTML dossier:\n{str(e)}")

    # ========================
    # DB Delete Row
    # ========================

    def delete_session(self):
        if not self.selected_scan:
            return

        confirm = QMessageBox.question(
            self, "Confirm Deletion",
            f"Are you absolutely sure you want to permanently delete Scan Session {self.selected_scan['id']} from the database?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            DatabaseManager.delete_scan(self.selected_scan["id"])
            self.load_scans_from_database()
            QMessageBox.information(self, "Session Deleted", "Session permanently removed from database.")