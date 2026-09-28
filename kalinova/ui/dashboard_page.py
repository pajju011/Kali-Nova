import sys
import os
import random
from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QFrame, QTextEdit, QLineEdit, QProgressBar, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QSize, QRectF
from PyQt6.QtGui import QFont, QCursor, QPainter, QPixmap, QIcon, QRadialGradient, QColor
from PyQt6.QtSvg import QSvgRenderer
from core.app_state import app_state
from ui.topology_widget import NetworkTopologyWidget
from core.ai_copilot import AICopilot, AIWorkerThread
from ui.icon_manager import get_tool_icon_path


class HeroFrame(QFrame):
    """Hero banner with authentic glowing Kali Linux Dragon matching screenshot."""

    def __init__(self):
        super().__init__()
        self.setObjectName("hudHero")
        logo_path = get_tool_icon_path("kalinova")
        self._renderer = QSvgRenderer(logo_path) if logo_path and os.path.exists(logo_path) else None

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self._renderer and self._renderer.isValid():
            dw = min(320.0, float(self.width()) * 0.38)
            dh = dw * 0.65
            dx = float(self.width()) * 0.44
            dy = float(self.height() - dh) / 2.0

            # Subtle radial cyan glow behind dragon
            cx = dx + dw * 0.5
            cy = dy + dh * 0.5
            glow = QRadialGradient(cx, cy, dw * 0.65)
            glow.setColorAt(0.0, QColor(0, 240, 255, 45))
            glow.setColorAt(0.5, QColor(37, 99, 235, 18))
            glow.setColorAt(1.0, QColor(8, 19, 36, 0))
            painter.fillRect(QRectF(dx - 30, dy - 20, dw + 60, dh + 40), glow)

            painter.setOpacity(0.95)
            self._renderer.render(painter, QRectF(dx, dy, dw, dh))

        painter.end()


