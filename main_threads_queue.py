import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt, QThread, Signal
import queue

from ui_mainwindow import Ui_MainWindow

class ThreadQueue(QThread):
    signalTaskIsDone = Signal(str, int, name="TaskIsDone")
    def __init__(self, id, queue, parent=None):
        super().__init__(parent)
        self.id = id
        self.queue = queue
        self.running = True

    def run(self):
        while self.running:
            workingtask = self.queue.get()
            self.sleep(5)
            self.TaskIsDone.emit(workingtask, self.id)
            self.queue.task_done()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.qpbuttonThreadStart.setText("Delegate tasks")
        self.qpbuttonThreadStop.setText("___")

        self.queue = queue.Queue()
        self.threads = []
        for i in [1,2]:
            thread = ThreadQueue(i,self.queue)
            thread.signalTaskIsDone.connect(self.task_is_done, Qt.QueuedConnection)
            self.statusBar().showMessage(f"Запущен в очереди поток вычислений №{i} ...")
            thread.start()
            self.threads.append( thread )
        self.qpbuttonThreadStart.clicked.connect(self.on_add_task)

    def on_add_task(self):
        for data in ["r500t6500logg4.5vinf6.4", "r400t8500logg4.5vinf3.4", "r450t9500logg5.5vinf4.6", "r350t4500logg5.5vinf5.4", "r500t1500logg3.5vinf2.6" ]:
            self.queue.put(data)
            self.statusBar().showMessage(f"Распределено задание №{data} ...")

    def task_is_done(self,data,id):
        print(f"Окончание задания {data} -- id = {id}")

    def closeEvent(self, event):
        self.hide()
        for thread in self.threads:
            if thread.isRunning():
                thread.running = False
        for thread in self.threads:
            if thread.isRunning():
                thread.wait(5000)
        self.queue.join()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Queue module")
    window.show()
    sys.exit(app.exec())
