from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QComboBox, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import requests
from io import BytesIO

class YouTubeDialog(QDialog):
    def __init__(self, converter, history, parent=None):
        super().__init__(parent)
        self.converter = converter
        self.history = history
        self.setWindowTitle("Скачать с YouTube")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        
        url_layout = QHBoxLayout()
        url_label = QLabel("URL видео:")
        self.url_input = QLineEdit()
        self.check_button = QPushButton("Проверить")
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(self.check_button)
        
        
        self.info_layout = QVBoxLayout()
        self.thumbnail_label = QLabel()
        self.thumbnail_label.setFixedSize(320, 180)
        self.thumbnail_label.setAlignment(Qt.AlignCenter)
        self.title_label = QLabel()
        self.author_label = QLabel()
        self.info_layout.addWidget(self.thumbnail_label)
        self.info_layout.addWidget(self.title_label)
        self.info_layout.addWidget(self.author_label)
        self.info_layout.setAlignment(Qt.AlignCenter)
        
        
        format_layout = QHBoxLayout()
        format_label = QLabel("Формат:")
        self.format_combo = QComboBox()
        self.format_combo.addItems(['MP4 видео', 'MP3 аудио'])
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_combo)
        
        
        self.download_button = QPushButton("Скачать")
        self.download_button.setEnabled(False)
        
        
        layout.addLayout(url_layout)
        layout.addLayout(self.info_layout)
        layout.addLayout(format_layout)
        layout.addWidget(self.download_button)
        
        self.setLayout(layout)
        
        
        self.check_button.clicked.connect(self.check_video)
        self.download_button.clicked.connect(self.start_download)
        
    def check_video(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Ошибка", "Введите URL видео")
            return
            
        try:
            info = self.converter.youtube_downloader.get_video_info(url)
            
            response = requests.get(info['thumbnail_url'])
            thumbnail = QPixmap()
            thumbnail.loadFromData(BytesIO(response.content).read())
            self.thumbnail_label.setPixmap(thumbnail.scaled(320, 180, Qt.KeepAspectRatio))
            
            self.title_label.setText(f"Название: {info['title']}")
            self.author_label.setText(f"Автор: {info['author']}")
            
            self.download_button.setEnabled(True)
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
            self.download_button.setEnabled(False)
    
    def start_download(self):
        url = self.url_input.text().strip()
        format = 'mp3' if self.format_combo.currentText() == 'MP3 аудио' else 'mp4'
        ext = 'mp3' if format == 'mp3' else 'mp4'
        
        try:
            from PyQt5.QtWidgets import QFileDialog
            output_path, _ = QFileDialog.getSaveFileName(
                self,
                "Сохранить файл",
                f"youtube_video.{ext}",
                f"{'Audio' if format == 'mp3' else 'Video'} Files (*.{ext})"
            )
            
            if not output_path:
                return
                
            result_path = self.converter.convert([url], output_path, self.format_combo.currentText())
            self.history.add_entry([url], result_path, "Успех")
            QMessageBox.information(self, "Успех", f"Файл успешно сохранен в:\n{result_path}")
            self.accept()
            
        except Exception as e:
            self.history.add_entry([url], "", f"Ошибка: {e}")
            QMessageBox.critical(self, "Ошибка загрузки", str(e))