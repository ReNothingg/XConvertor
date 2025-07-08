from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from .widgets.drop_area import DropArea

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XConvertor")
        self.setGeometry(100, 100, 800, 600)

        # Загрузка темной темы
        try:
            with open("assets/styles/dark_theme.qss", "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Не удалось загрузить файл темы.")


        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        self.drop_area = DropArea()
        layout.addWidget(self.drop_area)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            print(f"Перетащен файл: {f}")
            # Здесь будет логика обработки файла