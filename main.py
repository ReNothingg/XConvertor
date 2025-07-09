import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from gui.main_window import MainWindow

def set_taskbar_icon():
    if sys.platform == 'win32':
        import ctypes
        myappid = 'mycompany.xconvertor.1.0' 
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("assets/icons/logo.png"))
    set_taskbar_icon()
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()