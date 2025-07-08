from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from core.file_utils import get_file_type
from .conversion_dialog import ConversionDialog
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        
        self.setWindowTitle("XConvertor")
        self.setGeometry(200, 200, 600, 400)
        
        
        self.setAcceptDrops(True)

        
        try:
            with open("assets/styles/dark_theme.qss", "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("ПРЕДУПРЕЖДЕНИЕ: Файл стилей dark_theme.qss не найден.")

        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        
        self.drop_area = QLabel("\n\nПеретащите файлы сюда\n\n")
        self.drop_area.setAlignment(Qt.AlignCenter)
        self.drop_area.setObjectName("DropArea") 
        layout.addWidget(self.drop_area)

    

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction() 
            self.drop_area.setText("\n\nОтпустите, чтобы добавить\n\n")
        else:
            event.ignore() 

    def dragLeaveEvent(self, event):
        self.drop_area.setText("\n\nПеретащите файлы сюда\n\n")

    def dropEvent(self, event):
        self.drop_area.setText("\n\nПеретащите файлы сюда\n\n")
        
        
        urls = event.mimeData().urls()
        if not urls:
            return

        
        filepath = urls[0].toLocalFile()
        
        
        if not os.path.isfile(filepath):
            QMessageBox.warning(self, "Ошибка", "Перетаскивание папок пока не поддерживается.")
            return

        
        file_type = get_file_type(filepath)
        
        if file_type == 'unknown':
            self.handle_unknown_file(filepath)
        else:
            
            dialog = ConversionDialog(filepath, file_type, self)
            dialog.exec_()

    def handle_unknown_file(self, filepath):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Неизвестный файл")
        msg_box.setText(f"Формат файла '{os.path.basename(filepath)}' не поддерживается.")
        msg_box.setInformativeText("Хотите найти информацию о конвертации этого формата в интернете?")
        
        
        search_button = msg_box.addButton("Найти в интернете", QMessageBox.ActionRole)
        cancel_button = msg_box.addButton("Отмена", QMessageBox.RejectRole)
        
        msg_box.exec_()
        
        if msg_box.clickedButton() == search_button:
            import webbrowser
            from urllib.parse import quote
            query = f"how to convert {os.path.splitext(filepath)[1]} file"
            url = f"https://www.google.com/search?q={quote(query)}"
            webbrowser.open(url)