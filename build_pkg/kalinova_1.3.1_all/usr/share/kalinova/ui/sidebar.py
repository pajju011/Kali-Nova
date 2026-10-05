import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PyQt6.QtCore import pyqtSignal, QSize, Qt, QRectF
from PyQt6.QtGui import QIcon, QPainter, QPixmap
from PyQt6.QtSvg import QSvgRenderer
from ui.icon_manager import get_nav_icon_path, get_tool_icon_path


class SidebarDragonGraphic(QWidget):
    """Subtle Kali Dragon graphic matching reference image at bottom of sidebar."""

    def __init__(self):
        super().__init__()
        self.setFixedHeight(75)
        self.setStyleSheet("background: transparent;")
        icon_path = get_tool_icon_path("kalinova")
        self._renderer = QSvgRenderer(icon_path) if icon_path and os.path.exists(icon_path) else None

    def paintEvent(self, event):
        super().paintEvent(event)
        if self._renderer and self._renderer.isValid():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setOpacity(0.35)
            dw = float(self.width() - 24)
            dh = dw * 0.65
            dy = float(self.height() - dh)
            self._renderer.render(painter, QRectF(12.0, dy, dw, dh))
            painter.end()


class Sidebar(QWidget):

    navigate = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setObjectName("sideBar")
        self.setMinimumWidth(210)
        self.setMaximumWidth(230)

        self._active_target = "Dashboard"
        self._buttons = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 16, 12, 16)
        layout.setSpacing(4)

        # -----------------------
        # MAIN GROUP
        # -----------------------
        main_header = QLabel("MAIN")
        main_header.setStyleSheet("""
            font-size: 10px;
            font-weight: 800;
            color: #475569;
            letter-spacing: 1.2px;
            padding-left: 10px;
            padding-bottom: 4px;
        """)
        layout.addWidget(main_header)

        self._add_nav_item(layout, "Dashboard", "dashboard", "Dashboard")
        self._add_nav_item(layout, "Recon", "recon", "Recon")
        self._add_nav_item(layout, "Web Testing", "web", "Web")
        self._add_nav_item(layout, "Exploitation", "exploitation", "Auth")
        self._add_nav_item(layout, "Authentication", "auth", "Auth")
        self._add_nav_item(layout, "Network", "network", "Network")
        self._add_nav_item(layout, "Reports", "reports", "Reports")
        self._add_nav_item(layout, "Settings", "settings", "Settings")

        # -----------------------
        # TOOLS GROUP
        # -----------------------
        tools_header = QLabel("TOOLS")
        tools_header.setStyleSheet("""
            font-size: 10px;
            font-weight: 800;
            color: #475569;
            letter-spacing: 1.2px;
            padding-left: 10px;
            padding-top: 14px;
            padding-bottom: 4px;
        """)
        layout.addWidget(tools_header)

        self._add_nav_item(layout, "Toolbox", "toolbox", "Recon")
        self._add_nav_item(layout, "Logs", "logs", "Reports")

        layout.addStretch()

        # Dragon illustration above footer matching reference design
        self.dragon_graphic = SidebarDragonGraphic()
        layout.addWidget(self.dragon_graphic)

        # -----------------------
        # FOOTER
        # -----------------------
        footer_frame = QFrame()
        footer_frame.setObjectName("sidebarFooter")
        footer_frame.setStyleSheet("""
            QFrame#sidebarFooter {
                background: transparent;
                border-top: 1px solid #101c30;
                padding-top: 10px;
            }
        """)
        footer_layout = QVBoxLayout(footer_frame)
        footer_layout.setContentsMargins(8, 8, 8, 4)
        footer_layout.setSpacing(2)

        v_label = QLabel("KALINOVA v1.0.0")
        v_label.setStyleSheet("color: #cbd5e1; font-size: 11px; font-weight: 800; letter-spacing: 0.5px;")
        sub_label = QLabel("Built on Kali Linux")
        sub_label.setStyleSheet("color: #64748b; font-size: 9px; font-weight: 600;")

        footer_layout.addWidget(v_label)
        footer_layout.addWidget(sub_label)

        layout.addWidget(footer_frame)

        self._update_button_styles()

    def _add_nav_item(self, layout, text: str, icon_id: str, nav_target: str):
        btn = QPushButton(f"  {text}")
        btn.setObjectName("navButton")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        icon_path = get_nav_icon_path(icon_id)
        if icon_path and os.path.exists(icon_path):
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(18, 18))
        
        btn.clicked.connect(lambda _, t=nav_target, b=text: self._on_item_clicked(t, b))
        layout.addWidget(btn)
        self._buttons[text] = (btn, nav_target)

    def _on_item_clicked(self, nav_target: str, button_key: str):
        self._active_target = button_key
        self._update_button_styles()
        self.navigate.emit(nav_target)

    def set_active_page(self, page_name: str):
        # Match button key or nav target
        for key, (btn, target) in self._buttons.items():
            if target.lower() == page_name.lower() or key.lower() == page_name.lower():
                self._active_target = key
                break
        self._update_button_styles()

    def _update_button_styles(self):
        for key, (btn, target) in self._buttons.items():
            is_active = (key == self._active_target)
            if is_active:
                btn.setStyleSheet("""
                    QPushButton {
                        text-align: left;
                        padding: 8px 12px;
                        border-radius: 8px;
                        background-color: #1d4ed8;
                        color: #ffffff;
                        font-weight: 700;
                        font-size: 12px;
                        border: none;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        text-align: left;
                        padding: 8px 12px;
                        border-radius: 8px;
                        background-color: transparent;
                        color: #94a3b8;
                        font-weight: 500;
                        font-size: 12px;
                        border: none;
                    }
                    QPushButton:hover {
                        background-color: #0f1c32;
                        color: #f1f5f9;
                    }
                """)
