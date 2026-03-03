"""
Dashboard — Central hub for Kalinova.

Displays all registered tools as interactive cards,
organized by Kali Linux categories. Supports search/filter
and scales dynamically as new tools are added.
"""

import logging
from typing import Dict, Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QScrollArea, QGridLayout, QFrame,
    QSizePolicy, QStackedWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from kalinova.core.tool_registry import ToolRegistry, ToolInfo, KALI_CATEGORIES

logger = logging.getLogger(__name__)


class ToolCard(QFrame):
    """A clickable card representing a single tool."""

    clicked = pyqtSignal(str)  # Emits tool name

    TYPE_COLORS = {
        "assessment": "#00d4ff",
        "action": "#ffa502",
        "utility": "#2ed573",
    }

    TYPE_ICONS = {
        "assessment": "🔍",
        "action": "⚡",
        "utility": "🔧",
    }

    def __init__(self, tool_info: ToolInfo, parent=None):
        super().__init__(parent)
        self._tool_info = tool_info
        self._init_ui()

    def _init_ui(self):
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(260, 170)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        color = self.TYPE_COLORS.get(self._tool_info.tool_type, "#2a2a4e")
        available_opacity = "1.0" if self._tool_info.is_available else "0.5"

        self.setStyleSheet(f"""
            QFrame {{
                background-color: #1a1a2e;
                border: 1px solid #2a2a4e;
                border-radius: 14px;
                padding: 18px;
                border-top: 3px solid {color};
            }}
            QFrame:hover {{
                background-color: #22223a;
                border-color: {color};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        # Top: Icon + Name
        header = QHBoxLayout()

        icon = self.TYPE_ICONS.get(self._tool_info.tool_type, "🛠️")
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 28px; background: transparent;")
        header.addWidget(icon_label)

        name_label = QLabel(self._tool_info.display_name)
        name_font = QFont()
        name_font.setPointSize(16)
        name_font.setBold(True)
        name_label.setFont(name_font)
        name_label.setStyleSheet(f"color: {color}; background: transparent;")
        header.addWidget(name_label)

        header.addStretch()
        layout.addLayout(header)

        # Description
        desc = QLabel(self._tool_info.description[:80] + ("..." if len(self._tool_info.description) > 80 else ""))
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #8899aa; font-size: 12px; background: transparent;")
        layout.addWidget(desc)

        layout.addStretch()

        # Footer: Type badge + availability
        footer = QHBoxLayout()

        type_label = QLabel(self._tool_info.tool_type.upper())
        type_label.setStyleSheet(f"""
            color: {color};
            font-size: 10px;
            font-weight: bold;
            background: transparent;
            padding: 2px 8px;
            border: 1px solid {color};
            border-radius: 8px;
        """)
        footer.addWidget(type_label)

        footer.addStretch()

        if self._tool_info.is_available:
            status = QLabel("✅ Ready")
            status.setStyleSheet("color: #2ed573; font-size: 11px; background: transparent;")
        else:
            status = QLabel("❌ Not Installed")
            status.setStyleSheet("color: #ff4757; font-size: 11px; background: transparent;")

        footer.addWidget(status)
        layout.addLayout(footer)

    def mousePressEvent(self, event):
        if self._tool_info.is_available:
            self.clicked.emit(self._tool_info.name)
        super().mousePressEvent(event)


class Dashboard(QWidget):
    """
    Central dashboard showing all registered tools.

    Dynamically populates from ToolRegistry, supports
    search/filter, and organizes tools by Kali category.
    """

    tool_selected = pyqtSignal(str)  # Emits tool name

    def __init__(self, registry: ToolRegistry, parent=None):
        super().__init__(parent)
        self._registry = registry
        self._cards: Dict[str, ToolCard] = {}
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        # Header
        header = self._build_header()
        layout.addWidget(header)

        # Search bar
        search_layout = QHBoxLayout()

        self._search_input = QLineEdit()
        self._search_input.setPlaceholderText("🔍 Search tools...")
        self._search_input.setMinimumHeight(40)
        self._search_input.setStyleSheet("""
            QLineEdit {
                font-size: 15px;
                padding-left: 12px;
                border-radius: 10px;
            }
        """)
        self._search_input.textChanged.connect(self._filter_tools)
        search_layout.addWidget(self._search_input)

        # Stats
        total = self._registry.tool_count
        available = self._registry.available_count
        stats_label = QLabel(f"📦 {available}/{total} tools available")
        stats_label.setStyleSheet("color: #8899aa; font-size: 13px; min-width: 180px;")
        search_layout.addWidget(stats_label)

        layout.addLayout(search_layout)

        # Scrollable tool grid
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        self._grid_container = QWidget()
        self._grid_layout = QVBoxLayout(self._grid_container)
        self._grid_layout.setSpacing(20)

        self._populate_tools()

        scroll.setWidget(self._grid_container)
        layout.addWidget(scroll)

    def _build_header(self) -> QFrame:
        """Build the dashboard header."""
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a1a2e, stop:1 #16213e);
                border: 1px solid #0f3460;
                border-radius: 14px;
                padding: 24px;
            }
        """)
        layout = QVBoxLayout(header)
        layout.setSpacing(6)

        title = QLabel("🔐 Kalinova Security Suite")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #00d4ff; background: transparent;")
        layout.addWidget(title)

        subtitle = QLabel(
            "Intelligent GUI wrappers for Kali Linux security tools — "
            "powered by Machine Learning"
        )
        subtitle.setStyleSheet(
            "color: #8899aa; font-size: 14px; background: transparent;"
        )
        layout.addWidget(subtitle)

        return header

    def _populate_tools(self):
        """Populate the tool grid organized by category."""
        categories = self._registry.get_categories_with_tools()

        for cat_key, tools in categories.items():
            cat_name = KALI_CATEGORIES.get(cat_key, cat_key.replace("_", " ").title())

            # Category header
            cat_label = QLabel(f"📂 {cat_name}")
            cat_font = QFont()
            cat_font.setPointSize(16)
            cat_font.setBold(True)
            cat_label.setFont(cat_font)
            cat_label.setStyleSheet("color: #00d4ff; padding-top: 8px;")
            self._grid_layout.addWidget(cat_label)

            # Tool cards in horizontal flow
            flow_layout = QHBoxLayout()
            flow_layout.setSpacing(16)

            for tool in tools:
                card = ToolCard(tool)
                card.clicked.connect(self.tool_selected.emit)
                self._cards[tool.name] = card
                flow_layout.addWidget(card)

            flow_layout.addStretch()
            self._grid_layout.addLayout(flow_layout)

        self._grid_layout.addStretch()

    def _filter_tools(self, search_text: str):
        """Filter visible tools based on search text."""
        query = search_text.lower().strip()

        for name, card in self._cards.items():
            tool = self._registry.get(name)
            if not tool:
                continue

            visible = (
                not query or
                query in tool.name.lower() or
                query in tool.display_name.lower() or
                query in tool.description.lower() or
                query in tool.category.lower() or
                query in tool.tool_type.lower()
            )
            card.setVisible(visible)

    def refresh(self):
        """Refresh tool availability status."""
        self._registry.refresh_availability()
        # Rebuild UI
        # Clear existing
        while self._grid_layout.count():
            item = self._grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                while item.layout().count():
                    sub = item.layout().takeAt(0)
                    if sub.widget():
                        sub.widget().deleteLater()

        self._cards.clear()
        self._populate_tools()
