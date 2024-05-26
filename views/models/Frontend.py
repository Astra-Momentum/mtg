import backend as backend
from backend.classes import *
from PySide6.QtCore import QObject, Signal

class Frontend(QObject):
    someSignal = Signal(str)

    def __init__(self):
        super().__init__()
        self.emitSomeSignal()

    def emitSomeSignal(self):
        # Emits the "someSignal" signal with a message
        self.someSignal.emit("Hello from the Frontend!")

