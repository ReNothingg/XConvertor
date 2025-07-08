import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    # Создаем экземпляр QApplication
    app = QApplication(sys.argv)

    # Создаем главное окно
    window = MainWindow()
    
    # Показываем окно
    window.show()
    
    # Запускаем главный цикл приложения
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()