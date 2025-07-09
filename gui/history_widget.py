from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, 
                             QPushButton, QHeaderView, QHBoxLayout)
from PyQt5.QtCore import Qt
from core.conversion_history import ConversionHistory

class HistoryView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.history_manager = ConversionHistory()
        
        layout = QVBoxLayout(self)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Дата", "Источник", "Результат", "Статус"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        buttons_layout = QHBoxLayout()
        self.clear_button = QPushButton("Очистить историю")
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.clear_button)
        
        layout.addWidget(self.table)
        layout.addLayout(buttons_layout)
        
        self.clear_button.clicked.connect(self.clear_history)
        
        self.load_history()

    def load_history(self):
        history_data = self.history_manager.get_history()
        self.table.setRowCount(len(history_data))
        
        for row, item in enumerate(history_data):
            sources = ", ".join(item.get("sources", []))
            
            self.table.setItem(row, 0, QTableWidgetItem(item.get("timestamp", "")))
            self.table.setItem(row, 1, QTableWidgetItem(sources))
            self.table.setItem(row, 2, QTableWidgetItem(item.get("output", "")))
            
            status_item = QTableWidgetItem(item.get("status", ""))
            if "Ошибка" in item.get("status", ""):
                status_item.setForeground(Qt.red)
            else:
                status_item.setForeground(Qt.green)
            self.table.setItem(row, 3, status_item)

    def clear_history(self):
        # Placeholder for clearing history logic
        pass
    