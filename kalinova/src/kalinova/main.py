"""
Kalinova — Main application entry point.

Initializes the Qt application, shows the disclaimer on
first launch, and displays the main window.

Usage:
    python -m kalinova.main
"""

import sys
import logging
import os

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from kalinova.gui.main_window import MainWindow
from kalinova.gui.disclaimer_dialog import DisclaimerDialog


def setup_logging():
    """Configure application logging."""
    log_dir = os.path.expanduser("~/.kalinova/logs")
    os.makedirs(log_dir, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(
                os.path.join(log_dir, "kalinova.log"),
                encoding="utf-8",
            ),
            logging.StreamHandler(sys.stdout),
        ],
    )


def main():
    """Main application entry point."""
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Kalinova starting...")

    app = QApplication(sys.argv)
    app.setApplicationName("Kalinova")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Kalinova")

    # Set application icon if available
    icon_path = "/opt/kalinova/assets/icon.png"
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    # Show disclaimer on first launch
    if not DisclaimerDialog.was_accepted():
        disclaimer = DisclaimerDialog()
        result = disclaimer.exec()
        if result != disclaimer.DialogCode.Accepted:
            logger.info("Disclaimer declined. Exiting.")
            sys.exit(0)

    # Create and show main window
    window = MainWindow()
    window.show()

    logger.info("Kalinova ready.")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
