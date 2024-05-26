from PySide6.QtCore import QObject

# To be used on the @QmlElement decorator
# (QML_IMPORT_MINOR_VERSION is optional)
QML_IMPORT_NAME = "PlayableCard"
QML_IMPORT_MAJOR_VERSION = 1

class Card(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._x = 0
        self._y = 0

    def getX(self):
        return self._x

    def setX(self, x):
        self._x = x

    def getY(self):
        return self._y

    def setY(self, y):
        self._y = y

    x = property(getX, setX)
    y = property(getY, setY)