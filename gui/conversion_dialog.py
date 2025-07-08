from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QComboBox, 
                             QPushButton, QFileDialog, QHBoxLayout, QMessageBox)
from PyQt5.QtCore import Qt
import os
from core.file_utils import get_output_formats
from core.converter import Converter, ConversionError

class ConversionDialog(QDialog):
    def __init__(self, filepath, file_type, parent=None):
        super().__init__(parent)
        
        self.filepath = filepath
        self.file_type = file_type
        self.converter = Converter()

        self.setWindowTitle("Параметры конвертации")
        self.setMinimumWidth(400)
        
        # --- Создание виджетов ---
        layout = QVBoxLayout(self)
        
        self.info_label = QLabel(f"Файл: {os.path.basename(self.filepath)}")
        
        format_layout = QHBoxLayout()
        self.format_label = QLabel("Конвертировать в:")
        self.format_combo = QComboBox()
        
        self.convert_button = QPushButton("Конвертировать")
        
        # --- Настройка виджетов ---
        self.setModal(True)
        self.format_combo.addItems(get_output_formats(self.file_type))
        
        # --- Сборка макета ---
        layout.addWidget(self.info_label)
        format_layout.addWidget(self.format_label)
        format_layout.addWidget(self.format_combo)
        layout.addLayout(format_layout)
        layout.addSpacing(20)
        layout.addWidget(self.convert_button, alignment=Qt.AlignRight)
        
        # --- Подключение сигналов ---
        self.convert_button.clicked.connect(self.start_conversion)

    def start_conversion(self):
        selected_format_text = self.format_combo.currentText()
        
        if "(только аудио)" in selected_format_text:
            selected_format = selected_format_text.replace("(только аудио)", "").strip().lower()
        else:
            selected_format = selected_format_text.lower()
        
        base_name = os.path.splitext(os.path.basename(self.filepath))[0]
        output_filename = f"{base_name}.{selected_format}"
        
        output_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Сохранить файл", 
            output_filename,
            f"{selected_format.upper()} Files (*.{selected_format});;All Files (*)"
        )
        
        if not output_path:
            return
            
        try:
            self.converter.convert(self.filepath, output_path, self.file_type)
            QMessageBox.information(self, "Успех", f"Файл успешно сохранен в:\n{output_path}")
            self.accept()
        except ConversionError as e:
            QMessageBox.critical(self, "Ошибка конвертации", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Неизвестная ошибка", f"Произошла непредвиденная ошибка: {e}")