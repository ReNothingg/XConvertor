from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, 
                             QTableWidget, QHeaderView, QAbstractItemView, QProgressBar, 
                             QLabel, QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from core.youtube_downloader import YouTubeDownloader, DownloadWorker

class YouTubeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Загрузчик с YouTube")
        self.setMinimumSize(700, 500)
        
        self.downloader = YouTubeDownloader()
        self.streams = []

        
        main_layout = QVBoxLayout(self)
        url_layout = QHBoxLayout()
        
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Вставьте ссылку на YouTube видео сюда...")
        
        self.fetch_button = QPushButton("Получить информацию")
        
        self.streams_table = QTableWidget()
        self.streams_table.setColumnCount(5)
        self.streams_table.setHorizontalHeaderLabels(["Тип", "Разрешение", "Формат", "Размер", "Аудио"])
        self.streams_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.streams_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.streams_table.setSelectionMode(QAbstractItemView.SingleSelection)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        self.status_label = QLabel("")
        self.download_button = QPushButton("Скачать выбранное")
    
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(self.fetch_button)
        
        main_layout.addLayout(url_layout)
        main_layout.addWidget(self.streams_table)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.download_button, alignment=Qt.AlignRight)
        
        self.fetch_button.clicked.connect(self.fetch_streams)
        self.download_button.clicked.connect(self.download_stream)

    def fetch_streams(self):
        url = self.url_input.text()
        if not url:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, вставьте ссылку.")
            return
            
        try:
            self.status_label.setText("Получение информации о видео...")
            self.streams = self.downloader.get_streams(url)
            self.populate_table()
            self.status_label.setText(f"Видео найдено: {self.downloader.get_title(url)}")
        except Exception as e:
            self.status_label.setText("")
            QMessageBox.critical(self, "Ошибка", f"Не удалось получить информацию о видео:\n{e}")

    def populate_table(self):
        self.streams_table.setRowCount(0)
        for stream in self.streams:
            row_position = self.streams_table.rowCount()
            self.streams_table.insertRow(row_position)
            
            stream_type = "Видео" if stream.is_progressive or stream.type == "video" else "Аудио"
            resolution = stream.resolution if stream.resolution else f"{stream.abr}"
            file_ext = stream.mime_type.split('/')[1]
            file_size = f"{stream.filesize / 1024 / 1024:.2f} MB"
            audio_info = "Да" if stream.is_progressive or stream.type == "audio" else "Нет"
            
            self.streams_table.setItem(row_position, 0, self.create_item(stream_type))
            self.streams_table.setItem(row_position, 1, self.create_item(resolution))
            self.streams_table.setItem(row_position, 2, self.create_item(file_ext))
            self.streams_table.setItem(row_position, 3, self.create_item(file_size))
            self.streams_table.setItem(row_position, 4, self.create_item(audio_info))

    def create_item(self, text):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        return item

    def download_stream(self):
        selected_rows = self.streams_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите поток для скачивания.")
            return
            
        selected_index = selected_rows[0].row()
        stream_to_download = self.streams[selected_index]
        
        default_filename = self.downloader.get_default_filename(stream_to_download)
        output_path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", default_filename)
        
        if not output_path:
            return
            
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        self.download_button.setEnabled(False)
        
        self.thread = QThread()
        self.worker = DownloadWorker(stream_to_download, output_path)
        self.worker.moveToThread(self.thread)
        
        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.on_download_finished)
        self.worker.error.connect(self.on_download_error)
        
        self.thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def on_download_finished(self, path):
        self.thread.quit()
        self.thread.wait()
        self.download_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        QMessageBox.information(self, "Успех", f"Файл успешно скачан:\n{path}")

    def on_download_error(self, error_message):
        self.thread.quit()
        self.thread.wait()
        self.download_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        QMessageBox.critical(self, "Ошибка загрузки", error_message)