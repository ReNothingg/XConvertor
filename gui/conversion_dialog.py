from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QComboBox,
                             QPushButton, QFileDialog, QHBoxLayout, QMessageBox,
                             QListWidget, QAbstractItemView)
import os
from core.file_utils import get_output_formats, get_file_type
from core.converter import Converter, ConversionError
from core.conversion_history import ConversionHistory


PDF_DIRECTORY_ACTIONS = {'JPG', 'PNG', 'Разделить PDF'}


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
        self.available_actions = get_output_formats(self.file_type, self.filepaths[0])

        if self.available_actions:
            self.format_combo.addItems(self.available_actions)
        else:
            self.format_combo.addItem("Нет доступных действий")
            self.format_combo.setEnabled(False)
            self.convert_button.setEnabled(False)


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
        if not self.available_actions:
            return

        selected_action = self.format_combo.currentText()
        
        if len(self.filepaths) > 1 and not any(action in selected_action for action in ['Объединить', 'PDF (из изображений)']):
            self.run_batch_conversion(selected_action)
        else:
            self.run_single_conversion(selected_action)

    def run_single_conversion(self, action):
        output_target = self.select_output_target(action)
        if not output_target:
            return
            
        try:
            result = self.converter.convert(self.filepaths, output_target, action)
            history_output = output_target if isinstance(result, list) else result
            self.history.add_entry(self.filepaths, history_output, "Успех")
            QMessageBox.information(self, "Успех", self.build_success_message(result, output_target))
            self.accept()
        except ConversionError as e:
            self.history.add_entry(self.filepaths, output_target, f"Ошибка: {e}")
            QMessageBox.critical(self, "Ошибка конвертации", str(e))

    def run_batch_conversion(self, action):
        output_dir = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения результатов")
        if not output_dir:
            return

        success_count = 0
        failed_files = []

        for path in self.filepaths:
            try:
                output_target = self.get_batch_output_target(path, output_dir, action)
                result = self.converter.convert([path], output_target, action)
                history_output = output_target if isinstance(result, list) else result
                self.history.add_entry([path], history_output, "Успех")
                success_count += 1
            except ConversionError as e:
                failed_files.append(f"{os.path.basename(path)}: {e}")
                self.history.add_entry([path], "", f"Ошибка: {e}")
        
        message = (
            "Пакетная конвертация завершена.\n"
            f"Успешно: {success_count}\n"
            f"С ошибками: {len(failed_files)}\n"
            f"Результаты в папке:\n{output_dir}"
        )

        if failed_files:
            preview = '\n'.join(failed_files[:3])
            message = f"{message}\n\nПервые ошибки:\n{preview}"
            QMessageBox.warning(self, "Пакетная конвертация завершена", message)
        else:
            QMessageBox.information(self, "Успех", message)
        
        self.accept()

    def is_directory_output_action(self, action):
        return self.file_type == 'pdf' and action in PDF_DIRECTORY_ACTIONS

    def select_output_target(self, action):
        if self.is_directory_output_action(action):
            return QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения результатов")

        output_ext = self.get_extension_from_action(action)
        base_name = self.get_default_base_name(action)
        output_filename = f"{base_name}.{output_ext}"
        output_path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", output_filename)
        return output_path

    def get_default_base_name(self, action):
        if action == 'Объединить PDF':
            return 'merged'
        if action == 'PDF (из изображений)' and len(self.filepaths) > 1:
            return 'images_to_pdf'
        return os.path.splitext(os.path.basename(self.filepaths[0]))[0]

    def get_batch_output_target(self, path, output_dir, action):
        if self.is_directory_output_action(action):
            return output_dir

        output_ext = self.get_extension_from_action(action)
        base_name = os.path.splitext(os.path.basename(path))[0]
        return os.path.join(output_dir, f"{base_name}.{output_ext}")

    def build_success_message(self, result, output_target):
        if isinstance(result, list):
            return f"Создано файлов: {len(result)}\nРезультаты сохранены в:\n{output_target}"
        return f"Файл успешно сохранен в:\n{result}"

    def get_extension_from_action(self, action):
        if action in {'PDF (из изображений)', 'Объединить PDF', 'Разделить PDF'}:
            return 'pdf'
        if 'аудио' in action:
            return action.split(' ')[0].lower()
        if 'GIF' in action:
            return 'gif'
        if 'OCR' in action:
            return 'txt'
        return action.lower()
