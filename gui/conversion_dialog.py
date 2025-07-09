from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QComboBox, 
                             QPushButton, QFileDialog, QHBoxLayout, QMessageBox,
                             QListWidget, QAbstractItemView)
from PyQt5.QtCore import Qt
import os
from core.file_utils import get_output_formats, get_file_type
from core.converter import Converter, ConversionError
from core.conversion_history import ConversionHistory

class ConversionDialog(QDialog):
    def __init__(self, filepaths, parent=None):
        super().__init__(parent)
        
        self.filepaths = filepaths
        self.file_type = get_file_type(filepaths[0])
        self.converter = Converter()
        self.history = ConversionHistory()

        self.setWindowTitle("Параметры конвертации")
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout(self)
        
        self.info_label = QLabel(f"Файлов для конвертации: {len(self.filepaths)}")
        self.file_list = QListWidget()
        self.file_list.addItems([os.path.basename(p) for p in self.filepaths])
        self.file_list.setSelectionMode(QAbstractItemView.NoSelection)
        
        format_layout = QHBoxLayout()
        self.format_label = QLabel("Действие / Формат:")
        self.format_combo = QComboBox()
        
        buttons_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Отмена")
        self.convert_button = QPushButton("Конвертировать")
        
        self.setModal(True)
        self.format_combo.addItems(get_output_formats(self.file_type))
        
        self.format_combo.addItems(get_output_formats(self.file_type, self.filepaths[0]))


        layout.addWidget(self.info_label)
        layout.addWidget(self.file_list)
        format_layout.addWidget(self.format_label)
        format_layout.addWidget(self.format_combo)
        layout.addLayout(format_layout)
        layout.addSpacing(20)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.convert_button)
        layout.addLayout(buttons_layout)
        
        self.convert_button.clicked.connect(self.start_conversion)
        self.cancel_button.clicked.connect(self.reject)

    def start_conversion(self):
        selected_action = self.format_combo.currentText()
        
        if len(self.filepaths) > 1 and not any(action in selected_action for action in ['Объединить', 'PDF (из изображений)']):
            self.run_batch_conversion(selected_action)
        else:
            self.run_single_conversion(selected_action)

    def run_single_conversion(self, action):
        output_ext = self.get_extension_from_action(action)
        base_name = os.path.splitext(os.path.basename(self.filepaths[0]))[0]
        output_filename = f"{base_name}.{output_ext}"
        
        output_path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", output_filename)
        
        if not output_path:
            return
            
        try:
            result_path = self.converter.convert(self.filepaths, output_path, action)
            self.history.add_entry(self.filepaths, result_path, "Успех")
            QMessageBox.information(self, "Успех", f"Файл успешно сохранен в:\n{result_path}")
            self.accept()
        except ConversionError as e:
            self.history.add_entry(self.filepaths, output_path, f"Ошибка: {e}")
            QMessageBox.critical(self, "Ошибка конвертации", str(e))

    def run_batch_conversion(self, action):
        output_dir = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения результатов")
        if not output_dir:
            return

        # TODO: Implement a proper progress dialog
        for path in self.filepaths:
            try:
                output_ext = self.get_extension_from_action(action)
                base_name = os.path.splitext(os.path.basename(path))[0]
                output_path = os.path.join(output_dir, f"{base_name}.{output_ext}")
                self.converter.convert([path], output_path, action)
                self.history.add_entry([path], output_path, "Успех")
            except ConversionError as e:
                self.history.add_entry([path], "", f"Ошибка: {e}")
                continue
        
        QMessageBox.information(self, "Успех", f"Пакетная конвертация завершена.\nРезультаты в папке:\n{output_dir}")
        self.accept()

    def get_extension_from_action(self, action):
        if 'аудио' in action:
            return action.split(' ')[0].lower()
        if 'GIF' in action:
            return 'gif'
        if 'OCR' in action:
            return 'txt'
        return action.lower()