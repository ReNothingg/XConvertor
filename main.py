import sys
import os
import webbrowser
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                             QWidget, QMessageBox, QComboBox, QPushButton)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PIL import Image
import filetype


DARK_STYLE = """
QWidget {
    background-color: 
    color: 
    font-family: Arial, sans-serif;
}
QMainWindow {
    background-color: 
}
QLabel {
    font-size: 16px;
    font-weight: bold;
}
QComboBox {
    background-color: 
    border: 1px solid 
    padding: 5px;
    border-radius: 3px;
}
QPushButton {
    background-color: 
    color: 
    border: none;
    padding: 10px;
    border-radius: 5px;
    font-size: 14px;
}
QPushButton:hover {
    background-color: 
}
QPushButton:pressed {
    background-color: 
}
QMessageBox {
    background-color: 
}
"""

class XConvertor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XConvertor")
        self.setGeometry(100, 100, 500, 300)
        
        
        self.setAcceptDrops(True)
        
        self.file_path = None 

        self.setup_ui()

    def setup_ui(self):
        """Настройка пользовательского интерфейса."""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        layout = QVBoxLayout(self.central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.info_label = QLabel("Перетащите файл сюда")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setFont(QFont("Arial", 20))
        
        self.format_selector = QComboBox()
        self.format_selector.hide() 

        self.convert_button = QPushButton("Конвертировать")
        self.convert_button.hide() 
        self.convert_button.clicked.connect(self.run_conversion)

        layout.addWidget(self.info_label)
        layout.addWidget(self.format_selector)
        layout.addWidget(self.convert_button)

    def dragEnterEvent(self, event):
        """Событие, когда файл перетаскивают НАД окном."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        """Событие, когда файл 'бросают' в окно."""
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files:
            
            self.file_path = files[0]
            self.handle_new_file()

    def handle_new_file(self):
        """Обработка нового файла, определение его типа и доступных форматов."""
        if not self.file_path:
            return

        try:
            kind = filetype.guess(self.file_path)
            if kind is None:
                self.show_unknown_file_error()
                return

            file_extension = kind.extension.lower()
            self.info_label.setText(f"Файл: {os.path.basename(self.file_path)}")
            
            
            self.format_selector.clear()
            
            
            if file_extension in ['jpg', 'jpeg', 'png', 'bmp', 'webp']:
                self.format_selector.addItems(['png', 'jpg', 'bmp', 'webp'])
                self.format_selector.show()
                self.convert_button.show()                                                       
            else:
                self.show_unknown_file_error(f"Формат '{file_extension}' пока не поддерживается.")

        except Exception as e:
            self.show_unknown_file_error(f"Произошла ошибка: {e}")

    def run_conversion(self):
        """Запуск процесса конвертации."""
        if not self.file_path:
            return

        target_format = self.format_selector.currentText()
        output_path = self.generate_output_path(target_format)

        try:
            kind = filetype.guess(self.file_path)
            if kind.extension.lower() in ['jpg', 'jpeg', 'png', 'bmp', 'webp']:
                self.convert_image(output_path)
            
            QMessageBox.information(self, "Успех", f"Файл сохранен как:\n{output_path}")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка конвертации", f"Не удалось конвертировать файл.\nОшибка: {e}")
        
        self.reset_ui()

    def convert_image(self, output_path):
        """Конвертирует изображение."""
        with Image.open(self.file_path) as img:
            
            if output_path.lower().endswith('.jpg') and img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            img.save(output_path)

    def generate_output_path(self, target_format):
        """Генерирует путь для сохранения нового файла."""
        directory = os.path.dirname(self.file_path)
        base_name = os.path.splitext(os.path.basename(self.file_path))[0]
        return os.path.join(directory, f"{base_name}_converted.{target_format}")

    def show_unknown_file_error(self, message="Это неизвестный или неподдерживаемый тип файла."):
        """Показывает окно с ошибкой о неизвестном файле."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setText(message)
        msg_box.setInformativeText("Хотите найти информацию об этом формате в интернете?")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.Yes)
        
        ret = msg_box.exec()
        if ret == QMessageBox.StandardButton.Yes:
            search_query = os.path.splitext(os.path.basename(self.file_path))[1] + " file format"
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
            
        self.reset_ui()

    def reset_ui(self):
        """Сброс интерфейса в исходное состояние."""
        self.file_path = None
        self.info_label.setText("Перетащите файл сюда")
        self.format_selector.hide()
        self.convert_button.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_STYLE) 
    
    window = XConvertor()
    window.show()
    
    sys.exit(app.exec())