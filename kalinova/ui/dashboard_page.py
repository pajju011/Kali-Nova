import sys
import os
import random
from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QFrame, QTextEdit, QLineEdit, QProgressBar
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont
from core.app_state import app_state
from ui.topology_widget import NetworkTopologyWidget
from core.ai_copilot import AICopilot, AIWorkerThread
from ui.components.next_step_card import NextStepCard


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
            
            QLabel#portCellOpen {
                background-color: #062e1e;
                color: #34d399;
                border: 1px solid #059669;
                border-radius: 8px;
                font-weight: 800;
                font-family: 'Courier New', 'Consolas', monospace;
                font-size: 10px;
                padding: 8px 4px;
            }
            
            QLabel#portCellClosed {
                background-color: #0a1120;
                color: #475569;
                border: 1px solid #162238;
                border-radius: 8px;
                font-weight: 700;
                font-family: 'Courier New', 'Consolas', monospace;
                font-size: 10px;
                padding: 8px 4px;
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
        self.hud_title = QLabel("▲ KALINOVA OS // SECURITY OPERATIONS DECK")
        self.hud_title.setStyleSheet("font-size: 18px; font-weight: 800; color: #00f0ff; letter-spacing: 1px;")
        
        self.hud_subtitle = QLabel("REAL-TIME ATTACK SURFACE DISCOVERY & ML SCENARIO INTELLIGENCE")
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
        # 2. HERO ML SCENARIO INTELLIGENCE DIRECTIVE BANNER
        # =====================================================================
        self.next_step_card = NextStepCard()
        self.next_step_card.execute_step_signal.connect(self._handle_execute_next_step)
        main_layout.addWidget(self.next_step_card)

        # =====================================================================
        # 3. BENTO GRID WIDGETS LAYOUT (2x3 Grid)
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

        threat_layout.addWidget(threat_title)
        threat_layout.addWidget(self.radar_risk_readout)
        threat_layout.addWidget(self.threat_bar)
        threat_layout.addWidget(self.radar_score_label)
        threat_layout.addWidget(self.radar_segments)
        threat_layout.addStretch()

        # --- PANEL B: LIVE NETWORK PORT SCAN MATRIX (Row 0, Col 1) ---
        self.ports_card = QFrame()
        self.ports_card.setProperty("class", "hudCard")
        ports_layout = QVBoxLayout(self.ports_card)
        ports_layout.setContentsMargins(16, 14, 16, 14)
        ports_layout.setSpacing(8)

        ports_title = QLabel("Live Network Port Matrix")
        ports_title.setObjectName("hudCardTitle")
        ports_layout.addWidget(ports_title)

        # 2x4 Grid layout for ports
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
            cell = QLabel(f"{service} : {port}\n[CLOSED]")
            cell.setObjectName("portCellClosed")
            cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ports_grid.addWidget(cell, row, col)
            self.port_cells[port] = (cell, service)

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

        # --- PANEL E: TARGET & ATTACK SURFACE INTEL (Row 1, Col 1) ---
        self.action_card = QFrame()
        self.action_card.setProperty("class", "hudCard")
        action_layout = QVBoxLayout(self.action_card)
        action_layout.setContentsMargins(16, 14, 16, 14)
        action_layout.setSpacing(8)

        action_title = QLabel("Attack Surface & Target Intel")
        action_title.setObjectName("hudCardTitle")
        
        self.target_intel_label = QLabel("Active Target: 127.0.0.1 (Localhost)")
        self.target_intel_label.setStyleSheet("font-size: 13px; font-weight: 800; color: #ffffff;")

        self.suggestion_label = QLabel("[SYS_INTEL] Standing by for target recon. Discovered ports and services will map here.")
        self.suggestion_label.setWordWrap(True)
        self.suggestion_label.setStyleSheet("font-size: 11px; color: #94a3b8; line-height: 1.3;")

        self.next_tool_label = QLabel("DIRECTIVE: INITIAL OSINT RECON")
        self.next_tool_label.setStyleSheet("font-size: 11px; font-weight: 800; color: #00f0ff;")

        self.run_suggested_btn = QPushButton("⚡ Execute Directive (Auto-Fill)")
        self.run_suggested_btn.setObjectName("actionBtn")
        self.run_suggested_btn.clicked.connect(self.run_suggested_tool)

        action_layout.addWidget(action_title)
        action_layout.addWidget(self.target_intel_label)
        action_layout.addWidget(self.suggestion_label)
        action_layout.addWidget(self.next_tool_label)
        action_layout.addWidget(self.run_suggested_btn)
        action_layout.addStretch()

        # --- PANEL F: AI COPILOT INFRASTRUCTURE (Row 1, Col 2) ---
        self.copilot_card = QFrame()
        self.copilot_card.setProperty("class", "hudCard")
        copilot_layout = QVBoxLayout(self.copilot_card)
        copilot_layout.setContentsMargins(16, 14, 16, 14)
        copilot_layout.setSpacing(8)

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
                padding: 8px;
            }
        """)
        self.copilot_output.setText("Initializing security scan diagnostics...\nStanding by for AI copilot queries.")

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
        for port, (cell, service) in self.port_cells.items():
            if port in open_ports:
                cell.setText(f"{service} : {port}\n[OPEN ●]")
                cell.setObjectName("portCellOpen")
                cell.style().unpolish(cell)
                cell.style().polish(cell)
            else:
                cell.setText(f"{service} : {port}\n[CLOSED]")
                cell.setObjectName("portCellClosed")
                cell.style().unpolish(cell)
                cell.style().polish(cell)

        # 6. Real-Time State Fingerprint Tracking & ML Guidance Refresh
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
            if hasattr(self, "next_step_card"):
                self.next_step_card.refresh_guidance()

        # 7. Attack Surface & Intel Card Updates
        target_name = getattr(app_state, "next_target", "") or "127.0.0.1"
        if not target_name and app_state.pipeline_artifacts.get("targets"):
            target_name = app_state.pipeline_artifacts["targets"][0]
        self.target_intel_label.setText(f"Active Target: {target_name}")

        sug_text = app_state.suggestion
        if not sug_text or sug_text == "None" or "No suggestions yet" in sug_text:
            self.suggestion_label.setText("No critical anomalies detected. System ready for targeted port or OSINT discovery.")
        else:
            first_line = sug_text.splitlines()[0] if sug_text else "Signatures detected."
            self.suggestion_label.setText(first_line[:120])

        if app_state.next_tool:
            self.next_tool_label.setText(f"DIRECTIVE: {app_state.next_tool.upper()}")
            self.run_suggested_btn.setEnabled(True)
            self.run_suggested_btn.setText(f"⚡ Execute {app_state.next_tool.upper()} (Auto-Fill)")
        else:
            self.next_tool_label.setText("DIRECTIVE: STANDBY")
            self.run_suggested_btn.setEnabled(False)
            self.run_suggested_btn.setText("⚡ Execute Directive (Auto-Fill)")

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
        if app_state.next_tool:
            meta = getattr(app_state, "next_action_metadata", {}) or {}
            target = meta.get("target", "") or ""
            flags = meta.get("flags", "")
            tool_name = meta.get("tool_key", app_state.next_tool)
            self.run_suggested_signal.emit(f"{tool_name}|{target}|{flags}")

    def _handle_execute_next_step(self, page_name: str, sub_tool_key: str, suggested_target: str, suggested_flags: str):
        """Handler for one-click ML next step button with auto-fill parameters."""
        tool_name = sub_tool_key or app_state.next_tool
        self.run_suggested_signal.emit(f"{tool_name}|{suggested_target}|{suggested_flags}")