from PySide6.QtCore import (QAbstractListModel, QByteArray, QModelIndex, Qt, Slot, Signal)
from PySide6.QtQml import QmlElement
from PySide6.QtWidgets import QInputDialog

import backend as backend

# To be used on the @QmlElement decorator
# (QML_IMPORT_MINOR_VERSION is optional)
QML_IMPORT_NAME = "DeckListModel"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class DeckListModel(QAbstractListModel):
    decksChanged = Signal()
    NameRole = Qt.UserRole + 1
    FileRole = Qt.UserRole + 2

    def __init__(self, parent=None):
        super().__init__(parent)
        self.decks = backend.getDeckList()

    def rowCount(self, parent=QModelIndex()):
        return len(self.decks)

    def roleNames(self):
        default = super().roleNames()
        default[self.NameRole] = QByteArray(b"name")
        default[self.FileRole] = QByteArray(b"file")
        return default

    def data(self, index, role: int):
        if not self.decks: return None
        if not index.isValid(): return None
        if role == self.NameRole: return self.decks[index.row()]["name"]
        if role == self.FileRole: return self.decks[index.row()]["file"]
        return None

    def setData(self, index, value, role):
        if role == self.NameRole: self.decks[index]["name"] = value
        return True

    @Slot(str,int)
    def renameDeck(self,newName,row):
        if(any(item.get('name') == newName for item in self.decks)): return False
        backend.renameDeck(newName,self.decks[row]["name"])
        self.removeDeck(row)
        self.addDeck(newName,row)
        return True

    @Slot(int)
    def deleteDeck(self,row):
        backend.deleteDeck(self.decks[row]["name"])
        self.removeDeck(row)

    @Slot()
    def newDeck(self):
        name = backend.newDeck()
        self.addDeck(name, 0)

    @Slot(int)
    def copyDeck(self,row):
        name = backend.copyDeck(self.decks[row]["name"])
        self.addDeck(name, 0)

    def addDeck(self,name,row):
        self.beginInsertRows(QModelIndex(), row, row)
        self.decks.insert(row, {"name": name,"file":name+".txt"})
        self.endInsertRows()

    def removeDeck(self,row):
        self.beginRemoveRows(QModelIndex(), row, row )
        self.decks.remove(self.decks[row])
        self.endRemoveRows()
