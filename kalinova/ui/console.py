from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit


class Console(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setFixedHeight(150)

        layout.addWidget(self.output)
        self.setLayout(layout)

    def log(self, message):
        self.output.append(message)