from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt, pyqtSignal, QEvent
from PyQt6.QtGui import QFont, QColor


class ToolIconButton(QWidget):
    """
    Professional tool card with active/inactive states.
    Emits `clicked` when card content is selected.
    """

    clicked = pyqtSignal()

    def __init__(self, icon, tool_name, description="", accent_color="#3b82f6"):
        super().__init__()

        self.accent_color = accent_color
        self._is_active = False

        self.setObjectName("toolCard")

        layout = QVBoxLayout(self)
        layout.setSpacing(6)
        layout.setContentsMargins(10, 10, 10, 10)

        self.icon_btn = QPushButton(icon)
        self.icon_btn.setObjectName("toolIconButton")
        self.icon_btn.setFixedSize(96, 96)
        self.icon_btn.setFont(QFont("Segoe UI Emoji", 34))
        self.icon_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.icon_btn.clicked.connect(self.clicked.emit)

        self.name_label = QLabel(tool_name)
        self.name_label.setObjectName("toolNameLabel")
        self.name_label.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.desc_label = None
        if description:
            self.desc_label = QLabel(description)
            self.desc_label.setObjectName("toolDescLabel")
            self.desc_label.setFont(QFont("Segoe UI", 8))
            self.desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.desc_label.setWordWrap(True)
            layout.addWidget(self.desc_label)

        layout.addWidget(self.icon_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.name_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setMaximumWidth(150)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        clickable_widgets = [self, self.icon_btn, self.name_label]
        if self.desc_label is not None:
            clickable_widgets.append(self.desc_label)

        for widget in clickable_widgets:
            widget.installEventFilter(self)

        self._apply_style()

    def _alpha_color(self, color_hex, alpha):
        color = QColor(color_hex)
        return f"rgba({color.red()}, {color.green()}, {color.blue()}, {alpha})"

    def _apply_style(self):
        accent = self.accent_color
        accent_soft = self._alpha_color(accent, 48)

        if self._is_active:
            icon_bg = accent
            border_color = accent
            name_color = "#f8fbff"
            desc_color = "#dbeafe"
            card_bg = accent_soft
        else:
            icon_bg = "#1c273d"
            border_color = "#3a4a67"
            name_color = "#d7e2f4"
            desc_color = "#91a4c4"
            card_bg = "#111a2e"

        self.setStyleSheet(
            f"""
            QWidget#toolCard {{
                border: 1px solid {border_color};
                border-radius: 12px;
                background-color: {card_bg};
            }}
            QWidget#toolCard:hover {{
                border-color: {accent};
            }}
            QPushButton#toolIconButton {{
                background-color: {icon_bg};
                border: 2px solid {border_color};
                border-radius: 10px;
                color: white;
            }}
            QPushButton#toolIconButton:hover {{
                border-color: {accent};
            }}
            QLabel#toolNameLabel {{
                color: {name_color};
                border: none;
                background: transparent;
            }}
            QLabel#toolDescLabel {{
                color: {desc_color};
                border: none;
                background: transparent;
            }}
            """
        )

    def set_active(self, is_active):
        self._is_active = is_active
        self._apply_style()

    def eventFilter(self, watched, event):
        if (
            watched is not self.icon_btn
            and event.type() == QEvent.Type.MouseButtonRelease
            and event.button() == Qt.MouseButton.LeftButton
        ):
            self.clicked.emit()
            return True

        return super().eventFilter(watched, event)
