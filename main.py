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

        self.qpbuttonThreadStart.clicked.connect(self.start_thread)
        self.qpbuttonThreadStop.clicked.connect(self.stop_thread)

    def stop_thread(self):
        self.mythread.running = False

    def start_thread(self):
        self.qpbuttonThreadStart.setEnabled(False)
        self.statusBar().showMessage(f"Запущен процесс сканирования...")

        self.mythread = MyThread()
        self.mythread.mysignal.connect(self.update_status, Qt.QueuedConnection)  # Подключаем сигнал обновления интерфейса
        self.mythread.finished.connect(self.finish_thread)  # Подключаем сигнал завершения потока
        self.mythread.start()

    def update_status(self, iteration):
        self.statusBar().showMessage(f"{iteration}. Еще сканирую...")

    def finish_thread(self):
        self.qpbuttonThreadStart.setEnabled(True)
        self.statusBar().showMessage(f"Завершен процесс сканирования")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
