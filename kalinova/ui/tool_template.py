from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QStackedWidget,
    QGroupBox,
    QPushButton,
    QScrollArea,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from ui.tool_icon_button import ToolIconButton


class ToolModulePage(QScrollArea):
    """
    Shared module layout:
    - Header with title/subtitle
    - Horizontal tool cards
    - Empty state + stacked tool panels
    """

    validation_error = pyqtSignal(str)

    def __init__(self, title, accent_color, subtitle):
        super().__init__()

        self.accent_color = accent_color
        self._selected_tool = None
        self._tool_buttons = {}
        self._tool_panel_index = {}
        self._tool_focus_widget = {}

        self.setObjectName("toolModulePage")
        self.setWidgetResizable(True)
        self.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        # Create a container widget for all the content
        self.container = QWidget()
        self.container.setObjectName("toolModulePageContainer")
        self.container.setStyleSheet("background: transparent;")

        main_layout = QVBoxLayout(self.container)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(16)

        # Header
        header = QFrame()
        header.setObjectName("toolModuleHeader")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(20, 16, 20, 16)
        header_layout.setSpacing(6)

        title_label = QLabel(title)
        title_label.setObjectName("toolModuleTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {accent_color};")

        subtitle_label = QLabel(subtitle)
        subtitle_label.setObjectName("toolModuleSubtitle")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setWordWrap(True)

        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        main_layout.addWidget(header)

        # Tool cards row
        tools_row = QFrame()
        tools_row.setObjectName("toolRow")
        self.tools_layout = QHBoxLayout(tools_row)
        self.tools_layout.setSpacing(14)
        self.tools_layout.setContentsMargins(8, 4, 8, 4)
        self.tools_layout.addStretch()
        main_layout.addWidget(tools_row)

        # Panel area
        panel_container = QFrame()
        panel_container.setObjectName("panelContainer")
        panel_layout = QVBoxLayout(panel_container)
        panel_layout.setContentsMargins(16, 16, 16, 16)

        self.panel_stack = QStackedWidget()
        self.empty_panel = self._build_empty_panel()
        self.panel_stack.addWidget(self.empty_panel)

        panel_layout.addWidget(self.panel_stack)
        main_layout.addWidget(panel_container, 1)

        self.setWidget(self.container)

    def _build_empty_panel(self):
        empty = QWidget()
        layout = QVBoxLayout(empty)
        layout.setContentsMargins(24, 40, 24, 40)
        layout.setSpacing(8)

        hint_title = QLabel("Select a tool to begin")
        hint_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint_title.setObjectName("emptyStateTitle")
        hint_title.setFont(QFont("Segoe UI", 16, QFont.Weight.DemiBold))

        hint_subtitle = QLabel(
            "Tool options and input fields appear here after you choose a tool card above."
        )
        hint_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint_subtitle.setWordWrap(True)
        hint_subtitle.setObjectName("emptyStateSubtitle")

        layout.addStretch()
        layout.addWidget(hint_title)
        layout.addWidget(hint_subtitle)
        layout.addStretch()

        return empty

    def create_panel(self, title):
        panel = QGroupBox(title)
        panel.setProperty("class", "toolPanelGroup")
        panel_layout = QVBoxLayout(panel)
        panel_layout.setSpacing(10)
        panel_layout.setContentsMargins(14, 18, 14, 14)
        return panel, panel_layout

    def create_primary_button(self, text):
        button = QPushButton(text)
        button.setProperty("role", "primary")
        button.setMinimumHeight(42)
        return button

    def create_secondary_button(self, text):
        button = QPushButton(text)
        button.setProperty("role", "secondary")
        button.setMinimumHeight(38)
        return button

    def add_tool(self, tool_id, icon, name, description, panel, focus_widget=None):
        tool_button = ToolIconButton(icon, name, description, self.accent_color)
        tool_button.clicked.connect(lambda key=tool_id: self.activate_tool(key))

        # Insert before stretch so cards stay left-aligned
        insert_index = max(self.tools_layout.count() - 1, 0)
        self.tools_layout.insertWidget(insert_index, tool_button)

        panel_index = self.panel_stack.addWidget(panel)

        self._tool_buttons[tool_id] = tool_button
        self._tool_panel_index[tool_id] = panel_index
        self._tool_focus_widget[tool_id] = focus_widget

    def activate_tool(self, tool_id):
        if tool_id not in self._tool_panel_index:
            return

        self._selected_tool = tool_id
        self.panel_stack.setCurrentIndex(self._tool_panel_index[tool_id])

        for key, button in self._tool_buttons.items():
            button.set_active(key == tool_id)

        focus_widget = self._tool_focus_widget.get(tool_id)
        if focus_widget is not None:
            focus_widget.setFocus()
            if hasattr(focus_widget, "selectAll"):
                focus_widget.selectAll()

    def emit_validation_error(self, message):
        self.validation_error.emit(message)

    def clear_tool_selection(self):
        self._selected_tool = None
        self.panel_stack.setCurrentIndex(0)

        for button in self._tool_buttons.values():
            button.set_active(False)
