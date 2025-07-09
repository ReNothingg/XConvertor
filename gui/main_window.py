from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, QMessageBox,
                             QStackedWidget, QHBoxLayout, QPushButton)
from PyQt5.QtCore import Qt, QTimer
from core.file_utils import get_file_type
from .conversion_dialog import ConversionDialog
from .history_view import HistoryView
from .youtube_dialog import YouTubeDialog
import os
import webbrowser
from urllib.parse import quote
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("XConvertor")
        self.setGeometry(200, 200, 800, 600)
        self.setAcceptDrops(True)

        try:
            with open("assets/styles/dark_theme.qss", "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("WARNING: Stylesheet not found.")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        self.stack = QStackedWidget()
        
        self.drop_widget = QWidget()
        drop_layout = QVBoxLayout(self.drop_widget)
        self.drop_area = QLabel("\n\nПеретащите файлы сюда\n\n")
        self.drop_area.setAlignment(Qt.AlignCenter)
        self.drop_area.setObjectName("DropArea")
        drop_layout.addWidget(self.drop_area)
        
        self.history_widget = HistoryView()
        
        self.stack.addWidget(self.drop_widget)
        self.stack.addWidget(self.history_widget)
        
        nav_layout = QHBoxLayout()
        self.home_button = QPushButton("Конвертер")
        self.history_button = QPushButton("История")
        self.youtube_button = QPushButton("YouTube") # Новая кнопка

        nav_layout.addWidget(self.home_button)
        nav_layout.addWidget(self.history_button)
        nav_layout.addWidget(self.youtube_button) # Добавляем на панель
        nav_layout.addStretch()
        
        main_layout.addLayout(nav_layout)
        main_layout.addWidget(self.stack)
        
        self.home_button.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.history_button.clicked.connect(self.show_history)
        self.youtube_button.clicked.connect(self.open_youtube_downloader) # Подключаем сигнал


        if len(sys.argv) > 1:
            QTimer.singleShot(100, lambda: self.process_dropped_files([sys.argv[1]]))

    def show_history(self):
        self.history_widget.load_history()
        self.stack.setCurrentIndex(1)

    def open_youtube_downloader(self):
        dialog = YouTubeDialog(self)
        dialog.exec_()


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
        filepaths = [u.toLocalFile() for u in event.mimeData().urls()]
        self.process_dropped_files(filepaths)

    def process_dropped_files(self, filepaths):
        valid_files = [p for p in filepaths if os.path.isfile(p)]
        
        if not valid_files:
            QMessageBox.warning(self, "Ошибка", "Можно обрабатывать только файлы.")
            return

        first_file_type = get_file_type(valid_files[0])
        
        if first_file_type == 'unknown':
            self.handle_unknown_file(valid_files[0])
            return
            
        for path in valid_files[1:]:
            if get_file_type(path) != first_file_type:
                QMessageBox.warning(self, "Ошибка", "Все файлы в пакете должны быть одного типа (например, только изображения).")
                return
        
        dialog = ConversionDialog(valid_files, self)
        dialog.exec_()

    def handle_unknown_file(self, filepath):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Неизвестный файл")
        msg_box.setText(f"Формат файла '{os.path.basename(filepath)}' не поддерживается.")
        msg_box.setInformativeText("Хотите найти информацию о конвертации этого формата в интернете?")
        
        search_button = msg_box.addButton("Найти в интернете", QMessageBox.ActionRole)
        msg_box.addButton("Отмена", QMessageBox.RejectRole)
        
        msg_box.exec_()
        
        if msg_box.clickedButton() == search_button:
            query = f"how to convert {os.path.splitext(filepath)[1]} file"
            url = f"https://www.google.com/search?q={quote(query)}"
            webbrowser.open(url)