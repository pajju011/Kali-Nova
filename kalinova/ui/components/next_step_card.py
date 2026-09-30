"""
Next-Step Action Card for Kali-Nova.
Displays context-aware security recommendations, ML scenario directives, confidence ratings, and one-click execution.
Supports both Dashboard global telemetry and In-Tool contextual recommendations.
"""

import re
from typing import Dict, Any, Optional
from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from core.ml.ml_advisor import MLAdvisor
from core.app_state import app_state
from core.suggestion_engine import SuggestionEngine


class NextStepCard(QFrame):
    """
    Interactive Cyber Widget rendering live next-step recommendations,
    confidence probability gauge, rationale badges, and one-click auto-fill workflow buttons.
    """

    # Signal: (page_name, sub_tool_key, suggested_target, suggested_flags)
    execute_step_signal = pyqtSignal(str, str, str, str)
    # Generic payload signal for main_window.handle_suggested_tool
    run_suggested_signal = pyqtSignal(str)
    # AI Drawer assistance signal
    ai_assist_requested = pyqtSignal(dict)

    def __init__(self, parent=None, active_tool_id: Optional[str] = None):
        super().__init__(parent)
        self.setObjectName("NextStepCard")
        self.active_tool_id = active_tool_id
        self.active_tool_name = ""
        self.active_target = ""
        self.current_guidance: Dict[str, Any] = {}
        self.init_ui()
        self.refresh_guidance()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(8)

        self.setStyleSheet("""
            QFrame#NextStepCard {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0d1629, stop:0.5 #09101e, stop:1 #0e192f);
                border: 1px solid #1c2e4f;
                border-left: 4px solid #00f0ff;
                border-radius: 10px;
                margin-top: 10px;
            }
            QFrame#NextStepCard:hover {
                border-color: #38bdf8;
            }
        """)

        # 1. Header Row
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)

        self.directive_tag = QLabel("⚡ RECOMMENDED NEXT STEP")
        self.directive_tag.setStyleSheet("""
            font-size: 11px;
            font-weight: 800;
            color: #00f0ff;
            letter-spacing: 1px;
        """)
        header_layout.addWidget(self.directive_tag)

        header_layout.addStretch()

        self.confidence_badge = QLabel("● LIVE DIRECTIVE")
        self.confidence_badge.setStyleSheet("""
            background-color: #052e16;
            color: #34d399;
            font-size: 10px;
            font-weight: 800;
            padding: 3px 10px;
            border-radius: 10px;
            border: 1px solid #059669;
            letter-spacing: 0.5px;
        """)
        header_layout.addWidget(self.confidence_badge)

        layout.addLayout(header_layout)

        # 2. Main Action Title
        self.action_title_label = QLabel("Analyzing next testing phase...")
        self.action_title_label.setStyleSheet("font-size: 14px; font-weight: 800; color: #f8fafc; letter-spacing: 0.2px;")
        self.action_title_label.setWordWrap(True)
        layout.addWidget(self.action_title_label)

        # 3. Action Description & Insets
        self.action_desc_label = QLabel("Recommended action based on active target surface and scan output.")
        self.action_desc_label.setStyleSheet("font-size: 11px; color: #94a3b8; line-height: 1.3;")
        self.action_desc_label.setWordWrap(True)
        layout.addWidget(self.action_desc_label)

        # Inset Box for Tactical Rationale
        self.rationale_frame = QFrame()
        self.rationale_frame.setStyleSheet("""
            QFrame {
                background-color: #060b14;
                border: 1px solid #142238;
                border-left: 3px solid #38bdf8;
                border-radius: 6px;
                padding: 4px;
            }
        """)
        rationale_layout = QVBoxLayout(self.rationale_frame)
        rationale_layout.setContentsMargins(8, 6, 8, 6)
        rationale_layout.setSpacing(2)

        self.rationale_hdr = QLabel("💡 STRATEGIC RATIONALE & CONTEXT")
        self.rationale_hdr.setStyleSheet("font-size: 9px; font-weight: 800; color: #38bdf8; letter-spacing: 0.5px;")
        rationale_layout.addWidget(self.rationale_hdr)

        self.rationale_label = QLabel("Execute port or service discovery to identify reachable attack surfaces.")
        self.rationale_label.setStyleSheet("font-size: 11px; color: #cbd5e1;")
        self.rationale_label.setWordWrap(True)
        rationale_layout.addWidget(self.rationale_label)
        layout.addWidget(self.rationale_frame)

        # 4. Action Button Bar
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)

        self.execute_btn = QPushButton("⚡ Launch Recommended Next Step")
        self.execute_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.execute_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0284c7, stop:1 #2563eb);
                color: #ffffff;
                font-weight: 800;
                font-size: 12px;
                padding: 8px 18px;
                border-radius: 6px;
                border: 1px solid #38bdf8;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0ea5e9, stop:1 #3b82f6);
                border: 1px solid #7dd3fc;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
        """)
        self.execute_btn.clicked.connect(self.on_execute_clicked)
        btn_layout.addWidget(self.execute_btn, 3)

        self.ai_btn = QPushButton("✨ AI Diagnostic")
        self.ai_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ai_btn.setStyleSheet("""
            QPushButton {
                background-color: #0c1c33;
                color: #38bdf8;
                font-size: 11px;
                font-weight: 700;
                padding: 8px 12px;
                border-radius: 6px;
                border: 1px solid #0284c7;
            }
            QPushButton:hover {
                background-color: #0284c7;
                color: #ffffff;
            }
        """)
        self.ai_btn.clicked.connect(self.on_ai_clicked)
        btn_layout.addWidget(self.ai_btn, 1)

        self.refresh_btn = QPushButton("🔄")
        self.refresh_btn.setToolTip("Refresh live scenario recommendation")
        self.refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #111c30;
                color: #94a3b8;
                font-size: 12px;
                font-weight: 600;
                padding: 8px 12px;
                border-radius: 6px;
                border: 1px solid #1e2f4f;
            }
            QPushButton:hover {
                background-color: #172642;
                color: #f1f5f9;
                border-color: #38bdf8;
            }
        """)
        self.refresh_btn.clicked.connect(self.refresh_guidance)
        btn_layout.addWidget(self.refresh_btn, 0)

        layout.addLayout(btn_layout)

    def set_active_tool(self, tool_id: str, tool_name: str = "", active_target: str = ""):
        """Sets active tool and target context to generate tailored next-step advice."""
        self.active_tool_id = tool_id.lower().strip() if tool_id else None
        self.active_tool_name = tool_name or tool_id or ""
        if active_target:
            self.active_target = active_target.strip()
        self.refresh_guidance()

    def set_target(self, target: str):
        """Updates active target host/URL."""
        if target:
            self.active_target = target.strip()
            self.refresh_guidance()

    def _compute_tool_specific_guidance(self) -> Dict[str, Any]:
        """Calculates precise cybersecurity next-step recommendations based on tool and state."""
        tid = (self.active_tool_id or "").lower()
        target = self.active_target or getattr(app_state, "next_target", "") or "127.0.0.1"
        clean_target = target.replace("http://", "").replace("https://", "").split("/")[0].split(":")[0]

        # 1. SQLmap Guidance
        if "sqlmap" in tid:
            if "SQL_INJECTION" in app_state.events:
                return {
                    "tool_name": "SQLmap Advanced Extraction",
                    "action_title": "Enumerate Database Schema & Extract Tables",
                    "action_desc": f"SQL Injection confirmed on target. Next step: Dump database schema and extract user credentials.",
                    "rationale": "Vulnerability validated. Proceed to database enumeration using --dbs, --tables, and --dump.",
                    "page": "web_page",
                    "sub_tool": "sqlmap",
                    "suggested_target": target,
                    "suggested_flags": "--dbs --batch",
                    "confidence": 98.0
                }
            else:
                return {
                    "tool_name": "Nikto Web Vulnerability Scan",
                    "action_title": "Discover Web Endpoints & Injectable Parameters",
                    "action_desc": f"If SQLmap encounters connection refusal or lacks parameters, perform a web crawl to discover valid endpoints.",
                    "rationale": f"SQLmap requires reachable HTTP services and parameters (e.g. ?id=1). Scan {clean_target} with Nikto/Nmap first.",
                    "page": "web_page",
                    "sub_tool": "nikto",
                    "suggested_target": f"http://{clean_target}" if not target.startswith("http") else target,
                    "suggested_flags": "-h",
                    "confidence": 92.0
                }

        # 2. Nmap Guidance
        if "nmap" in tid:
            if any(p in app_state.open_ports for p in [80, 443, 8080, 8000, 8443]):
                return {
                    "tool_name": "Nikto / Gobuster Web Audit",
                    "action_title": "Scan Discovered Web Server Ports (80/443)",
                    "action_desc": f"Nmap identified open HTTP/HTTPS ports on {clean_target}. Initiate web server vulnerability and directory inspection.",
                    "rationale": "Exposed web ports represent primary entry vectors. Crawl for known CVEs and directories.",
                    "page": "web_page",
                    "sub_tool": "nikto",
                    "suggested_target": f"http://{clean_target}",
                    "suggested_flags": "",
                    "confidence": 95.0
                }
            elif any(p in app_state.open_ports for p in [21, 22, 3306, 5432, 3389]):
                return {
                    "tool_name": "Hydra Network Authentication Audit",
                    "action_title": "Audit Credential Strength on Exposed Services",
                    "action_desc": f"Nmap detected open authentication ports. Test credential resilience using Hydra dictionary spray.",
                    "rationale": "Default or weak administrative credentials are a frequent vulnerability on exposed management ports.",
                    "page": "auth_page",
                    "sub_tool": "hydra",
                    "suggested_target": clean_target,
                    "suggested_flags": "",
                    "confidence": 90.0
                }
            else:
                return {
                    "tool_name": "Nikto Web Scanner",
                    "action_title": "Launch Web Application Security Audit",
                    "action_desc": f"Audit {clean_target} for outdated server software, dangerous files, and security misconfigurations.",
                    "rationale": "Comprehensive scanning combines port intelligence with protocol-level tests.",
                    "page": "web_page",
                    "sub_tool": "nikto",
                    "suggested_target": f"http://{clean_target}",
                    "suggested_flags": "",
                    "confidence": 88.0
                }

        # 3. Nikto Guidance
        if "nikto" in tid:
            return {
                "tool_name": "Gobuster Directory Fuzzer",
                "action_title": "Brute-Force Hidden Directories & Admin Panels",
                "action_desc": f"Nikto identified server profile. Next phase: Fuzz hidden directories, backup files, and API routes on {clean_target}.",
                "rationale": "Hidden administrative endpoints and unindexed paths often bypass frontend authentication controls.",
                "page": "web_page",
                "sub_tool": "gobuster",
                "suggested_target": f"http://{clean_target}",
                "suggested_flags": "",
                "confidence": 93.0
            }

        # 4. Gobuster / Wfuzz Guidance
        if "gobuster" in tid or "wfuzz" in tid:
            return {
                "tool_name": "SQLmap Injection Testing",
                "action_title": "Test Discovered Endpoints for SQL Injection",
                "action_desc": f"Fuzzing revealed active URI routes. Test input fields and query parameters on {clean_target} with SQLmap.",
                "rationale": "Dynamic web endpoints often process user queries with backend databases.",
                "page": "web_page",
                "sub_tool": "sqlmap",
                "suggested_target": f"http://{clean_target}/index.php?id=1",
                "suggested_flags": "--batch",
                "confidence": 91.0
            }

        # 5. Hydra / John / Hashcat / Ncrack Guidance
        if any(k in tid for k in ["hydra", "john", "hashcat", "ncrack"]):
            return {
                "tool_name": "Netcat Banner & Port Verification",
                "action_title": "Verify Service Access & Privilege Boundaries",
                "action_desc": f"Audit authenticated connection parameters and verify banner response on {clean_target}.",
                "rationale": "Following authentication checks, verify valid access controls and network segment boundaries.",
                "page": "network_page",
                "sub_tool": "netcat",
                "suggested_target": clean_target,
                "suggested_flags": "",
                "confidence": 89.0
            }

        # 6. Network & Wireless (Wireshark / Wifite / Wash / Reaver)
        if any(k in tid for k in ["wireshark", "wifite", "wash", "reaver", "sparrow"]):
            return {
                "tool_name": "Hashcat WPA/WPS Recovery",
                "action_title": "Process Captured Handshake & Wireless Cryptography",
                "action_desc": "Analyze captured wireless packets or PINs for cryptographic weaknesses and key recovery.",
                "rationale": "Offline recovery avoids radio noise and leverages hardware-accelerated dictionary rules.",
                "page": "auth_page",
                "sub_tool": "hashcat",
                "suggested_target": "",
                "suggested_flags": "-m 22000",
                "confidence": 90.0
            }

        # 7. Recon & OSINT (Whois / theHarvester / Metagoofil / Amass)
        if any(k in tid for k in ["whois", "harvester", "theharvester", "metagoofil", "amass", "photon"]):
            return {
                "tool_name": "Nmap Port Scanner",
                "action_title": "Scan Discovered Host Infrastructure & IPs",
                "action_desc": f"OSINT reconnaissance registered target domains. Next step: Run full port scan on {clean_target}.",
                "rationale": "Transitioning from passive reconnaissance to active network enumeration identifies actionable attack surfaces.",
                "page": "recon_page",
                "sub_tool": "nmap",
                "suggested_target": clean_target,
                "suggested_flags": "-sV -Pn",
                "confidence": 94.0
            }

        # Fallback to ML Advisor
        return MLAdvisor.get_guidance()

    def refresh_guidance(self):
        """Re-evaluates scenario guidance and updates UI elements."""
        if self.active_tool_id:
            self.current_guidance = self._compute_tool_specific_guidance()
        else:
            self.current_guidance = MLAdvisor.get_guidance()

        conf = self.current_guidance.get("confidence", 88.0)
        tool_name = self.current_guidance.get("tool_name", "Security Tool")
        action_title = self.current_guidance.get("action_title", "Recommended Security Action")
        action_desc = self.current_guidance.get("action_desc", "")
        rationale = self.current_guidance.get("rationale", "")

        self.confidence_badge.setText(f"● {conf}% CONFIDENCE")
        if conf >= 90:
            self.confidence_badge.setStyleSheet("background-color: #052e16; color: #34d399; font-size: 10px; font-weight: 800; padding: 3px 10px; border-radius: 10px; border: 1px solid #059669;")
        elif conf >= 70:
            self.confidence_badge.setStyleSheet("background-color: #451a03; color: #fbbf24; font-size: 10px; font-weight: 800; padding: 3px 10px; border-radius: 10px; border: 1px solid #d97706;")
        else:
            self.confidence_badge.setStyleSheet("background-color: #1e1b4b; color: #a5b4fc; font-size: 10px; font-weight: 800; padding: 3px 10px; border-radius: 10px; border: 1px solid #6366f1;")

        self.action_title_label.setText(f"{action_title} ({tool_name})")
        self.action_desc_label.setText(action_desc)
        self.rationale_label.setText(rationale)
        self.execute_btn.setText(f"⚡ Launch Next Step: {tool_name}")

    def on_execute_clicked(self):
        """Emits signal to switch to target tool page with pre-populated parameters."""
        page = self.current_guidance.get("page", "recon_page")
        sub_tool = self.current_guidance.get("sub_tool", "nmap")
        target = self.current_guidance.get("suggested_target", self.active_target or "127.0.0.1")
        flags = self.current_guidance.get("suggested_flags", "")

        # Emit both granular and pipe-delimited signals
        self.execute_step_signal.emit(page, sub_tool, target, flags)
        payload = f"{sub_tool}|{target}|{flags}" if (target or flags) else sub_tool
        self.run_suggested_signal.emit(payload)

    def on_ai_clicked(self):
        """Emits AI assistance request for the current recommendation."""
        ctx = {
            "tool_id": self.active_tool_id or "general",
            "tool_name": self.active_tool_name or "Security Tool",
            "target": self.active_target,
            "guidance": self.current_guidance
        }
        self.ai_assist_requested.emit(ctx)

