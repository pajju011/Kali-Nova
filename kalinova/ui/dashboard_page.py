import sys
import os
import random
from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QFrame, QTextEdit, QLineEdit, QProgressBar, QToolTip
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QCursor
from core.app_state import app_state
from ui.topology_widget import NetworkTopologyWidget
from core.ai_copilot import AICopilot, AIWorkerThread


class DashboardPage(QWidget):

    # Signal to notify MainWindow which tool to run (composite format: tool|target|flags)
    run_suggested_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setObjectName("dashboardPageContainer")
        self.uptime_seconds = 0
        self.ai_worker = None
        self._last_state_fingerprint = None

        # Custom Premium Cyber StyleSheets
        self.setStyleSheet("""
            QWidget#dashboardPageContainer {
                background-color: #070c18;
            }
            
            QFrame.hudCard {
                background-color: #0b1426;
                border: 1px solid #162744;
                border-radius: 12px;
            }
            
            QFrame.hudCard:hover {
                border-color: #38bdf8;
            }
            
            QLabel#hudCardTitle {
                color: #8ea2c5;
                font-family: 'Segoe UI', sans-serif;
                font-size: 11px;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 1px;
                padding-bottom: 4px;
                border-bottom: 1px solid #14243f;
            }
            
            QLabel#telemetryValue {
                font-family: 'Courier New', 'Consolas', monospace;
                font-size: 22px;
                font-weight: 800;
                color: #00f0ff;
            }
            
            QLabel#telemetryUnit {
                font-family: 'Segoe UI', sans-serif;
                font-size: 10px;
                font-weight: 600;
                color: #64748b;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            QPushButton.portChipOpen {
                background-color: #062e1e;
                color: #34d399;
                border: 1px solid #059669;
                border-radius: 8px;
                font-weight: 800;
                font-family: 'Courier New', 'Consolas', monospace;
                font-size: 10px;
                padding: 8px 4px;
                text-align: center;
            }
            QPushButton.portChipOpen:hover {
                background-color: #0a4730;
                border-color: #10b981;
            }
            
            QPushButton.portChipClosed {
                background-color: #0a1120;
                color: #475569;
                border: 1px solid #162238;
                border-radius: 8px;
                font-weight: 700;
                font-family: 'Courier New', 'Consolas', monospace;
                font-size: 10px;
                padding: 8px 4px;
                text-align: center;
            }
            QPushButton.portChipClosed:hover {
                background-color: #111d33;
                border-color: #38bdf8;
                color: #94a3b8;
            }
            
            QPushButton#actionBtn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0284c7, stop:1 #2563eb);
                color: #ffffff;
                font-weight: 800;
                font-size: 12px;
                padding: 8px 16px;
                border-radius: 8px;
                border: 1px solid #38bdf8;
            }
            QPushButton#actionBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0ea5e9, stop:1 #3b82f6);
            }
            QPushButton#actionBtn:disabled {
                background-color: #111a2c;
                border: 1px solid #1c2b44;
                color: #475569;
            }
            
            QPushButton.quickChip {
                background-color: #0f1c33;
                color: #93c5fd;
                border: 1px solid #1e355b;
                border-radius: 6px;
                padding: 4px 8px;
                font-size: 10px;
                font-weight: 700;
            }
            QPushButton.quickChip:hover {
                background-color: #1d355e;
                color: #ffffff;
                border-color: #38bdf8;
            }
            
            QProgressBar.hudProgress {
                border: 1px solid #162640;
                border-radius: 4px;
                background-color: #070d1a;
                text-align: center;
                min-height: 8px;
                max-height: 8px;
            }
            QProgressBar.hudProgress::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00f0ff, stop:1 #3b82f6);
                border-radius: 3px;
            }
        """)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 16, 20, 16)
        main_layout.setSpacing(14)

        # =====================================================================
        # 1. CYBERNETIC STATUS DECK (HEADER)
        # =====================================================================
        header_frame = QFrame()
        header_frame.setObjectName("hudHeader")
        header_frame.setStyleSheet("""
            QFrame#hudHeader {
                background-color: #0b1426;
                border: 1px solid #162744;
                border-radius: 12px;
                padding: 10px;
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(16, 10, 16, 10)

        title_layout = QVBoxLayout()
        self.hud_title = QLabel("▲ KALINOVA // SECURITY OPERATIONS DECK")
        self.hud_title.setStyleSheet("font-size: 18px; font-weight: 800; color: #00f0ff; letter-spacing: 1px;")
        
        self.hud_subtitle = QLabel("REAL-TIME ATTACK SURFACE DISCOVERY")
        self.hud_subtitle.setStyleSheet("font-size: 10px; font-weight: 700; color: #64748b; letter-spacing: 0.5px;")
        
        title_layout.addWidget(self.hud_title)
        title_layout.addWidget(self.hud_subtitle)

        # Right Header Metadata Panel
        meta_layout = QHBoxLayout()
        meta_layout.setSpacing(14)
        
        # System clock
        self.system_time_label = QLabel("SYSTEM TIME: 00:00:00")
        self.system_time_label.setStyleSheet("font-family: 'Courier New', monospace; font-size: 11px; font-weight: 700; color: #8ea2c5;")
        
        # System uptime
        self.system_uptime_label = QLabel("UPTIME: 00:00:00")
        self.system_uptime_label.setStyleSheet("font-family: 'Courier New', monospace; font-size: 11px; font-weight: 700; color: #8ea2c5;")

        # Active telemetry indicator
        self.beacon_label = QLabel("● CORE ONLINE")
        self.beacon_label.setStyleSheet("color: #34d399; font-weight: 800; font-size: 11px; padding: 3px 8px; border: 1px solid #059669; border-radius: 6px; background: #052e16;")

        meta_layout.addWidget(self.system_time_label)
        meta_layout.addWidget(self.system_uptime_label)
        meta_layout.addWidget(self.beacon_label)

        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addLayout(meta_layout)

        main_layout.addWidget(header_frame)

        # =====================================================================
        # 2. BENTO GRID WIDGETS LAYOUT (2x3 Grid)
        # =====================================================================
        grid_layout = QGridLayout()
        grid_layout.setSpacing(14)

        # --- PANEL A: THREAT RADAR GAUGE (Row 0, Col 0) ---
        self.threat_card = QFrame()
        self.threat_card.setProperty("class", "hudCard")
        threat_layout = QVBoxLayout(self.threat_card)
        threat_layout.setContentsMargins(16, 14, 16, 14)
        threat_layout.setSpacing(8)

        threat_title = QLabel("Threat Radar Gauge")
        threat_title.setObjectName("hudCardTitle")
        
        self.radar_risk_readout = QLabel("LOW HAZARD LEVEL")
        self.radar_risk_readout.setStyleSheet("font-size: 16px; font-weight: 800; color: #34d399;")

        # Modern graphical progress meter
        self.threat_bar = QProgressBar()
        self.threat_bar.setProperty("class", "hudProgress")
        self.threat_bar.setRange(0, 100)
        self.threat_bar.setValue(0)
        self.threat_bar.setTextVisible(False)
        self.threat_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #162744;
                border-radius: 4px;
                background-color: #070d18;
                min-height: 10px;
                max-height: 10px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #10b981, stop:1 #34d399);
                border-radius: 3px;
            }
        """)

        self.radar_segments = QLabel("Risk Exposure: Baseline (0/100)")
        self.radar_segments.setStyleSheet("font-size: 11px; color: #94a3b8;")
        
        self.radar_score_label = QLabel("Threat Score: 0 / 100")
        self.radar_score_label.setStyleSheet("font-size: 12px; font-weight: 800; color: #38bdf8;")

        self.quick_audit_btn = QPushButton("🛡️ Deep Vulnerability Diagnostic")
        self.quick_audit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.quick_audit_btn.setStyleSheet("""
            QPushButton {
                background-color: #0d1a30;
                color: #38bdf8;
                border: 1px solid #1e355b;
                border-radius: 6px;
                padding: 6px;
                font-size: 11px;
                font-weight: 700;
            }
            QPushButton:hover {
                background-color: #172a4d;
                border-color: #00f0ff;
                color: #ffffff;
            }
        """)
        self.quick_audit_btn.clicked.connect(self._run_quick_vulnerability_audit)

        threat_layout.addWidget(threat_title)
        threat_layout.addWidget(self.radar_risk_readout)
        threat_layout.addWidget(self.threat_bar)
        threat_layout.addWidget(self.radar_score_label)
        threat_layout.addWidget(self.radar_segments)
        threat_layout.addWidget(self.quick_audit_btn)
        threat_layout.addStretch()

        # --- PANEL B: LIVE NETWORK PORT SCAN MATRIX (Row 0, Col 1) ---
        self.ports_card = QFrame()
        self.ports_card.setProperty("class", "hudCard")
        ports_layout = QVBoxLayout(self.ports_card)
        ports_layout.setContentsMargins(16, 14, 16, 14)
        ports_layout.setSpacing(8)

        ports_header = QHBoxLayout()
        ports_title = QLabel("Live Network Port Matrix")
        ports_title.setObjectName("hudCardTitle")
        ports_hint = QLabel("(Click port to audit)")
        ports_hint.setStyleSheet("font-size: 9px; color: #64748b; font-weight: 600;")
        ports_header.addWidget(ports_title)
        ports_header.addStretch()
        ports_header.addWidget(ports_hint)
        ports_layout.addLayout(ports_header)

        # 2x4 Grid layout for ports with interactive buttons
        self.ports_grid_widget = QWidget()
        self.ports_grid = QGridLayout(self.ports_grid_widget)
        self.ports_grid.setContentsMargins(0, 4, 0, 0)
        self.ports_grid.setSpacing(8)

        # Target ports to monitor
        self.monitored_ports = [
            (21, "FTP"), (22, "SSH"), (80, "HTTP"), (443, "HTTPS"),
            (3306, "MySQL"), (8080, "HTTP-Alt"), (9000, "FastCGI"), (993, "IMAPS")
        ]
        self.port_cells = {}

        for idx, (port, service) in enumerate(self.monitored_ports):
            row = idx // 4
            col = idx % 4
            cell_btn = QPushButton(f"{service} : {port}\n[CLOSED]")
            cell_btn.setProperty("class", "portChipClosed")
            cell_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            cell_btn.setToolTip(f"Click to audit service on Port {port} ({service})")
            cell_btn.clicked.connect(lambda _, p=port, s=service: self._on_port_clicked(p, s))
            self.ports_grid.addWidget(cell_btn, row, col)
            self.port_cells[port] = (cell_btn, service)

        ports_layout.addWidget(self.ports_grid_widget)
        ports_layout.addStretch()

        # --- PANEL C: INTERACTIVE RADAR TOPOLOGY (Row 0, Col 2) ---
        self.topology_card = QFrame()
        self.topology_card.setProperty("class", "hudCard")
        topo_layout = QVBoxLayout(self.topology_card)
        topo_layout.setContentsMargins(16, 14, 16, 14)
        topo_layout.setSpacing(6)

        topo_title = QLabel("Network Topology Sweep")
        topo_title.setObjectName("hudCardTitle")

        self.topology_widget = NetworkTopologyWidget()

        topo_layout.addWidget(topo_title)
        topo_layout.addWidget(self.topology_widget, 1)

        # --- PANEL D: CORE HARDWARE & SCANNER TELEMETRY (Row 1, Col 0) ---
        self.telemetry_card = QFrame()
        self.telemetry_card.setProperty("class", "hudCard")
        telemetry_layout = QVBoxLayout(self.telemetry_card)
        telemetry_layout.setContentsMargins(16, 14, 16, 14)
        telemetry_layout.setSpacing(8)

        telemetry_title = QLabel("Core Hardware & Scanner Telemetry")
        telemetry_title.setObjectName("hudCardTitle")
        telemetry_layout.addWidget(telemetry_title)

        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(12)

        # Metric 1: Core load
        cpu_box = QVBoxLayout()
        self.cpu_val = QLabel("42.8%")
        self.cpu_val.setObjectName("telemetryValue")
        cpu_lbl = QLabel("Hacking Core")
        cpu_lbl.setObjectName("telemetryUnit")
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setProperty("class", "hudProgress")
        self.cpu_bar.setRange(0, 100)
        self.cpu_bar.setValue(42)
        self.cpu_bar.setTextVisible(False)
        cpu_box.addWidget(self.cpu_val)
        cpu_box.addWidget(cpu_lbl)
        cpu_box.addWidget(self.cpu_bar)

        # Metric 2: Network Bandwidth
        bw_box = QVBoxLayout()
        self.bw_val = QLabel("482 KB/s")
        self.bw_val.setObjectName("telemetryValue")
        self.bw_val.setStyleSheet("color: #a855f7;")
        bw_lbl = QLabel("Bandwidth")
        bw_lbl.setObjectName("telemetryUnit")
        self.bw_bar = QProgressBar()
        self.bw_bar.setProperty("class", "hudProgress")
        self.bw_bar.setRange(0, 1000)
        self.bw_bar.setValue(482)
        self.bw_bar.setTextVisible(False)
        bw_box.addWidget(self.bw_val)
        bw_box.addWidget(bw_lbl)
        bw_box.addWidget(self.bw_bar)

        # Metric 3: Active threads
        thread_box = QVBoxLayout()
        self.thread_val = QLabel("12 Active")
        self.thread_val.setObjectName("telemetryValue")
        self.thread_val.setStyleSheet("color: #3b82f6;")
        thread_lbl = QLabel("Run Threads")
        thread_lbl.setObjectName("telemetryUnit")
        self.thread_bar = QProgressBar()
        self.thread_bar.setProperty("class", "hudProgress")
        self.thread_bar.setRange(0, 32)
        self.thread_bar.setValue(12)
        self.thread_bar.setTextVisible(False)
        thread_box.addWidget(self.thread_val)
        thread_box.addWidget(thread_lbl)
        thread_box.addWidget(self.thread_bar)

        metrics_layout.addLayout(cpu_box)
        metrics_layout.addLayout(bw_box)
        metrics_layout.addLayout(thread_box)

        telemetry_layout.addLayout(metrics_layout)
        telemetry_layout.addStretch()

        # --- PANEL E: TARGET CONTROLLER & ATTACK SURFACE INTEL (Row 1, Col 1) ---
        self.action_card = QFrame()
        self.action_card.setProperty("class", "hudCard")
        action_layout = QVBoxLayout(self.action_card)
        action_layout.setContentsMargins(16, 14, 16, 14)
        action_layout.setSpacing(6)

        action_title = QLabel("Target Controller & Surface Intel")
        action_title.setObjectName("hudCardTitle")
        action_layout.addWidget(action_title)

        # Target Quick-Editor Row
        target_box = QHBoxLayout()
        target_lbl = QLabel("Target:")
        target_lbl.setStyleSheet("font-size: 11px; font-weight: 700; color: #8ea2c5;")
        self.target_input = QLineEdit("")
        self.target_input.setPlaceholderText("Enter target IP or domain (e.g. 192.168.1.1)...")
        self.target_input.setStyleSheet("""
            QLineEdit {
                background-color: #070d18;
                border: 1px solid #1e355b;
                border-radius: 6px;
                color: #00f0ff;
                padding: 5px 8px;
                font-size: 11px;
                font-family: 'Courier New', monospace;
                font-weight: bold;
            }
            QLineEdit:focus {
                border-color: #00f0ff;
            }
        """)
        self.target_input.textChanged.connect(self._on_target_changed)
        target_box.addWidget(target_lbl)
        target_box.addWidget(self.target_input)
        action_layout.addLayout(target_box)

        self.suggestion_label = QLabel("[SYS_INTEL] Standing by. Enter a target IP address or domain above to receive AI scenario directives.")
        self.suggestion_label.setWordWrap(True)
        self.suggestion_label.setStyleSheet("font-size: 11px; color: #94a3b8; line-height: 1.3;")
        action_layout.addWidget(self.suggestion_label)

        self.next_tool_label = QLabel("DIRECTIVE: STANDBY (Enter Target)")
        self.next_tool_label.setStyleSheet("font-size: 11px; font-weight: 800; color: #00f0ff;")
        action_layout.addWidget(self.next_tool_label)

        self.run_suggested_btn = QPushButton("⚡ Execute Directive (Enter Target to Begin)")
        self.run_suggested_btn.setObjectName("actionBtn")
        self.run_suggested_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.run_suggested_btn.setEnabled(False)
        self.run_suggested_btn.clicked.connect(self.run_suggested_tool)
        action_layout.addWidget(self.run_suggested_btn)
        action_layout.addStretch()

        # --- PANEL F: AI COPILOT INFRASTRUCTURE (Row 1, Col 2) ---
        self.copilot_card = QFrame()
        self.copilot_card.setProperty("class", "hudCard")
        copilot_layout = QVBoxLayout(self.copilot_card)
        copilot_layout.setContentsMargins(16, 14, 16, 14)
        copilot_layout.setSpacing(6)

        copilot_header = QHBoxLayout()
        copilot_title = QLabel("AI Copilot Advisory")
        copilot_title.setObjectName("hudCardTitle")
        
        self.ai_status_dot = QLabel("● READY")
        self.ai_status_dot.setStyleSheet("color: #34d399; font-size: 10px; font-weight: 800;")
        copilot_header.addWidget(copilot_title)
        copilot_header.addStretch()
        copilot_header.addWidget(self.ai_status_dot)

        self.copilot_output = QTextEdit()
        self.copilot_output.setReadOnly(True)
        self.copilot_output.setStyleSheet("""
            QTextEdit {
                background-color: #060c18;
                color: #34d399;
                font-family: 'Courier New', monospace;
                font-size: 11px;
                border: 1px solid #142238;
                border-radius: 8px;
                padding: 6px;
            }
        """)
        self.copilot_output.setText("Initializing security scan diagnostics...\nStanding by for AI copilot queries.")

        # Quick AI Suggestion Chips
        chips_row = QHBoxLayout()
        chips_row.setSpacing(6)
        chip_sqli = QPushButton("💉 SQLi Patch")
        chip_sqli.setProperty("class", "quickChip")
        chip_sqli.setCursor(Qt.CursorShape.PointingHandCursor)
        chip_sqli.clicked.connect(lambda: self._quick_prompt("How to patch SQL injection vulnerabilities in Python and Node.js?"))

        chip_recon = QPushButton("🔍 Recon Strategy")
        chip_recon.setProperty("class", "quickChip")
        chip_recon.setCursor(Qt.CursorShape.PointingHandCursor)
        chip_recon.clicked.connect(lambda: self._quick_prompt("What is the optimal reconnaissance sequence for this target?"))

        chip_ports = QPushButton("🛡️ Port Hardening")
        chip_ports.setProperty("class", "quickChip")
        chip_ports.setCursor(Qt.CursorShape.PointingHandCursor)
        chip_ports.clicked.connect(lambda: self._quick_prompt("How to securely harden discovered open ports and firewall daemons?"))

        chips_row.addWidget(chip_sqli)
        chips_row.addWidget(chip_recon)
        chips_row.addWidget(chip_ports)

        prompt_layout = QHBoxLayout()
        self.ai_prompt_input = QLineEdit()
        self.ai_prompt_input.setPlaceholderText("Ask AI Copilot (e.g. How to patch SQLi?)...")
        self.ai_prompt_input.setStyleSheet("""
            QLineEdit {
                background-color: #0b1424;
                border: 1px solid #1e2e4a;
                border-radius: 6px;
                color: #e2e8f0;
                padding: 6px;
                font-size: 11px;
            }
        """)
        self.ai_prompt_input.returnPressed.connect(self.run_ai_analysis)

        self.ask_ai_btn = QPushButton("Ask AI")
        self.ask_ai_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ask_ai_btn.setStyleSheet("""
            QPushButton {
                background-color: #00f0ff;
                color: #070c18;
                font-weight: 800;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 11px;
                border: none;
            }
            QPushButton:hover {
                background-color: #38bdf8;
            }
        """)
        self.ask_ai_btn.clicked.connect(self.run_ai_analysis)

        prompt_layout.addWidget(self.ai_prompt_input)
        prompt_layout.addWidget(self.ask_ai_btn)

        copilot_layout.addLayout(copilot_header)
        copilot_layout.addWidget(self.copilot_output, 1)
        copilot_layout.addLayout(chips_row)
        copilot_layout.addLayout(prompt_layout)

        # Place panels in Bento Grid
        grid_layout.addWidget(self.threat_card, 0, 0, 1, 1)
        grid_layout.addWidget(self.ports_card, 0, 1, 1, 1)
        grid_layout.addWidget(self.topology_card, 0, 2, 1, 1)
        grid_layout.addWidget(self.telemetry_card, 1, 0, 1, 1)
        grid_layout.addWidget(self.action_card, 1, 1, 1, 1)
        grid_layout.addWidget(self.copilot_card, 1, 2, 1, 1)

        # Grid Stretch Settings
        grid_layout.setRowStretch(0, 1)
        grid_layout.setRowStretch(1, 1)
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 1)
        grid_layout.setColumnStretch(2, 1)

        main_layout.addLayout(grid_layout)

        self.setLayout(main_layout)

        # Dynamic update timer (1 second ticks)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_dashboard)
        self.timer.start(1000)

        # Load initial diagnostic findings
        self._load_initial_diagnostics()

    def _load_initial_diagnostics(self):
        findings = AICopilot.diagnose(app_state.events, app_state.open_ports)
        advice_parts = []
        for f in findings[:2]:
            advice_parts.append(f"● {f['title']} [{f['severity']}]\n  {f['description']}")
        
        if advice_parts:
            self.copilot_output.setText("\n\n".join(advice_parts))

    def _on_target_changed(self, new_target: str):
        cleaned = new_target.strip()
        if cleaned:
            app_state.next_target = cleaned
            if not app_state.pipeline_artifacts.get("targets"):
                app_state.pipeline_artifacts["targets"] = [cleaned]
            else:
                app_state.pipeline_artifacts["targets"][0] = cleaned
        else:
            app_state.next_target = None
            if app_state.pipeline_artifacts.get("targets"):
                app_state.pipeline_artifacts["targets"].clear()
            app_state.clear_next_action()

    def _on_port_clicked(self, port: int, service: str):
        """Routes directly to relevant security tool when user clicks a port chip."""
        target = self.target_input.text().strip() or "127.0.0.1"
        if port in (80, 8080):
            self.run_suggested_signal.emit(f"nikto|http://{target}:{port}|")
        elif port == 443:
            self.run_suggested_signal.emit(f"sslscan|{target}|")
        elif port == 22:
            self.run_suggested_signal.emit(f"hydra|{target}|-s 22")
        elif port == 21:
            self.run_suggested_signal.emit(f"hydra|{target}|-s 21")
        elif port == 3306:
            self.run_suggested_signal.emit(f"sqlmap|http://{target}:3306|")
        else:
            self.run_suggested_signal.emit(f"nmap|{target}|-p {port} -sV")

    def _run_quick_vulnerability_audit(self):
        """Runs instant Copilot vulnerability breakdown."""
        findings = AICopilot.diagnose(app_state.events, app_state.open_ports)
        lines = [f"🛡️ [VULNERABILITY AUDIT REPORT - THREAT LEVEL: {app_state.global_risk}]"]
        lines.append(f"Open Port Surface: {app_state.open_ports or 'None detected yet'}")
        lines.append(f"Detected Events: {app_state.events or 'No high-risk signatures'}\n")
        for f in findings:
            title = f.get("title", "Security Finding")
            sev = f.get("severity", "LOW")
            cvss = f.get("cvss", f.get("cvss_score", 3.0))
            desc = f.get("description", "")
            rem = f.get("remediation", "")
            if not rem:
                rem_code = f.get("remediation_python", "")
                if rem_code:
                    lines_code = [l.lstrip("#/ ").strip() for l in rem_code.splitlines() if l.startswith(("#", "//"))]
                    rem = " ".join(lines_code[:2]) if lines_code else "Apply security hardening patches."
                else:
                    rem = "Apply defensive configuration patches."
            lines.append(f"● {title} [{sev} - {cvss} CVSS]\n  {desc}\n  Remediation: {rem}\n")
        self.copilot_output.setText("\n".join(lines))
        self.ai_status_dot.setText("● AUDIT DONE")
        self.ai_status_dot.setStyleSheet("color: #00f0ff; font-size: 10px; font-weight: 800;")

    def _quick_prompt(self, text: str):
        self.ai_prompt_input.setText(text)
        self.run_ai_analysis()

    # ========================
    # Update Dashboard Data
    # ========================

    def update_dashboard(self):
        # 1. Update system Uptime and Time
        self.uptime_seconds += 1
        hours = self.uptime_seconds // 3600
        minutes = (self.uptime_seconds % 3600) // 60
        seconds = self.uptime_seconds % 60
        self.system_uptime_label.setText(f"UPTIME: {hours:02d}:{minutes:02d}:{seconds:02d}")
        
        current_time = datetime.now().strftime("%H:%M:%S")
        self.system_time_label.setText(f"SYSTEM TIME: {current_time}")

        # 2. Pulsing online beacon
        if self.uptime_seconds % 2 == 0:
            self.beacon_label.setText("● CORE ONLINE")
            self.beacon_label.setStyleSheet("color: #34d399; font-weight: 800; font-size: 11px; padding: 3px 8px; border: 1px solid #059669; border-radius: 6px; background: #052e16;")
        else:
            self.beacon_label.setText("○ CORE SCANNING")
            self.beacon_label.setStyleSheet("color: #00f0ff; font-weight: 800; font-size: 11px; padding: 3px 8px; border: 1px solid #00f0ff; border-radius: 6px; background: #08212e;")

        # 3. Dynamic Telemetry Metric Fluctuations (Feels Alive)
        cpu_load = max(5.0, min(99.0, 35.0 + random.uniform(-10.0, 10.0)))
        self.cpu_val.setText(f"{cpu_load:.1f}%")
        self.cpu_bar.setValue(int(cpu_load))
        
        bw = max(0.0, 300.0 + random.uniform(-120.0, 120.0))
        self.bw_val.setText(f"{int(bw)} KB/s")
        self.bw_bar.setValue(int(bw))
        
        threads = random.randint(8, 16)
        self.thread_val.setText(f"{threads} Active")
        self.thread_bar.setValue(threads)

        # 4. Threat Level & Modern Progress Meter
        risk = app_state.global_risk
        score = app_state.risk_score
        self.radar_score_label.setText(f"Threat Score: {score} / 100")
        self.threat_bar.setValue(min(100, max(0, score)))

        if risk.upper() == "LOW":
            self.radar_risk_readout.setText("LOW HAZARD LEVEL")
            self.radar_risk_readout.setStyleSheet("font-size: 16px; font-weight: 800; color: #34d399;")
            self.radar_segments.setText("Risk Exposure: Baseline (0/100)")
            self.threat_bar.setStyleSheet("""
                QProgressBar { border: 1px solid #162744; border-radius: 4px; background-color: #070d18; min-height: 10px; max-height: 10px; }
                QProgressBar::chunk { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #10b981, stop:1 #34d399); border-radius: 3px; }
            """)
        elif risk.upper() == "MEDIUM":
            self.radar_risk_readout.setText("MEDIUM WARNING THREAT")
            self.radar_risk_readout.setStyleSheet("font-size: 16px; font-weight: 800; color: #f59e0b;")
            self.radar_segments.setText("Risk Exposure: Elevated (40-70/100)")
            self.threat_bar.setStyleSheet("""
                QProgressBar { border: 1px solid #162744; border-radius: 4px; background-color: #070d18; min-height: 10px; max-height: 10px; }
                QProgressBar::chunk { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #d97706, stop:1 #fbbf24); border-radius: 3px; }
            """)
        else:
            self.radar_risk_readout.setText("CRITICAL PENETRATION LEVEL")
            self.radar_risk_readout.setStyleSheet("font-size: 16px; font-weight: 800; color: #f43f5e;")
            self.radar_segments.setText("Risk Exposure: Critical (>75/100)")
            self.threat_bar.setStyleSheet("""
                QProgressBar { border: 1px solid #162744; border-radius: 4px; background-color: #070d18; min-height: 10px; max-height: 10px; }
                QProgressBar::chunk { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #e11d48, stop:1 #f43f5e); border-radius: 3px; }
            """)

        # 5. Live Ports status check
        open_ports = app_state.open_ports
        for port, (cell_btn, service) in self.port_cells.items():
            if port in open_ports:
                cell_btn.setText(f"{service} : {port}\n[OPEN ●]")
                cell_btn.setProperty("class", "portChipOpen")
                cell_btn.style().unpolish(cell_btn)
                cell_btn.style().polish(cell_btn)
            else:
                cell_btn.setText(f"{service} : {port}\n[CLOSED]")
                cell_btn.setProperty("class", "portChipClosed")
                cell_btn.style().unpolish(cell_btn)
                cell_btn.style().polish(cell_btn)

        # 6. Real-Time State Fingerprint Tracking
        current_fingerprint = (
            tuple(app_state.open_ports),
            tuple(app_state.events),
            app_state.last_tool_executed,
            app_state.risk_score,
            app_state.global_risk,
            app_state.next_tool
        )
        if getattr(self, "_last_state_fingerprint", None) != current_fingerprint:
            self._last_state_fingerprint = current_fingerprint

        # 7. Attack Surface & Intel Card Updates
        target_present = bool(
            (self.target_input.text() and self.target_input.text().strip()) or
            app_state.open_ports or
            app_state.events or
            app_state.last_tool_executed
        )
        if target_present:
            from core.ml.ml_advisor import MLAdvisor
            guidance = MLAdvisor.get_guidance()
            sug_text = guidance.get("rationale", "")
            self.suggestion_label.setText(sug_text[:140] if sug_text else "Target surface registered. Launch scan directive.")
            if app_state.next_tool:
                self.next_tool_label.setText(f"DIRECTIVE: {app_state.next_tool.upper()}")
                self.run_suggested_btn.setEnabled(True)
                self.run_suggested_btn.setText(f"⚡ Execute {app_state.next_tool.upper()} (Auto-Fill)")
            else:
                self.next_tool_label.setText("DIRECTIVE: STANDBY")
                self.run_suggested_btn.setEnabled(False)
                self.run_suggested_btn.setText("⚡ Execute Directive (Enter Target to Begin)")
        else:
            self.suggestion_label.setText("[SYS_INTEL] Standing by. Enter a target IP address or domain above to receive AI scenario directives.")
            self.next_tool_label.setText("DIRECTIVE: STANDBY (Enter Target)")
            self.run_suggested_btn.setEnabled(False)
            self.run_suggested_btn.setText("⚡ Execute Directive (Enter Target to Begin)")

    # ========================
    # Interactive AI Copilot Querying
    # ========================

    def run_ai_analysis(self):
        user_prompt = self.ai_prompt_input.text().strip()
        context_parts = [
            f"Global Threat Level: {app_state.global_risk} (Score: {app_state.risk_score}/100)",
            f"Active Discovered Open Ports: {app_state.open_ports}",
            f"Vulnerability Events Detected: {app_state.events}",
            f"Active Recommendation: {app_state.suggestion}"
        ]
        context_info = "\n".join(context_parts)

        self.ai_status_dot.setText("● THINKING...")
        self.ai_status_dot.setStyleSheet("color: #fbbf24; font-size: 10px; font-weight: 800;")
        self.ask_ai_btn.setEnabled(False)
        self.copilot_output.setText("🧠 AI Copilot is analyzing scan metrics and crafting analysis response...")

        self.ai_worker = AIWorkerThread(context_info=context_info, user_prompt=user_prompt)
        self.ai_worker.finished_signal.connect(self._on_ai_analysis_finished)
        self.ai_worker.error_signal.connect(self._on_ai_analysis_error)
        self.ai_worker.start()

    def _on_ai_analysis_finished(self, response: str):
        self.ask_ai_btn.setEnabled(True)
        self.ai_prompt_input.clear()
        self.ai_status_dot.setText("● READY")
        self.ai_status_dot.setStyleSheet("color: #34d399; font-size: 10px; font-weight: 800;")
        self.copilot_output.setText(response)

    def _on_ai_analysis_error(self, err_msg: str):
        self.ask_ai_btn.setEnabled(True)
        self.ai_status_dot.setText("● ERROR")
        self.ai_status_dot.setStyleSheet("color: #f43f5e; font-size: 10px; font-weight: 800;")
        self.copilot_output.setText(f"❌ AI Analysis Error:\n{err_msg}")

    # ========================
    # Trigger suggested tool routing
    # ========================

    def run_suggested_tool(self):
        target = self.target_input.text().strip() or "127.0.0.1"
        if app_state.next_tool:
            meta = getattr(app_state, "next_action_metadata", {}) or {}
            flags = meta.get("flags", "")
            tool_name = meta.get("tool_key", app_state.next_tool)
            self.run_suggested_signal.emit(f"{tool_name}|{target}|{flags}")

    def _handle_execute_next_step(self, page_name: str, sub_tool_key: str, suggested_target: str, suggested_flags: str):
        """Handler for one-click ML next step button with auto-fill parameters."""
        active_target = self.target_input.text().strip() or suggested_target or "127.0.0.1"
        tool_name = sub_tool_key or app_state.next_tool
        self.run_suggested_signal.emit(f"{tool_name}|{active_target}|{suggested_flags}")