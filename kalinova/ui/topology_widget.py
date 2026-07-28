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

        # Target ports to draw
        self.monitored_ports = [
            (21, "FTP"), (22, "SSH"), (80, "HTTP"), (443, "HTTPS"),
            (3306, "MySQL"), (8080, "HTTP-Alt"), (9000, "FastCGI"), (993, "IMAPS")
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

        self.sweep_angle += 1.5
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
        radius = min(width, height) * 0.35

        # 1. Draw Radar Grid Lines (Low Opacity Steel Blue)
        grid_pen = QPen(QColor(28, 42, 71, 100))
        grid_pen.setWidth(1)
        painter.setPen(grid_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(QPointF(cx, cy), radius * 0.4, radius * 0.4)
        painter.drawEllipse(QPointF(cx, cy), radius * 0.7, radius * 0.7)
        painter.drawEllipse(QPointF(cx, cy), radius, radius)

        # 2. Draw Radar Sweep Vector (Electric Cyan)
        sweep_rad = math.radians(self.sweep_angle)
        sx = cx + radius * math.cos(sweep_rad)
        sy = cy + radius * math.sin(sweep_rad)
        
        sweep_pen = QPen(QColor(0, 240, 255, 60))
        sweep_pen.setWidth(2)
        painter.setPen(sweep_pen)
        painter.drawLine(QPointF(cx, cy), QPointF(sx, sy))

        # Sweep trail arc
        trail_pen = QPen(QColor(0, 240, 255, 20))
        trail_pen.setWidth(1)
        painter.setPen(trail_pen)
        painter.setBrush(QBrush(QColor(0, 240, 255, 5)))
        painter.drawPie(
            int(cx - radius), int(cy - radius), int(radius * 2), int(radius * 2),
            int(-self.sweep_angle * 16), int(35 * 16)
        )

        # 3. Draw Connection Lines and Sub-nodes
        open_ports = app_state.open_ports
        node_count = len(self.monitored_ports)

        for idx, (port, service) in enumerate(self.monitored_ports):
            angle = (360.0 / node_count) * idx
            rad = math.radians(angle)
            nx = cx + radius * math.cos(rad)
            ny = cy + radius * math.sin(rad)

            is_open = port in open_ports

            # Set connection pen colors
            if is_open:
                line_pen = QPen(QColor(16, 185, 129, 200)) # Neon Green
                line_pen.setWidth(2)
            else:
                line_pen = QPen(QColor(30, 41, 59, 150)) # Steel Blue/Gray
                line_pen.setWidth(1)
                line_pen.setStyle(Qt.PenStyle.DashLine)

            painter.setPen(line_pen)
            painter.drawLine(QPointF(cx, cy), QPointF(nx, ny))

            # Draw Port Nodes
            if is_open:
                # Glowing outer pulse rings
                pulse_size = 12.0 + 5.0 * math.sin(self.pulse_phase)
                pulse_color = QColor(16, 185, 129, int(100 - (pulse_size - 7.0) * 10))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QBrush(pulse_color))
                painter.drawEllipse(QPointF(nx, ny), pulse_size, pulse_size)

                # Core solid green node
                painter.setBrush(QBrush(QColor(16, 185, 129)))
                painter.drawEllipse(QPointF(nx, ny), 6, 6)

                # Vibrant Label
                label_pen = QPen(QColor(16, 185, 129))
                painter.setPen(label_pen)
                label_text = f"{service}:{port} [OPEN]"
            else:
                # Dim un-scanned hollow node
                node_pen = QPen(QColor(74, 92, 122))
                node_pen.setWidthF(1.5)
                painter.setPen(node_pen)
                painter.setBrush(QBrush(QColor(15, 22, 36)))
                painter.drawEllipse(QPointF(nx, ny), 5, 5)

                # Dim Label
                label_pen = QPen(QColor(74, 92, 122))
                painter.setPen(label_pen)
                label_text = f"{service}:{port}"

            # Styled Text Labels centered on radial vectors
            painter.setFont(QFont("Courier New", 7, QFont.Weight.Bold))
            # Offset labels outwards from target coordinates
            tx_offset = 18.0 * math.cos(rad)
            ty_offset = 18.0 * math.sin(rad)
            
            # Text alignment adjustment based on side
            if math.cos(rad) < -0.1:
                # Left side - align text right
                x_coord = int(nx + tx_offset - 75)
                y_coord = int(ny + ty_offset + 3)
                align = Qt.AlignmentFlag.AlignRight
            else:
                # Right side - align text left
                x_coord = int(nx + tx_offset)
                y_coord = int(ny + ty_offset + 3)
                align = Qt.AlignmentFlag.AlignLeft

            # Robust coordinate checks to prevent access violation in headless/offscreen environments
            if x_coord >= 0 and y_coord >= 0 and x_coord + 75 <= width and y_coord + 15 <= height:
                painter.drawText(x_coord, y_coord, 70, 15, align, label_text)

        # 4. Draw central core "Target Host" node
        core_grad = QRadialGradient(cx, cy, 22.0)
        core_grad.setColorAt(0.0, QColor(0, 240, 255, 255))
        core_grad.setColorAt(0.4, QColor(0, 240, 255, 150))
        core_grad.setColorAt(1.0, QColor(14, 23, 40, 0))

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(core_grad))
        painter.drawEllipse(QPointF(cx, cy), 22, 22)

        # Center core solid point
        painter.setBrush(QBrush(QColor(0, 240, 255)))
        painter.drawEllipse(QPointF(cx, cy), 6, 6)

        # Central label "CORE TARGET"
        painter.setPen(QPen(QColor(0, 240, 255)))
        painter.setFont(QFont("Segoe UI", 8, QFont.Weight.Black))
        
        cx_text_x = int(cx - 50)
        cx_text_y = int(cy - 30)
        if cx_text_x >= 0 and cx_text_y >= 0 and cx_text_x + 100 <= width and cx_text_y + 15 <= height:
            painter.drawText(cx_text_x, cx_text_y, 100, 15, Qt.AlignmentFlag.AlignCenter, "CORE TARGET")
