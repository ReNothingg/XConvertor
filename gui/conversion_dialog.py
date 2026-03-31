from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QComboBox,
                             QPushButton, QFileDialog, QHBoxLayout, QMessageBox,
                             QListWidget, QAbstractItemView, QProgressDialog)
from PyQt5.QtCore import QObject, QThread, pyqtSignal, Qt
import os
from core.file_utils import get_output_formats, get_file_type
from core.converter import Converter, ConversionError
from core.conversion_history import ConversionHistory


PDF_DIRECTORY_ACTIONS = {'JPG', 'PNG', 'Разделить PDF'}


class BatchConversionWorker(QObject):
    item_started = pyqtSignal(int, int, str)
    item_succeeded = pyqtSignal(str, object)
    item_failed = pyqtSignal(str, str)
    item_finished = pyqtSignal(int)
    finished = pyqtSignal(int, list, bool)

    def __init__(self, filepaths, output_dir, action, parent=None):
        super().__init__(parent)
        self.filepaths = filepaths
        self.output_dir = output_dir
        self.action = action
        self.converter = Converter()
        self._cancel_requested = False

    def request_cancel(self):
        self._cancel_requested = True

    def _is_directory_output_action(self, action, filepath):
        return get_file_type(filepath) == 'pdf' and action in PDF_DIRECTORY_ACTIONS

    def _get_output_target(self, filepath):
        if self._is_directory_output_action(self.action, filepath):
            return self.output_dir

        output_ext = ConversionDialog.get_extension_from_action(self.action)
        base_name = os.path.splitext(os.path.basename(filepath))[0]
        return os.path.join(self.output_dir, f"{base_name}.{output_ext}")

    def run(self):
        success_count = 0
        failed_files = []
        total_files = len(self.filepaths)

        for index, path in enumerate(self.filepaths, start=1):
            if self._cancel_requested:
                break

            self.item_started.emit(index, total_files, path)

            try:
                output_target = self._get_output_target(path)
                result = self.converter.convert([path], output_target, self.action)
                self.item_succeeded.emit(path, result if isinstance(result, list) else output_target)
                success_count += 1
            except ConversionError as e:
                failed_files.append((path, str(e)))
                self.item_failed.emit(path, str(e))

            self.item_finished.emit(index)

        self.finished.emit(success_count, failed_files, self._cancel_requested)


class ConversionDialog(QDialog):
    def __init__(self, filepaths, parent=None):
        super().__init__(parent)
        
        self.filepaths = filepaths
        self.file_type = get_file_type(filepaths[0])
        self.converter = Converter()
        self.history = ConversionHistory()
        self.batch_thread = None
        self.batch_worker = None
        self.progress_dialog = None
        self.batch_cancel_requested = False

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

    def reject(self):
        if self.batch_worker is not None:
            self.cancel_batch_conversion()
            return

        super().reject()

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
            history_output = result
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

        self.batch_cancel_requested = False
        self.progress_dialog = QProgressDialog("Подготовка пакетной конвертации...", "Остановить", 0, len(self.filepaths), self)
        self.progress_dialog.setWindowTitle("Пакетная конвертация")
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setAutoClose(False)
        self.progress_dialog.setAutoReset(False)
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.setValue(0)

        self.set_controls_enabled(False)

        self.batch_thread = QThread(self)
        self.batch_worker = BatchConversionWorker(self.filepaths, output_dir, action)
        self.batch_worker.moveToThread(self.batch_thread)

        self.batch_thread.started.connect(self.batch_worker.run)
        self.batch_worker.item_started.connect(self.on_batch_item_started)
        self.batch_worker.item_succeeded.connect(self.on_batch_item_succeeded)
        self.batch_worker.item_failed.connect(self.on_batch_item_failed)
        self.batch_worker.item_finished.connect(self.on_batch_item_finished)
        self.batch_worker.finished.connect(self.on_batch_finished)
        self.batch_worker.finished.connect(self.batch_thread.quit)
        self.batch_worker.finished.connect(self.batch_worker.deleteLater)
        self.batch_thread.finished.connect(self.batch_thread.deleteLater)
        self.progress_dialog.canceled.connect(self.cancel_batch_conversion)

        self.batch_thread.start()

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

    def set_controls_enabled(self, enabled):
        self.format_combo.setEnabled(enabled)
        self.convert_button.setEnabled(enabled)
        self.cancel_button.setEnabled(enabled)

    def cancel_batch_conversion(self):
        if self.batch_worker is None or self.batch_cancel_requested:
            return

        self.batch_cancel_requested = True
        self.progress_dialog.setLabelText("Остановка после завершения текущего файла...")
        self.progress_dialog.setCancelButtonText("Ожидание...")
        cancel_button = self.progress_dialog.findChild(QPushButton)
        if cancel_button is not None:
            cancel_button.setEnabled(False)
        self.batch_worker.request_cancel()

    def on_batch_item_started(self, index, total, path):
        if self.progress_dialog is None:
            return

        self.progress_dialog.setMaximum(total)
        self.progress_dialog.setLabelText(
            f"Обработка файла {index} из {total}:\n{os.path.basename(path)}"
        )

    def on_batch_item_succeeded(self, source_path, output_result):
        self.history.add_entry([source_path], output_result, "Успех")

    def on_batch_item_failed(self, source_path, error_message):
        self.history.add_entry([source_path], "", f"Ошибка: {error_message}")

    def on_batch_item_finished(self, value):
        if self.progress_dialog is not None:
            self.progress_dialog.setValue(value)

    def on_batch_finished(self, success_count, failed_files, cancelled):
        processed_count = success_count + len(failed_files)
        skipped_count = max(0, len(self.filepaths) - processed_count)

        if self.batch_thread is not None:
            self.batch_thread.quit()
            self.batch_thread.wait()

        if self.progress_dialog is not None:
            self.progress_dialog.setValue(processed_count)
            self.progress_dialog.close()
            self.progress_dialog = None

        self.set_controls_enabled(True)

        self.batch_thread = None
        self.batch_worker = None

        message = (
            f"Обработано: {processed_count} из {len(self.filepaths)}\n"
            f"Успешно: {success_count}\n"
            f"С ошибками: {len(failed_files)}"
        )

        if skipped_count:
            message = f"{message}\nПропущено после остановки: {skipped_count}"

        if failed_files:
            preview = '\n'.join(
                f"{os.path.basename(path)}: {error}" for path, error in failed_files[:3]
            )
            message = f"{message}\n\nПервые ошибки:\n{preview}"

        if cancelled:
            QMessageBox.warning(self, "Конвертация остановлена", message)
        elif failed_files:
            QMessageBox.warning(self, "Пакетная конвертация завершена", message)
        else:
            QMessageBox.information(self, "Успех", message)

        self.accept()

    @staticmethod
    def get_extension_from_action(action):
        if action in {'PDF (из изображений)', 'Объединить PDF', 'Разделить PDF'}:
            return 'pdf'
        if 'аудио' in action:
            return action.split(' ')[0].lower()
        if 'GIF' in action:
            return 'gif'
        if 'OCR' in action:
            return 'txt'
        return action.lower()
