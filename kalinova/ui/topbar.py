from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox


class TopBar(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()

        self.title = QLabel("KALINOVA OS")
        self.title.setStyleSheet("font-size:18px; font-weight:bold;")

        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["Beginner Mode", "Expert Mode"])

        self.risk_label = QLabel("Global Risk: LOW")
        self.risk_label.setStyleSheet("color: green; font-weight:bold;")

        layout.addWidget(self.title)
        layout.addStretch()
        layout.addWidget(self.mode_selector)
        layout.addWidget(self.risk_label)

        self.setLayout(layout)