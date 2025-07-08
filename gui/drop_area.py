from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

class DropArea(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setText("\n\nПеретащите файлы сюда\n\n")
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 5px;
                font-size: 16px;
                color: #aaa;
            }
        """)