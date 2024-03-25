from PyQt6.QtCore import (
    QObject,
    pyqtSignal,
    pyqtSlot,
    QRunnable
)

class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal()

class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()

        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            self.fn(*self.args, **self.kwargs)
        except:
            self.signals.error.emit()
        else:
            self.signals.finished.emit()
