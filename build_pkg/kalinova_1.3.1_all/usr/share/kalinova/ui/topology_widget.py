import sys
import math
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFont, QRadialGradient
from core.app_state import app_state

class NetworkTopologyWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.setObjectName("networkTopologyWidget")
        self.setStyleSheet("background-color: transparent;")

        # Target ports with exact radial positions matching screenshot
        self.monitored_ports = [
            (9000, "FastCGI", -90),
            (993, "IMAPS", -45),
            (21, "FTP", 0),
            (22, "SSH", 45),
            (80, "HTTP", 90),
            (443, "HTTPS", 135),
            (3306, "MySQL", 180),
            (8080, "HTTP-Alt", 225)
        ]

        # Animation states
        self.pulse_phase = 0.0
        self.sweep_angle = 0.0

        # Animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(50)  # ~20 FPS for smooth rendering

    def animate(self):
        self.pulse_phase += 0.15
        if self.pulse_phase > 2 * math.pi:
            self.pulse_phase -= 2 * math.pi

        self.sweep_angle += 1.8
        if self.sweep_angle >= 360.0:
            self.sweep_angle -= 360.0

        self.update()

    def paintEvent(self, event):
        width = self.width()
        height = self.height()
        if width <= 0 or height <= 0:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        cx = width / 2.0
        cy = height / 2.0
        radius = min(width, height) * 0.33

        # 1. Draw Radar Grid Lines (Concentric Cyber Rings)
        grid_pen = QPen(QColor(16, 38, 70, 160))
        grid_pen.setWidth(1)
        painter.setPen(grid_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(QPointF(cx, cy), radius * 0.35, radius * 0.35)
        painter.drawEllipse(QPointF(cx, cy), radius * 0.68, radius * 0.68)
        painter.drawEllipse(QPointF(cx, cy), radius, radius)

        # Crosshairs
        cross_pen = QPen(QColor(16, 38, 70, 100))
        cross_pen.setWidth(1)
        painter.setPen(cross_pen)
        painter.drawLine(QPointF(cx - radius * 1.05, cy), QPointF(cx + radius * 1.05, cy))
        painter.drawLine(QPointF(cx, cy - radius * 1.05), QPointF(cx, cy + radius * 1.05))

        # 2. Draw Radar Sweep Vector & Gradient Cone
        sweep_rad = math.radians(self.sweep_angle)
        sx = cx + radius * math.cos(sweep_rad)
        sy = cy + radius * math.sin(sweep_rad)
        
        sweep_pen = QPen(QColor(0, 240, 255, 120))
        sweep_pen.setWidth(2)
        painter.setPen(sweep_pen)
        painter.drawLine(QPointF(cx, cy), QPointF(sx, sy))

        # Sweep trail arc cone
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(0, 240, 255, 15)))
        painter.drawPie(
            int(cx - radius), int(cy - radius), int(radius * 2), int(radius * 2),
            int(-self.sweep_angle * 16), int(45 * 16)
        )

        # 3. Draw Port Nodes and Connection Lines
        open_ports = app_state.open_ports

        for port, service, angle in self.monitored_ports:
            rad = math.radians(angle)
            nx = cx + radius * math.cos(rad)
            ny = cy + radius * math.sin(rad)

            is_open = port in open_ports

            # Radial spoke line
            spoke_pen = QPen(QColor(16, 38, 70, 120))
            spoke_pen.setWidth(1)
            painter.setPen(spoke_pen)
            painter.drawLine(QPointF(cx, cy), QPointF(nx, ny))

            # Draw Node circle
            if is_open:
                # Glowing pulse for open port
                pulse_size = 10.0 + 4.0 * math.sin(self.pulse_phase)
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QBrush(QColor(16, 185, 129, 80)))
                painter.drawEllipse(QPointF(nx, ny), pulse_size, pulse_size)

                painter.setBrush(QBrush(QColor(16, 185, 129)))
                painter.drawEllipse(QPointF(nx, ny), 5, 5)

                label_pen = QPen(QColor(16, 185, 129))
                label_text = f"{service}:{port}"
            else:
                # Solid cyan/blue node on outer ring
                painter.setPen(QPen(QColor(37, 99, 235), 1.5))
                painter.setBrush(QBrush(QColor(0, 240, 255)))
                painter.drawEllipse(QPointF(nx, ny), 4, 4)

                label_pen = QPen(QColor(148, 163, 184))
                label_text = f"{service}:{port}"

            # Styled Text Label
            painter.setPen(label_pen)
            painter.setFont(QFont("Segoe UI", 7, QFont.Weight.Bold))

            # Label positioning relative to node
            if angle == -90:
                # Top
                painter.drawText(int(nx - 45), int(ny - 16), 90, 14, Qt.AlignmentFlag.AlignCenter, label_text)
            elif angle == 90:
                # Bottom
                painter.drawText(int(nx - 45), int(ny + 6), 90, 14, Qt.AlignmentFlag.AlignCenter, label_text)
            elif math.cos(rad) < 0:
                # Left side
                painter.drawText(int(nx - 85), int(ny - 7), 78, 14, Qt.AlignmentFlag.AlignRight, label_text)
            else:
                # Right side
                painter.drawText(int(nx + 7), int(ny - 7), 78, 14, Qt.AlignmentFlag.AlignLeft, label_text)

        # 4. Draw Central Core Target Host Node
        core_grad = QRadialGradient(cx, cy, 18.0)
        core_grad.setColorAt(0.0, QColor(0, 240, 255, 255))
        core_grad.setColorAt(0.5, QColor(0, 240, 255, 160))
        core_grad.setColorAt(1.0, QColor(8, 18, 36, 0))

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(core_grad))
        painter.drawEllipse(QPointF(cx, cy), 18, 18)

        # Center core solid point
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.drawEllipse(QPointF(cx, cy), 4.5, 4.5)

        # Central label "CORE TARGET"
        painter.setPen(QPen(QColor(0, 240, 255)))
        painter.setFont(QFont("Segoe UI", 7, QFont.Weight.Black))
        painter.drawText(int(cx - 45), int(cy - 22), 90, 14, Qt.AlignmentFlag.AlignCenter, "CORE TARGET")
