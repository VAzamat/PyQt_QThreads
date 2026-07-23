import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt, QThread, Signal

from ui_mainwindow import Ui_MainWindow

class MyThread(QThread):
    mysignal = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.running = True

    def run(self):
        for i in range(10):
            if not self.running:
                break
            self.mysignal.emit(i + 1)
            QThread.sleep(5)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
