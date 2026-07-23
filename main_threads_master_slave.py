import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt, QThread, Signal

from ui_mainwindow import Ui_MainWindow

class ThreadMaster(QThread):
    signal = Signal(int)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.count = 0

    def run(self):
        self.exec()

    def on_start(self):
        self.count += 1
        self.signal.emit(self.count)

class ThreadSlave(QThread):
    signal = Signal(int)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.count = 0

    def run(self):
        self.exec()

    def on_change(self, i):
        i += 10
        self.signal.emit(i)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.qpbuttonThreadStart.setText("Start interaction")
        self.qpbuttonThreadStop.setText("___")


        self.statusBar().showMessage(f"Запущены процессы ...")

        self.threadMaster = ThreadMaster()
        self.threadSlave = ThreadSlave()
        self.threadMaster.start()
        self.threadSlave.start()
        self.qpbuttonThreadStart.clicked.connect(self.threadMaster.on_start)
        self.threadMaster.signal.connect(self.threadSlave.on_change)
        self.threadSlave.signal.connect(self.on_slave_update_signal)

    def on_slave_update_signal(self, s):
        self.statusBar().showMessage(f"Текущий номер процесса {s}")

    def closeEvent(self, event):
        if hasattr(self, 'threadMaster') and self.threadMaster.isRunning():
            self.threadMaster.exit()
        if hasattr(self, 'threadSlave') and self.threadSlave.isRunning():
            self.threadSlave.exit()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Взаимодействие между процессам")
    window.show()
    sys.exit(app.exec())
