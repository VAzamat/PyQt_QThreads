import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt, QThread, Signal
import queue

from ui_mainwindow import Ui_MainWindow

class ThreadQueue(QThread):
    signalTaskIsDone = Signal(int, int, name="TaskIsDone")
    def __init__(self, id, queue, parent=None):
        super().__init__(parent)
        self.id = id
        self.queue = queue

    def run(self):
        while True:
            task = self.queue.get()
            self.sleep(5)
            self.TaskIsDone.emit(task, self.id)
            self.queue.task_done()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.qpbuttonThreadStart.setText("Delegate tasks")
        self.qpbuttonThreadStop.setText("___")



        self.queue = queue.Queue()
        self.threads = []
        for i in range(1,3):
            thread = ThreadQueue(i,self.queue)
            thread.signalTaskIsDone.connect(self.task_is_done, Qt.QueuedConnection)
            self.statusBar().showMessage(f"Запущен в очереди процесс №{i} ...")
            thread.start()
            self.threads.append( thread )
        self.qpbuttonThreadStart.clicked.connect(self.on_add_task)

    def on_add_task(self):
        for data in range(3):
            self.queue.put(data)
            self.statusBar().showMessage(f"Распределено задание №{data} ...")

    def task_is_done(self,data,id):
        print(f"{data} -- id = {id}")

    def closeEvent(self, event):
        self.hide()
        for thread in self.threads:
            if thread.isRunning():
                thread.exit()
        for thread in self.threads:
            if thread.isRunning():
                thread.wait()
        self.queue.join()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Queue module")
    window.show()
    sys.exit(app.exec())
