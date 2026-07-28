import sys
import os
import random
from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QFrame
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont
from core.app_state import app_state
from ui.topology_widget import NetworkTopologyWidget
from core.ai_copilot import AICopilot


class DashboardPage(QWidget):

    # Signal to notify MainWindow which tool to run
    run_suggested_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setObjectName("dashboardPageContainer")
        self.uptime_seconds = 0

        # Custom Premium Cyber StyleSheets
        self.setStyleSheet("""
            QWidget#dashboardPageContainer {
                background-color: #0b1220;
            }
            
            QFrame.hudCard {
                background-color: #0e1728;
                border: 1px solid #1c2a47;
                border-radius: 12px;
            }
            
            QFrame.hudCard:hover {
                border-color: #3b82f6;
            }
            
            QLabel#hudCardTitle {
                color: #8ea2c5;
                font-family: 'Segoe UI', sans-serif;
                font-size: 10px;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 1px;
                padding-bottom: 4px;
                border-bottom: 1px solid #1e2e4f;
            }
            
            QLabel#telemetryValue {
                font-family: 'Courier New', 'Consolas', monospace;
                font-size: 24px;
                font-weight: bold;
                color: #00f0ff;
            }
            
            QLabel#telemetryUnit {
                font-family: 'Segoe UI', sans-serif;
                font-size: 11px;
                color: #5d7290;
            }
            
            QLabel#portCellOpen {
                background-color: #092c20;
                color: #2ecc71;
                border: 1px solid #2ecc71;
                border-radius: 8px;
                font-weight: bold;
                font-family: 'Courier New', 'Consolas', monospace;
                font-size: 10px;
                padding: 8px;
                alignment: center;
            }
            
            QLabel#portCellClosed {
                background-color: #0f1624;
                color: #4a5c7a;
                border: 1px solid #1b263b;
                border-radius: 8px;
                font-weight: bold;
                font-family: 'Courier New', 'Consolas', monospace;
                font-size: 10px;
                padding: 8px;
                alignment: center;
            }
            
            QPushButton#actionBtn {
                background-color: #2f5eb8;
                color: #f2f7ff;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 8px;
                border: 1px solid #3567c7;
            }
            QPushButton#actionBtn:hover {
                background-color: #3a6cca;
            }
            QPushButton#actionBtn:disabled {
                background-color: #151e2e;
                border: 1px solid #202b3d;
                color: #4c5d78;
            }
        """)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(16)

        # =====================================================================
        # 1. CYBERNETIC STATUS DECK (HEADER)
        # =====================================================================
        header_frame = QFrame()
        header_frame.setObjectName("hudHeader")
        header_frame.setStyleSheet("""
            QFrame#hudHeader {
                background-color: #0e1728;
                border: 1px solid #1c2a47;
                border-radius: 12px;
                padding: 12px;
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(16, 12, 16, 12)

        title_layout = QVBoxLayout()
        self.hud_title = QLabel("▲ KALINOVA OS // COMMAND DECK")
        self.hud_title.setStyleSheet("font-size: 20px; font-weight: 800; color: #00f0ff; letter-spacing: 1px;")
        
        self.hud_subtitle = QLabel("DYNAMIC SCANNER & RISK INTELLIGENCE SCAN DECK")
        self.hud_subtitle.setStyleSheet("font-size: 10px; font-weight: 600; color: #64748b; letter-spacing: 0.5px;")
        
        title_layout.addWidget(self.hud_title)
        title_layout.addWidget(self.hud_subtitle)

        # Right Header Metadata Panel
        meta_layout = QHBoxLayout()
        meta_layout.setSpacing(16)
        
        # System clock
        self.system_time_label = QLabel("TIME: 00:00:00")
        self.system_time_label.setStyleSheet("font-family: 'Courier New', monospace; font-size: 11px; color: #8ea2c5;")
        
        # System uptime
        self.system_uptime_label = QLabel("UPTIME: 00:00:00")
        self.system_uptime_label.setStyleSheet("font-family: 'Courier New', monospace; font-size: 11px; color: #8ea2c5;")

        # Active telemetry indicator
        self.beacon_label = QLabel("● CORE ONLINE")
        self.beacon_label.setStyleSheet("color: #2ecc71; font-weight: bold; font-size: 11px; padding: 2px 6px; border: 1px solid #2ecc71; border-radius: 4px; background: #0c291b;")

        meta_layout.addWidget(self.system_time_label)
        meta_layout.addWidget(self.system_uptime_label)
        meta_layout.addWidget(self.beacon_label)

        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addLayout(meta_layout)

        main_layout.addWidget(header_frame)

        # =====================================================================
        # 2. BENTO GRID WIDGETS LAYOUT
        # =====================================================================
        grid_layout = QGridLayout()
        grid_layout.setSpacing(16)

        # --- PANEL A: THREAT RADAR RADIAL / DANGER BAR (Row 0, Col 0) ---
        self.threat_card = QFrame()
        self.threat_card.setProperty("class", "hudCard")
        threat_layout = QVBoxLayout(self.threat_card)
        threat_layout.setContentsMargins(16, 16, 16, 16)
        threat_layout.setSpacing(8)

        threat_title = QLabel("Threat Radar Gauge")
        threat_title.setObjectName("hudCardTitle")
        
        self.radar_risk_readout = QLabel("LOW HAZARD LEVEL")
        self.radar_risk_readout.setStyleSheet("font-size: 18px; font-weight: bold; color: #2ecc71;")

        # Segmented threat visual meter
        self.radar_segments = QLabel("[ ░░░░░░░░░░░░░░░░░░░░ ]")
        self.radar_segments.setStyleSheet("font-family: 'Courier New', monospace; font-size: 16px; color: #2ecc71;")
        
        self.radar_score_label = QLabel("Threat Rating: 0 / 100")
        self.radar_score_label.setStyleSheet("font-size: 11px; color: #64748b;")

        threat_layout.addWidget(threat_title)
        threat_layout.addWidget(self.radar_risk_readout)
        threat_layout.addWidget(self.radar_segments)
        threat_layout.addWidget(self.radar_score_label)
        threat_layout.addStretch()

        # --- PANEL B: LIVE NETWORK PORT SCAN GRID (Row 0, Col 1) ---
        self.ports_card = QFrame()
        self.ports_card.setProperty("class", "hudCard")
        ports_layout = QVBoxLayout(self.ports_card)
        ports_layout.setContentsMargins(16, 16, 16, 16)
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

        # --- PANEL C: CORE ENGINE TELEMETRY & HARDWARE GAUGES (Row 1, Col 0) ---
        self.telemetry_card = QFrame()
        self.telemetry_card.setProperty("class", "hudCard")
        telemetry_layout = QVBoxLayout(self.telemetry_card)
        telemetry_layout.setContentsMargins(16, 16, 16, 16)
        telemetry_layout.setSpacing(8)

        telemetry_title = QLabel("Core Hardware Telemetry")
        telemetry_title.setObjectName("hudCardTitle")
        telemetry_layout.addWidget(telemetry_title)

        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(12)

        # Metric 1: Core load
        cpu_box = QVBoxLayout()
        self.cpu_val = QLabel("42.8%")
        self.cpu_val.setObjectName("telemetryValue")
        cpu_lbl = QLabel("Hacking Core Load")
        cpu_lbl.setObjectName("telemetryUnit")
        cpu_box.addWidget(self.cpu_val)
        cpu_box.addWidget(cpu_lbl)

        # Metric 2: Network Bandwidth
        bw_box = QVBoxLayout()
        self.bw_val = QLabel("482.4 KB/s")
        self.bw_val.setObjectName("telemetryValue")
        self.bw_val.setStyleSheet("color: #a855f7;")
        bw_lbl = QLabel("Scraping Bandwidth")
        bw_lbl.setObjectName("telemetryUnit")
        bw_box.addWidget(self.bw_val)
        bw_box.addWidget(bw_lbl)

        # Metric 3: Active threads
        thread_box = QVBoxLayout()
        self.thread_val = QLabel("12 Core")
        self.thread_val.setObjectName("telemetryValue")
        self.thread_val.setStyleSheet("color: #3b82f6;")
        thread_lbl = QLabel("Active Run Threads")
        thread_lbl.setObjectName("telemetryUnit")
        thread_box.addWidget(self.thread_val)
        thread_box.addWidget(thread_lbl)

        metrics_layout.addLayout(cpu_box)
        metrics_layout.addLayout(bw_box)
        metrics_layout.addLayout(thread_box)

        telemetry_layout.addLayout(metrics_layout)
        telemetry_layout.addStretch()

        # --- PANEL D: TACTICAL ACTION DECK & INTEL (Row 1, Col 1) ---
        self.action_card = QFrame()
        self.action_card.setProperty("class", "hudCard")
        action_layout = QVBoxLayout(self.action_card)
        action_layout.setContentsMargins(16, 16, 16, 16)
        action_layout.setSpacing(8)

        action_title = QLabel("Hacking Suggestion Deck")
        action_title.setObjectName("hudCardTitle")
        
        self.suggestion_label = QLabel("Suggestions: Scanning segments...")
        self.suggestion_label.setWordWrap(True)
        self.suggestion_label.setStyleSheet("font-family: 'Courier New', monospace; font-size: 11px; color: #d6e2ff;")

        self.next_tool_label = QLabel("Recommended Tool: None")
        self.next_tool_label.setStyleSheet("font-size: 11px; font-weight: bold; color: #f59e0b;")

        self.run_suggested_btn = QPushButton("Initialize Tool Deck")
        self.run_suggested_btn.setObjectName("actionBtn")
        self.run_suggested_btn.setEnabled(False)
        self.run_suggested_btn.clicked.connect(self.run_suggested_tool)

        action_layout.addWidget(action_title)
        action_layout.addWidget(self.suggestion_label)
        action_layout.addWidget(self.next_tool_label)
        action_layout.addWidget(self.run_suggested_btn)
        action_layout.addStretch()

        # --- PANEL E: INTERACTIVE RADAR TOPOLOGY (Row 0, Col 2) ---
        self.topology_card = QFrame()
        self.topology_card.setProperty("class", "hudCard")
        topo_layout = QVBoxLayout(self.topology_card)
        topo_layout.setContentsMargins(16, 16, 16, 16)
        topo_layout.setSpacing(6)

        topo_title = QLabel("Network Topology Sweep")
        topo_title.setObjectName("hudCardTitle")

        self.topology_widget = NetworkTopologyWidget()

        topo_layout.addWidget(topo_title)
        topo_layout.addWidget(self.topology_widget, 1)

        # --- PANEL F: SECURITY COPILOT INFRASTRUCTURE (Row 1, Col 2) ---
        self.copilot_card = QFrame()
        self.copilot_card.setProperty("class", "hudCard")
        copilot_layout = QVBoxLayout(self.copilot_card)
        copilot_layout.setContentsMargins(16, 16, 16, 16)
        copilot_layout.setSpacing(8)

        copilot_title = QLabel("Heuristic Copilot Advisory")
        copilot_title.setObjectName("hudCardTitle")

        self.copilot_advice = QLabel("Initializing security scan diagnostics...")
        self.copilot_advice.setWordWrap(True)
        self.copilot_advice.setStyleSheet("font-family: 'Courier New', monospace; font-size: 10px; color: #10b981;")

        copilot_layout.addWidget(copilot_title)
        copilot_layout.addWidget(self.copilot_advice)
        copilot_layout.addStretch()

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

        # Dynamic update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_dashboard)
        self.timer.start(1000)

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
            self.beacon_label.setStyleSheet("color: #2ecc71; font-weight: bold; font-size: 11px; padding: 2px 6px; border: 1px solid #2ecc71; border-radius: 4px; background: #0c291b;")
        else:
            self.beacon_label.setText("○ CORE SCANNING")
            self.beacon_label.setStyleSheet("color: #00f0ff; font-weight: bold; font-size: 11px; padding: 2px 6px; border: 1px solid #00f0ff; border-radius: 4px; background: #08212e;")

        # 3. Dynamic Telemetry Metric Fluctuations (Feels Alive)
        cpu_load = max(5.0, min(99.0, 35.0 + random.uniform(-10.0, 10.0)))
        self.cpu_val.setText(f"{cpu_load:.1f}%")
        
        bw = max(0.0, 300.0 + random.uniform(-120.0, 120.0))
        self.bw_val.setText(f"{bw:.1f} KB/s")
        
        threads = random.randint(8, 16)
        self.thread_val.setText(f"{threads} Active")

        # 4. Threat Level segments & rating color adjustments
        risk = app_state.global_risk
        score = app_state.risk_score
        self.radar_score_label.setText(f"Threat Rating: {score} / 100")

        # Visual segment representation
        filled_segments = int(score / 5)
        bar = "█" * filled_segments + "░" * (20 - filled_segments)
        self.radar_segments.setText(f"[ {bar} ]")

        if risk.upper() == "LOW":
            self.radar_risk_readout.setText("LOW HAZARD LEVEL")
            self.radar_risk_readout.setStyleSheet("font-size: 18px; font-weight: bold; color: #10b981;")
            self.radar_segments.setStyleSheet("font-family: 'Courier New', monospace; font-size: 16px; color: #10b981;")
        elif risk.upper() == "MEDIUM":
            self.radar_risk_readout.setText("MEDIUM WARNING THREAT")
            self.radar_risk_readout.setStyleSheet("font-size: 18px; font-weight: bold; color: #f59e0b;")
            self.radar_segments.setStyleSheet("font-family: 'Courier New', monospace; font-size: 16px; color: #f59e0b;")
        else:
            self.radar_risk_readout.setText("CRITICAL PENETRATION LEVEL")
            self.radar_risk_readout.setStyleSheet("font-size: 18px; font-weight: bold; color: #f43f5e;")
            self.radar_segments.setStyleSheet("font-family: 'Courier New', monospace; font-size: 16px; color: #f43f5e;")

        # 5. Live Ports status check
        open_ports = app_state.open_ports
        for port, (cell, service) in self.port_cells.items():
            if port in open_ports:
                cell.setText(f"{service} : {port}\n[OPEN ●]")
                cell.setObjectName("portCellOpen")
                # Force CSS polish update
                cell.style().unpolish(cell)
                cell.style().polish(cell)
            else:
                cell.setText(f"{service} : {port}\n[CLOSED]")
                cell.setObjectName("portCellClosed")
                cell.style().unpolish(cell)
                cell.style().polish(cell)

        # 6. Suggestions
        sug_text = app_state.suggestion
        if not sug_text or sug_text == "None":
            self.suggestion_label.setText("[SYS_DECK] > Standing by. No anomalies detected on scanned local segments. Recommended action: Nmap recon.")
        else:
            self.suggestion_label.setText(f"[SYS_INTEL] > Threat signatures detected:\n{sug_text}")

        # 7. Next Tool quick-action
        if app_state.next_tool:
            self.next_tool_label.setText(f"RECOMMENDED DIRECTIVE: {app_state.next_tool.upper()}")
            self.run_suggested_btn.setEnabled(True)
        else:
            self.next_tool_label.setText("RECOMMENDED DIRECTIVE: STANDBY")
            self.run_suggested_btn.setEnabled(False)

        # 8. Query Heuristic Diagnostics Copilot
        findings = AICopilot.diagnose(app_state.events, app_state.open_ports)
        advice_parts = []
        for f in findings[:2]: # Show up to 2 key findings in dashboard to save space
            advice_parts.append(f"● {f['title']} [{f['severity']}]\n  {f['description']}")
        
        self.copilot_advice.setText("\n\n".join(advice_parts))

    # ========================
    # Trigger suggested tool routing
    # ========================

    def run_suggested_tool(self):
        if app_state.next_tool:
            self.run_suggested_signal.emit(app_state.next_tool)