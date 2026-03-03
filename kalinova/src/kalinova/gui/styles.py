"""
Global stylesheet for Kalinova GUI.

Dark-themed, modern design system used consistently
across all windows and widgets.
"""

STYLESHEET = """
/* ======================================
   Kalinova Global Theme — Dark Mode
   ====================================== */

/* Base */
QWidget {
    background-color: #0f0f1a;
    color: #e0e0e0;
    font-family: 'Segoe UI', 'Noto Sans', 'DejaVu Sans', sans-serif;
    font-size: 14px;
}

QMainWindow {
    background-color: #0f0f1a;
}

/* Labels */
QLabel {
    color: #e0e0e0;
    background: transparent;
}

QLabel#title {
    font-size: 26px;
    font-weight: bold;
    color: #00d4ff;
}

QLabel#subtitle {
    font-size: 15px;
    color: #8899aa;
}

QLabel#section-header {
    font-size: 18px;
    font-weight: bold;
    color: #00d4ff;
    padding: 10px 0;
}

/* Input fields */
QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #1a1a2e;
    border: 1px solid #2a2a4e;
    border-radius: 8px;
    padding: 10px 14px;
    color: #e0e0e0;
    font-size: 14px;
    selection-background-color: #0f3460;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 1px solid #00d4ff;
}

QLineEdit:disabled {
    background-color: #12121e;
    color: #555;
}

/* ComboBox */
QComboBox {
    background-color: #1a1a2e;
    border: 1px solid #2a2a4e;
    border-radius: 8px;
    padding: 8px 14px;
    color: #e0e0e0;
    min-width: 120px;
}

QComboBox:hover {
    border: 1px solid #00d4ff;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox QAbstractItemView {
    background-color: #1a1a2e;
    border: 1px solid #2a2a4e;
    color: #e0e0e0;
    selection-background-color: #0f3460;
}

/* Buttons */
QPushButton {
    background-color: #0f3460;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 10px 24px;
    font-size: 14px;
    font-weight: bold;
    min-height: 36px;
}

QPushButton:hover {
    background-color: #1a4a7a;
}

QPushButton:pressed {
    background-color: #0a2540;
}

QPushButton:disabled {
    background-color: #1a1a2e;
    color: #555;
}

QPushButton#primary {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #00d4ff, stop:1 #0099cc);
    color: #000;
    font-weight: bold;
}

QPushButton#primary:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #33ddff, stop:1 #00aadd);
}

QPushButton#danger {
    background-color: #e53e3e;
    color: #ffffff;
}

QPushButton#danger:hover {
    background-color: #ff5555;
}

QPushButton#success {
    background-color: #2ed573;
    color: #000;
}

QPushButton#success:hover {
    background-color: #44e088;
}

/* CheckBox */
QCheckBox {
    spacing: 8px;
    color: #e0e0e0;
    background: transparent;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border-radius: 4px;
    border: 2px solid #2a2a4e;
    background-color: #1a1a2e;
}

QCheckBox::indicator:checked {
    background-color: #00d4ff;
    border-color: #00d4ff;
}

QCheckBox::indicator:hover {
    border-color: #00d4ff;
}

/* SpinBox */
QSpinBox {
    background-color: #1a1a2e;
    border: 1px solid #2a2a4e;
    border-radius: 8px;
    padding: 8px;
    color: #e0e0e0;
}

/* GroupBox */
QGroupBox {
    border: 1px solid #2a2a4e;
    border-radius: 10px;
    margin-top: 16px;
    padding-top: 20px;
    font-weight: bold;
    color: #00d4ff;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 4px 12px;
    color: #00d4ff;
}

/* ScrollArea */
QScrollArea {
    border: none;
    background: transparent;
}

QScrollBar:vertical {
    background: #0f0f1a;
    width: 10px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background: #2a2a4e;
    border-radius: 5px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: #3a3a6e;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    border: none;
    background: none;
    height: 0;
}

/* Table */
QTableWidget {
    background-color: #12121e;
    border: 1px solid #2a2a4e;
    border-radius: 8px;
    gridline-color: #2a2a4e;
    color: #e0e0e0;
}

QTableWidget::item {
    padding: 8px;
}

QTableWidget::item:selected {
    background-color: #0f3460;
}

QHeaderView::section {
    background-color: #1a1a2e;
    color: #00d4ff;
    padding: 10px;
    border: 1px solid #2a2a4e;
    font-weight: bold;
}

/* Tab Widget */
QTabWidget::pane {
    border: 1px solid #2a2a4e;
    border-radius: 8px;
    background-color: #0f0f1a;
    padding: 10px;
}

QTabBar::tab {
    background-color: #1a1a2e;
    color: #8899aa;
    padding: 10px 20px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    margin-right: 4px;
}

QTabBar::tab:selected {
    background-color: #0f3460;
    color: #00d4ff;
}

QTabBar::tab:hover {
    background-color: #2a2a4e;
    color: #e0e0e0;
}

/* Progress Bar */
QProgressBar {
    background-color: #1a1a2e;
    border: 1px solid #2a2a4e;
    border-radius: 8px;
    text-align: center;
    color: #e0e0e0;
    min-height: 20px;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #00d4ff, stop:1 #0099cc);
    border-radius: 7px;
}

/* StatusBar */
QStatusBar {
    background-color: #0a0a14;
    color: #8899aa;
    border-top: 1px solid #2a2a4e;
}

/* ToolTip */
QToolTip {
    background-color: #1a1a2e;
    color: #e0e0e0;
    border: 1px solid #0f3460;
    border-radius: 6px;
    padding: 6px;
}

/* Menu */
QMenuBar {
    background-color: #0a0a14;
    color: #e0e0e0;
    border-bottom: 1px solid #2a2a4e;
}

QMenuBar::item:selected {
    background-color: #0f3460;
}

QMenu {
    background-color: #1a1a2e;
    border: 1px solid #2a2a4e;
    color: #e0e0e0;
}

QMenu::item:selected {
    background-color: #0f3460;
}

/* File Dialog styling */
QFileDialog {
    background-color: #0f0f1a;
}

/* Splitter */
QSplitter::handle {
    background-color: #2a2a4e;
    width: 2px;
}
"""
