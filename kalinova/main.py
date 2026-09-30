import sys
from PyQt6.QtWidgets import QApplication

def main():
    """Application entrypoint for kalinova console script and library launcher."""
    from ui.main_window import MainWindow
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())   