class DashboardPage(QWidget):

    # Signal to notify MainWindow which tool to run (composite format: tool|target|flags)
    run_suggested_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setObjectName("dashboardPageContainer")
        self.uptime_seconds = 880  # 00:14:40 baseline matching image
        self.ai_worker = None
        self._last_state_fingerprint = None

        # Custom Cyber StyleSheets matching the exact UI design
        self.setStyleSheet("""
            QWidget#dashboardPageContainer {
                background-color: #060b13;
            }
            
            QFrame.hudCard {
                background-color: #081220;
                border: 1px solid #14243e;
                border-radius: 8px;
            }
            
            QFrame.hudCard:hover {
                border-color: #1d4ed8;
            }
            
            QLabel#hudCardTitle {
                color: #cbd5e1;
                font-family: 'Segoe UI', 'Inter', sans-serif;
                font-size: 11px;
                font-weight: 800;
                letter-spacing: 0.8px;
            }
            
            QLabel#telemetryValue {
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 20px;
                font-weight: 800;
                color: #00f0ff;
            }
            
            QLabel#telemetryUnit {
                font-family: 'Segoe UI', sans-serif;
                font-size: 8.5px;
                font-weight: 700;
                color: #64748b;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            QPushButton.portChipOpen {
                background-color: #08101e;
                color: #34d399;
                border: 1px solid #059669;
                border-radius: 6px;
                font-weight: 700;
                font-family: 'Segoe UI', sans-serif;
                font-size: 9.5px;
                padding: 6px 2px;
                text-align: center;
            }
            QPushButton.portChipOpen:hover {
                background-color: #062e1e;
                border-color: #10b981;
            }
            
            QPushButton.portChipClosed {
                background-color: #08101e;
                color: #cbd5e1;
                border: 1px solid #14243e;
                border-radius: 6px;
                font-weight: 700;
                font-family: 'Segoe UI', sans-serif;
                font-size: 9.5px;
                padding: 6px 2px;
                text-align: center;
            }
            QPushButton.portChipClosed:hover {
                background-color: #0c182b;
                border-color: #2563eb;
            }
            
            QPushButton.quickChip {
                background-color: #091629;
                color: #93c5fd;
                border: 1px solid #172d4c;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 9.5px;
                font-weight: 700;
            }
            QPushButton.quickChip:hover {
                background-color: #162a48;
                color: #ffffff;
                border-color: #38bdf8;
            }
            
            QProgressBar.hudProgress {
                border: 1px solid #142238;
                border-radius: 3px;
                background-color: #070d18;
                text-align: center;
                min-height: 5px;
                max-height: 5px;
            }
        """)

        # Main Layout: 3 Rows Bento Grid
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 12, 16, 14)
        main_layout.setSpacing(12)

        # =====================================================================
        # ROW 1: HERO BANNER (Left ~70%) + SYSTEM STATUS (Right ~30%)
        # =====================================================================
        row1_layout = QHBoxLayout()
        row1_layout.setSpacing(12)

        # 1A. Hero Banner
        self.hero_card = HeroFrame()
        self.hero_card.setStyleSheet("""
            QFrame#hudHero {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #081324, stop:0.5 #0c1c34, stop:1 #081120);
                border: 1px solid #14243e;
                border-radius: 8px;
            }
        """)
        self.hero_card.setFixedHeight(132)
        hero_layout = QHBoxLayout(self.hero_card)
        hero_layout.setContentsMargins(20, 14, 20, 14)

        # Left title column
        hero_text_col = QVBoxLayout()
        hero_text_col.setSpacing(2)
        hero_text_col.setContentsMargins(0, 0, 0, 0)

        self.hud_title = QLabel("KALINOVA")
        self.hud_title.setStyleSheet("""
            font-size: 28px;
            font-weight: 900;
            color: #ffffff;
            letter-spacing: 2px;
            background: transparent;
            border: none;
            font-family: 'Segoe UI', 'Inter', sans-serif;
        """)

        self.hud_op = QLabel("ADVANCED SECURITY OPERATIONS")
        self.hud_op.setStyleSheet("""
            font-size: 10.5px;
            font-weight: 800;
            color: #00f0ff;
            letter-spacing: 1.5px;
            background: transparent;
            border: none;
            font-family: 'Segoe UI', sans-serif;
        """)

        self.hud_subtitle = QLabel("REAL-TIME ATTACK SURFACE DISCOVERY & PENETRATION TESTING")
        self.hud_subtitle.setStyleSheet("""
            font-size: 8.5px;
            font-weight: 600;
            color: #94a3b8;
            letter-spacing: 0.5px;
            background: transparent;
            border: none;
            font-family: 'Segoe UI', sans-serif;
        """)

        hero_text_col.addWidget(self.hud_title)
        hero_text_col.addWidget(self.hud_op)
        hero_text_col.addWidget(self.hud_subtitle)
        hero_layout.addLayout(hero_text_col)

        hero_layout.addStretch()

        # Right Quote
        quote_col = QVBoxLayout()
        quote_col.setSpacing(2)
        quote_col.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        quote_line = QLabel('"The quieter you become,\nthe more you are able to hear."')
        quote_line.setStyleSheet("color: #94a3b8; font-size: 9.5px; font-style: italic; line-height: 1.3; background: transparent; border: none;")
        quote_line.setAlignment(Qt.AlignmentFlag.AlignRight)

        quote_author = QLabel("— KALI LINUX")
        quote_author.setStyleSheet("color: #00f0ff; font-size: 9px; font-weight: 800; letter-spacing: 1px; background: transparent; border: none;")
        quote_author.setAlignment(Qt.AlignmentFlag.AlignRight)

        quote_col.addWidget(quote_line)
        quote_col.addWidget(quote_author)
        hero_layout.addLayout(quote_col)

        row1_layout.addWidget(self.hero_card, 64)

        # 1B. System Status Card
        self.sys_status_card = QFrame()
        self.sys_status_card.setProperty("class", "hudCard")
        self.sys_status_card.setFixedHeight(132)
        sys_status_layout = QVBoxLayout(self.sys_status_card)
        sys_status_layout.setContentsMargins(16, 14, 16, 14)
        sys_status_layout.setSpacing(12)

        # Header row
        sys_header = QHBoxLayout()
        sys_title = QLabel("SYSTEM STATUS")
        sys_title.setObjectName("hudCardTitle")

        self.beacon_label = QLabel("● CORE ONLINE")
        self.beacon_label.setStyleSheet("color: #10b981; font-weight: 800; font-size: 10px; letter-spacing: 0.5px;")

        sys_header.addWidget(sys_title)
        sys_header.addStretch()
        sys_header.addWidget(self.beacon_label)
        sys_status_layout.addLayout(sys_header)

        # 4 Columns of System Info
        sys_metrics = QHBoxLayout()
        sys_metrics.setSpacing(10)

        # Time
        c1 = QVBoxLayout()
        c1.setSpacing(3)
        self.system_time_val = QLabel("14:48:54")
        self.system_time_val.setStyleSheet("color: #f8fafc; font-family: 'Consolas', monospace; font-size: 13.5px; font-weight: 800; border: none;")
        c1_lbl = QLabel("SYSTEM TIME")
        c1_lbl.setWordWrap(False)
        c1_lbl.setStyleSheet("color: #64748b; font-size: 8px; font-weight: 700; letter-spacing: 0.5px; border: none;")
        c1.addWidget(self.system_time_val)
        c1.addWidget(c1_lbl)

        # Uptime
        c2 = QVBoxLayout()
        c2.setSpacing(3)
        self.system_uptime_val = QLabel("00:14:40")
        self.system_uptime_val.setStyleSheet("color: #f8fafc; font-family: 'Consolas', monospace; font-size: 13.5px; font-weight: 800; border: none;")
        c2_lbl = QLabel("UPTIME")
        c2_lbl.setWordWrap(False)
        c2_lbl.setStyleSheet("color: #64748b; font-size: 8px; font-weight: 700; letter-spacing: 0.5px; border: none;")
        c2.addWidget(self.system_uptime_val)
        c2.addWidget(c2_lbl)

        # Kernel
        c3 = QVBoxLayout()
        c3.setSpacing(3)
        c3_val = QLabel("6.6.0-kali")
        c3_val.setStyleSheet("color: #f8fafc; font-family: 'Consolas', monospace; font-size: 13.5px; font-weight: 800; border: none;")
        c3_lbl = QLabel("KERNEL")
        c3_lbl.setWordWrap(False)
        c3_lbl.setStyleSheet("color: #64748b; font-size: 8px; font-weight: 700; letter-spacing: 0.5px; border: none;")
        c3.addWidget(c3_val)
        c3.addWidget(c3_lbl)

        # Memory
        c4 = QVBoxLayout()
        c4.setSpacing(3)
        c4_val = QLabel("8 / 16 GB")
        c4_val.setStyleSheet("color: #f8fafc; font-family: 'Consolas', monospace; font-size: 13.5px; font-weight: 800; border: none;")
        c4_lbl = QLabel("MEMORY")
        c4_lbl.setWordWrap(False)
        c4_lbl.setStyleSheet("color: #64748b; font-size: 8px; font-weight: 700; letter-spacing: 0.5px; border: none;")
        c4.addWidget(c4_val)
        c4.addWidget(c4_lbl)

        sys_metrics.addLayout(c1)
        sys_metrics.addLayout(c2)
        sys_metrics.addLayout(c3)
        sys_metrics.addLayout(c4)

        sys_status_layout.addLayout(sys_metrics)
        sys_status_layout.addStretch()

        row1_layout.addWidget(self.sys_status_card, 36)

        main_layout.addLayout(row1_layout, 0)

        # =====================================================================
        # ROW 2: THREAT RADAR (28%) + PORT MATRIX (44%) + TOPOLOGY SWEEP (28%)
        # =====================================================================
        row2_layout = QHBoxLayout()
        row2_layout.setSpacing(12)

        # 2A. Threat Radar Gauge
        self.threat_card = QFrame()
        self.threat_card.setProperty("class", "hudCard")
        threat_layout = QVBoxLayout(self.threat_card)
        threat_layout.setContentsMargins(16, 12, 16, 12)
        threat_layout.setSpacing(8)

        threat_title = QLabel("🛡️  THREAT RADAR GAUGE")
        threat_title.setObjectName("hudCardTitle")
        
        self.radar_risk_readout = QLabel("LOW HAZARD LEVEL")
        self.radar_risk_readout.setStyleSheet("""
            background-color: #041f17;
            border: 1px solid #059669;
            color: #10b981;
            font-size: 11px;
            font-weight: 800;
            padding: 5px 12px;
            border-radius: 6px;
        """)
        self.radar_risk_readout.setFixedWidth(160)
        self.radar_risk_readout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.radar_score_label = QLabel("Threat Score: 0 / 100")
        self.radar_score_label.setStyleSheet("font-size: 12px; font-weight: 700; color: #f8fafc;")

        # Progress bar
        self.threat_bar = QProgressBar()
        self.threat_bar.setProperty("class", "hudProgress")
        self.threat_bar.setRange(0, 100)
        self.threat_bar.setValue(0)
        self.threat_bar.setTextVisible(False)
        self.threat_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #142238;
                border-radius: 4px;
                background-color: #070d18;
                min-height: 8px;
                max-height: 8px;
            }
            QProgressBar::chunk {
                background: #10b981;
                border-radius: 3px;
            }
        """)

        self.radar_segments = QLabel("Risk Exposure: Baseline (0/100)")
        self.radar_segments.setStyleSheet("font-size: 10px; color: #64748b; font-weight: 600; border: none;")

        self.quick_audit_btn = QPushButton()
        self.quick_audit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.quick_audit_btn.setStyleSheet("""
            QPushButton {
                background-color: #0a1c36;
                border: 1px solid #1d4ed8;
                border-radius: 6px;
                padding: 7px 12px;
            }
            QPushButton:hover {
                background-color: #14284d;
                border-color: #38bdf8;
            }
        """)
        btn_layout = QHBoxLayout(self.quick_audit_btn)
        btn_layout.setContentsMargins(4, 0, 4, 0)
        btn_left = QLabel("🔍  Deep Vulnerability Diagnostic")
        btn_left.setStyleSheet("color: #e2e8f0; font-size: 11px; font-weight: 700; background: transparent; border: none;")
        btn_left.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        btn_right = QLabel(">")
        btn_right.setStyleSheet("color: #38bdf8; font-size: 12px; font-weight: 800; background: transparent; border: none;")
        btn_right.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        btn_layout.addWidget(btn_left)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_right)
        self.quick_audit_btn.clicked.connect(self._run_quick_vulnerability_audit)

        threat_layout.addWidget(threat_title)
        threat_layout.addWidget(self.radar_risk_readout)
        threat_layout.addWidget(self.radar_score_label)
        threat_layout.addWidget(self.threat_bar)
        threat_layout.addWidget(self.radar_segments)
        threat_layout.addWidget(self.quick_audit_btn)
        threat_layout.addStretch()

        self.threat_card.setMinimumHeight(200)
        self.threat_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        row2_layout.addWidget(self.threat_card, 28)

        # 2B. Live Network Port Scan Matrix
        self.ports_card = QFrame()
        self.ports_card.setProperty("class", "hudCard")
        self.ports_card.setMinimumHeight(200)
        self.ports_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        ports_layout = QVBoxLayout(self.ports_card)
        ports_layout.setContentsMargins(16, 12, 16, 12)
        ports_layout.setSpacing(8)

        ports_header = QHBoxLayout()
        ports_title = QLabel("🌐  LIVE NETWORK PORT MATRIX")
        ports_title.setObjectName("hudCardTitle")
        ports_hint = QLabel("(Click port to audit)")
        ports_hint.setStyleSheet("font-size: 8.5px; color: #64748b; font-weight: 600; border: none;")
        ports_header.addWidget(ports_title)
        ports_header.addStretch()
        ports_header.addWidget(ports_hint)
        ports_layout.addLayout(ports_header)

        # 2x4 Grid layout
        self.ports_grid_widget = QWidget()
        self.ports_grid = QGridLayout(self.ports_grid_widget)
        self.ports_grid.setContentsMargins(0, 4, 0, 0)
        self.ports_grid.setSpacing(8)

        self.monitored_ports = [
            (21, "FTP"), (22, "SSH"), (80, "HTTP"), (443, "HTTPS"),
            (3306, "MySQL"), (8080, "HTTP-Alt"), (9000, "FastCGI"), (993, "IMAPS")
        ]
        self.port_cells = {}

        for idx, (port, service) in enumerate(self.monitored_ports):
            row = idx // 4
            col = idx % 4
            cell_btn = QPushButton(f"{service} : {port}\n● CLOSED")
            cell_btn.setProperty("class", "portChipClosed")
            cell_btn.setMinimumHeight(48)
            cell_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            cell_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            cell_btn.setToolTip(f"Audit service on Port {port} ({service})")
            cell_btn.clicked.connect(lambda _, p=port, s=service: self._on_port_clicked(p, s))
            self.ports_grid.addWidget(cell_btn, row, col)
            self.port_cells[port] = (cell_btn, service)

        ports_layout.addWidget(self.ports_grid_widget)
        ports_layout.addStretch()

        row2_layout.addWidget(self.ports_card, 44)

        # 2C. Network Topology Sweep
        self.topology_card = QFrame()
        self.topology_card.setProperty("class", "hudCard")
        self.topology_card.setMinimumHeight(200)
        self.topology_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        topo_layout = QVBoxLayout(self.topology_card)
        topo_layout.setContentsMargins(16, 12, 16, 12)
        topo_layout.setSpacing(6)

        topo_title = QLabel("🎯  NETWORK TOPOLOGY SWEEP")
        topo_title.setObjectName("hudCardTitle")

        self.topology_widget = NetworkTopologyWidget()
        self.topology_widget.setMinimumHeight(150)
        self.topology_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        topo_layout.addWidget(topo_title)
        topo_layout.addWidget(self.topology_widget, 1)

        row2_layout.addWidget(self.topology_card, 28)

        main_layout.addLayout(row2_layout, 1)

        # =====================================================================
        # ROW 3: TELEMETRY (30%) + TARGET CONTROLLER (42%) + AI COPILOT (28%)
        # =====================================================================
        row3_layout = QHBoxLayout()
        row3_layout.setSpacing(12)

        # 3A. Core Hardware & Scanner Telemetry
        self.telemetry_card = QFrame()
        self.telemetry_card.setProperty("class", "hudCard")
        self.telemetry_card.setMinimumHeight(240)
        self.telemetry_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        telemetry_layout = QVBoxLayout(self.telemetry_card)
        telemetry_layout.setContentsMargins(16, 12, 16, 12)
        telemetry_layout.setSpacing(8)

        telemetry_title = QLabel("💻  CORE HARDWARE & SCANNER TELEMETRY")
        telemetry_title.setObjectName("hudCardTitle")
        telemetry_layout.addWidget(telemetry_title)

        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(12)

        # Metric 1: Core load
        cpu_box = QVBoxLayout()
        cpu_box.setSpacing(3)
        self.cpu_val = QLabel("44.9%")
        self.cpu_val.setObjectName("telemetryValue")
        cpu_lbl = QLabel("HACKING CORE")
        cpu_lbl.setObjectName("telemetryUnit")
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setProperty("class", "hudProgress")
        self.cpu_bar.setRange(0, 100)
        self.cpu_bar.setValue(45)
        self.cpu_bar.setTextVisible(False)
        self.cpu_bar.setStyleSheet("QProgressBar::chunk { background-color: #00f0ff; border-radius: 2px; }")
        cpu_box.addWidget(self.cpu_val)
        cpu_box.addWidget(cpu_lbl)
        cpu_box.addWidget(self.cpu_bar)

        # Metric 2: Bandwidth
        bw_box = QVBoxLayout()
        bw_box.setSpacing(3)
        self.bw_val = QLabel("267 KB/s")
        self.bw_val.setObjectName("telemetryValue")
        self.bw_val.setStyleSheet("color: #d946ef;")
        bw_lbl = QLabel("BANDWIDTH")
        bw_lbl.setObjectName("telemetryUnit")
        self.bw_bar = QProgressBar()
        self.bw_bar.setProperty("class", "hudProgress")
        self.bw_bar.setRange(0, 1000)
        self.bw_bar.setValue(267)
        self.bw_bar.setTextVisible(False)
        self.bw_bar.setStyleSheet("QProgressBar::chunk { background-color: #d946ef; border-radius: 2px; }")
        bw_box.addWidget(self.bw_val)
        bw_box.addWidget(bw_lbl)
        bw_box.addWidget(self.bw_bar)

        # Metric 3: Active threads
        thread_box = QVBoxLayout()
        thread_box.setSpacing(3)
        self.thread_val = QLabel("16 Active")
        self.thread_val.setObjectName("telemetryValue")
        self.thread_val.setStyleSheet("color: #38bdf8;")
        thread_lbl = QLabel("RUN THREADS")
        thread_lbl.setObjectName("telemetryUnit")
        self.thread_bar = QProgressBar()
        self.thread_bar.setProperty("class", "hudProgress")
        self.thread_bar.setRange(0, 32)
        self.thread_bar.setValue(16)
        self.thread_bar.setTextVisible(False)
        self.thread_bar.setStyleSheet("QProgressBar::chunk { background-color: #38bdf8; border-radius: 2px; }")
        thread_box.addWidget(self.thread_val)
        thread_box.addWidget(thread_lbl)
        thread_box.addWidget(self.thread_bar)

        metrics_layout.addLayout(cpu_box)
        metrics_layout.addLayout(bw_box)
        metrics_layout.addLayout(thread_box)
        telemetry_layout.addLayout(metrics_layout)

        # Mini console log
        self.telemetry_console = QLabel(
            "<span style='color:#10b981;'>[+]</span> Scanner engine initialized...<br>"
            "<span style='color:#10b981;'>[+]</span> Loading modules...<br>"
            "<span style='color:#10b981;'>[+]</span> System check complete.<br>"
            "<span style='color:#10b981;'>[+]</span> Network interface: eth0 (192.168.1.10)<br>"
            "<span style='color:#10b981;'>[+]</span> Ready."
        )
        self.telemetry_console.setStyleSheet("""
            background-color: #050c18;
            border: 1px solid #111e33;
            border-radius: 6px;
            padding: 8px;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 10px;
            color: #94a3b8;
            line-height: 1.4;
        """)
        telemetry_layout.addWidget(self.telemetry_console)
        telemetry_layout.addStretch()

        row3_layout.addWidget(self.telemetry_card, 30)

        # 3B. Target Controller & Surface Intel
        self.action_card = QFrame()
        self.action_card.setProperty("class", "hudCard")
        self.action_card.setMinimumHeight(240)
        self.action_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        action_layout = QVBoxLayout(self.action_card)
        action_layout.setContentsMargins(16, 12, 16, 12)
        action_layout.setSpacing(8)

        action_title = QLabel("🎯  TARGET CONTROLLER & SURFACE INTEL")
        action_title.setObjectName("hudCardTitle")
        action_layout.addWidget(action_title)

        # Target input row
        target_box = QHBoxLayout()
        target_box.setSpacing(8)
        target_lbl = QLabel("Target:")
        target_lbl.setStyleSheet("font-size: 11px; font-weight: 700; color: #cbd5e1;")
        self.target_input = QLineEdit("")
        self.target_input.setPlaceholderText("Enter target IP or domain (e.g. 192.168.1.1)...")
        self.target_input.setStyleSheet("""
            QLineEdit {
                background-color: #060f1d;
                border: 1px solid #162a48;
                border-radius: 6px;
                color: #00f0ff;
                padding: 6px 10px;
                font-size: 11px;
                font-family: 'Consolas', monospace;
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

        self.suggestion_label = QLabel("[SYS_INTEL] Enter a target IP address or domain above to receive AI scenario directives.")
        self.suggestion_label.setWordWrap(True)
        self.suggestion_label.setStyleSheet("font-size: 10px; color: #94a3b8; line-height: 1.3;")
        action_layout.addWidget(self.suggestion_label)

        self.next_tool_label = QLabel("DIRECTIVE: STANDBY (Enter Target)")
        self.next_tool_label.setStyleSheet("font-size: 11px; font-weight: 800; color: #00f0ff;")
        action_layout.addWidget(self.next_tool_label)

        self.run_suggested_btn = QPushButton("▶  Execute Directive (Enter Target to Begin)")
        self.run_suggested_btn.setObjectName("actionBtn")
        self.run_suggested_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.run_suggested_btn.setEnabled(False)
        self.run_suggested_btn.setStyleSheet("""
            QPushButton {
                background-color: #0b1a32;
                color: #38bdf8;
                font-weight: 800;
                font-size: 11px;
                padding: 8px 14px;
                border-radius: 6px;
                border: 1px solid #1e3a64;
            }
            QPushButton:hover {
                background-color: #12284c;
                border-color: #00f0ff;
                color: #ffffff;
            }
            QPushButton:disabled {
                background-color: #081220;
                border: 1px solid #122238;
                color: #475569;
            }
        """)
        self.run_suggested_btn.clicked.connect(self.run_suggested_tool)
        action_layout.addWidget(self.run_suggested_btn)
        action_layout.addStretch()

        row3_layout.addWidget(self.action_card, 42)

        # 3C. AI Copilot Advisory
        self.copilot_card = QFrame()
        self.copilot_card.setProperty("class", "hudCard")
        self.copilot_card.setMinimumHeight(240)
        self.copilot_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        copilot_layout = QVBoxLayout(self.copilot_card)
        copilot_layout.setContentsMargins(16, 12, 16, 12)
        copilot_layout.setSpacing(6)

        copilot_header = QHBoxLayout()
        copilot_title = QLabel("🧠  AI COPILOT ADVISORY")
        copilot_title.setObjectName("hudCardTitle")
        
        self.ai_status_dot = QLabel("● READY")
        self.ai_status_dot.setStyleSheet("color: #10b981; font-size: 10px; font-weight: 800;")
        copilot_header.addWidget(copilot_title)
        copilot_header.addStretch()
        copilot_header.addWidget(self.ai_status_dot)

        self.copilot_output = QTextEdit()
        self.copilot_output.setReadOnly(True)
        self.copilot_output.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.copilot_output.setStyleSheet("""
            QTextEdit {
                background-color: #050c18;
                color: #94a3b8;
                font-family: 'Segoe UI', 'Consolas', sans-serif;
                font-size: 10.5px;
                border: 1px solid #111e33;
                border-radius: 6px;
                padding: 6px;
                line-height: 1.35;
            }
        """)
        self.copilot_output.setHtml(
            "<span style='color:#34d399; font-weight:bold;'>[+] Standard Host Hardening Recommendations [LOW]</span><br>"
            "No immediate high-severity socket vulnerabilities or event anomalies were observed.<br>"
            "Run comprehensive Nmap or web directory vulnerability sweeps."
        )

        # Quick AI Suggestion Chips
        chips_row = QHBoxLayout()
        chips_row.setSpacing(6)
        chip_sqli = QPushButton("📄 SQLi Patch")
        chip_sqli.setProperty("class", "quickChip")
        chip_sqli.setCursor(Qt.CursorShape.PointingHandCursor)
        chip_sqli.clicked.connect(lambda: self._quick_prompt("How to patch SQL injection vulnerabilities in Python and Node.js?"))

        chip_recon = QPushButton("👁️ Recon Strategy")
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

        # AI prompt input row with send button
        prompt_layout = QHBoxLayout()
        prompt_layout.setSpacing(6)
        self.ai_prompt_input = QLineEdit()
        self.ai_prompt_input.setPlaceholderText("Ask AI Copilot (e.g. How to patch SQLi?)...")
        self.ai_prompt_input.setStyleSheet("""
            QLineEdit {
                background-color: #060f1d;
                border: 1px solid #14253e;
                border-radius: 6px;
                color: #e2e8f0;
                padding: 5px 8px;
                font-size: 10px;
            }
            QLineEdit:focus {
                border-color: #2563eb;
            }
        """)
        self.ai_prompt_input.returnPressed.connect(self.run_ai_analysis)

        self.ask_ai_btn = QPushButton("➤")
        self.ask_ai_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ask_ai_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: #ffffff;
                font-weight: 900;
                border-radius: 6px;
                padding: 5px 10px;
                font-size: 12px;
                border: none;
            }
            QPushButton:hover {
                background-color: #3b82f6;
            }
        """)
        self.ask_ai_btn.clicked.connect(self.run_ai_analysis)

        prompt_layout.addWidget(self.ai_prompt_input, 1)
        prompt_layout.addWidget(self.ask_ai_btn)

        copilot_layout.addLayout(copilot_header)
        copilot_layout.addWidget(self.copilot_output, 1)
        copilot_layout.addLayout(chips_row)
        copilot_layout.addLayout(prompt_layout)

        row3_layout.addWidget(self.copilot_card, 28)

        main_layout.addLayout(row3_layout, 1)

        # Timer for live dashboard updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_dashboard)
        self.timer.start(1000)

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
        findings = AICopilot.diagnose(app_state.events, app_state.open_ports)
        lines = [f"<b style='color:#00f0ff;'>[VULNERABILITY AUDIT REPORT - THREAT: {app_state.global_risk}]</b>"]
        lines.append(f"<span style='color:#64748b;'>Open Port Surface: {app_state.open_ports or 'None detected yet'}</span>")
        lines.append(f"<span style='color:#64748b;'>Detected Events: {app_state.events or 'No high-risk signatures'}</span><br>")
        for f in findings:
            title = f.get("title", "Security Finding")
            sev = f.get("severity", "LOW")
            cvss = f.get("cvss", f.get("cvss_score", 3.0))
            desc = f.get("description", "")
            lines.append(f"<span style='color:#34d399;'>● {title} [{sev} - {cvss} CVSS]</span><br><span style='color:#94a3b8;'>{desc}</span><br>")
        self.copilot_output.setHtml("<br>".join(lines))
        self.ai_status_dot.setText("● AUDIT DONE")
        self.ai_status_dot.setStyleSheet("color: #00f0ff; font-size: 10px; font-weight: 800;")

    def _quick_prompt(self, text: str):
        self.ai_prompt_input.setText(text)
        self.run_ai_analysis()

    def update_dashboard(self):
        self.uptime_seconds += 1
        hours = self.uptime_seconds // 3600
        minutes = (self.uptime_seconds % 3600) // 60
        seconds = self.uptime_seconds % 60
        self.system_uptime_val.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        
        current_time = datetime.now().strftime("%H:%M:%S")
        self.system_time_val.setText(f"{current_time}")

        # Dynamic Telemetry Metric Fluctuations
        cpu_load = max(5.0, min(99.0, 44.9 + random.uniform(-4.0, 4.0)))
        self.cpu_val.setText(f"{cpu_load:.1f}%")
        self.cpu_bar.setValue(int(cpu_load))
        
        bw = max(0.0, 267.0 + random.uniform(-20.0, 20.0))
        self.bw_val.setText(f"{int(bw)} KB/s")
        self.bw_bar.setValue(int(bw))
        
        threads = random.randint(14, 18)
        self.thread_val.setText(f"{threads} Active")
        self.thread_bar.setValue(threads)

        # Threat Level
        risk = app_state.global_risk
        score = app_state.risk_score
        self.radar_score_label.setText(f"Threat Score: {score} / 100")
        self.threat_bar.setValue(min(100, max(0, score)))

        if risk.upper() == "LOW":
            self.radar_risk_readout.setText("LOW HAZARD LEVEL")
            self.radar_risk_readout.setStyleSheet("""
                background-color: #041f17; border: 1px solid #059669; color: #10b981;
                font-size: 11px; font-weight: 800; padding: 5px 12px; border-radius: 6px;
            """)
            self.radar_segments.setText("Risk Exposure: Baseline (0/100)")
        elif risk.upper() == "MEDIUM":
            self.radar_risk_readout.setText("MEDIUM HAZARD")
            self.radar_risk_readout.setStyleSheet("""
                background-color: #241407; border: 1px solid #d97706; color: #fbbf24;
                font-size: 11px; font-weight: 800; padding: 5px 12px; border-radius: 6px;
            """)
            self.radar_segments.setText("Risk Exposure: Elevated (40-70/100)")
        else:
            self.radar_risk_readout.setText("CRITICAL HAZARD")
            self.radar_risk_readout.setStyleSheet("""
                background-color: #28080f; border: 1px solid #e11d48; color: #f43f5e;
                font-size: 11px; font-weight: 800; padding: 5px 12px; border-radius: 6px;
            """)
            self.radar_segments.setText("Risk Exposure: Critical (>75/100)")

        # Port Matrix
        open_ports = app_state.open_ports
        for port, (cell_btn, service) in self.port_cells.items():
            if port in open_ports:
                cell_btn.setText(f"{service} : {port}\n● OPEN")
                cell_btn.setProperty("class", "portChipOpen")
            else:
                cell_btn.setText(f"{service} : {port}\n● CLOSED")
                cell_btn.setProperty("class", "portChipClosed")
            cell_btn.style().unpolish(cell_btn)
            cell_btn.style().polish(cell_btn)

        # Target and Directive status
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
                self.run_suggested_btn.setText(f"▶  Execute {app_state.next_tool.upper()} (Auto-Fill)")
            else:
                self.next_tool_label.setText("DIRECTIVE: STANDBY")
                self.run_suggested_btn.setEnabled(False)
                self.run_suggested_btn.setText("▶  Execute Directive (Enter Target to Begin)")
        else:
            self.suggestion_label.setText("[SYS_INTEL] Enter a target IP address or domain above to receive AI scenario directives.")
            self.next_tool_label.setText("DIRECTIVE: STANDBY (Enter Target)")
            self.run_suggested_btn.setEnabled(False)
            self.run_suggested_btn.setText("▶  Execute Directive (Enter Target to Begin)")

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
        self.copilot_output.setHtml("<span style='color:#38bdf8;'>🧠 AI Copilot is analyzing scan metrics and crafting analysis response...</span>")

        self.ai_worker = AIWorkerThread(context_info=context_info, user_prompt=user_prompt)
        self.ai_worker.finished_signal.connect(self._on_ai_analysis_finished)
        self.ai_worker.error_signal.connect(self._on_ai_analysis_error)
        self.ai_worker.start()

    def _on_ai_analysis_finished(self, response: str):
        self.ask_ai_btn.setEnabled(True)
        self.ai_prompt_input.clear()
        self.ai_status_dot.setText("● READY")
        self.ai_status_dot.setStyleSheet("color: #10b981; font-size: 10px; font-weight: 800;")
        self.copilot_output.setText(response)

    def _on_ai_analysis_error(self, err_msg: str):
        self.ask_ai_btn.setEnabled(True)
        self.ai_status_dot.setText("● ERROR")
        self.ai_status_dot.setStyleSheet("color: #f43f5e; font-size: 10px; font-weight: 800;")
        self.copilot_output.setText(f"❌ AI Analysis Error:\n{err_msg}")

    def run_suggested_tool(self):
        target = self.target_input.text().strip() or "127.0.0.1"
        if app_state.next_tool:
            meta = getattr(app_state, "next_action_metadata", {}) or {}
            flags = meta.get("flags", "")
            tool_name = meta.get("tool_key", app_state.next_tool)
            self.run_suggested_signal.emit(f"{tool_name}|{target}|{flags}")