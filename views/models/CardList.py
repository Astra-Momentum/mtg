from PySide6.QtCore import (QAbstractListModel, QByteArray, QModelIndex, Qt, Slot, Signal)
from PySide6.QtQml import QmlElement
from PySide6.QtWidgets import QInputDialog
import backend as backend

# To be used on the @QmlElement decorator
# (QML_IMPORT_MINOR_VERSION is optional)
QML_IMPORT_NAME = "CardListModel"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class CardListModel(QAbstractListModel):
    CardsChanged = Signal()
    NameRole = Qt.UserRole + 1
    FrontRole = Qt.UserRole + 2
    BackRole = Qt.UserRole + 3
    AmountRole = Qt.UserRole + 4
    SelectedRole = Qt.UserRole + 5


    def __init__(self, parent=None):
        super().__init__(parent)
        self.cards = []

    def rowCount(self, parent=QModelIndex()):
        return len(self.cards)

    def roleNames(self):
        default = super().roleNames()
        default[self.NameRole] = QByteArray(b"name")
        default[self.FrontRole] = QByteArray(b"front")
        default[self.BackRole] = QByteArray(b"back")
        default[self.AmountRole] = QByteArray(b"amount")
        default[self.SelectedRole] = QByteArray(b"selected")
        return default

    def data(self, index, role: int):
        if not self.cards: return None
        if not index.isValid(): return None
        if role == self.NameRole: return self.cards[index.row()]["name"]
        if role == self.FrontRole: return self.cards[index.row()]["front"]
        if role == self.BackRole: return self.cards[index.row()]["back"]
        if role == self.AmountRole: return self.cards[index.row()]["amount"]
        if role == self.SelectedRole: return self.cards[index.row()]["selected"]
        return None

    def setData(self, index, value, role):
        if role == self.SelectedRole: self.cards[index]["name"] = value
        return True

    @Slot(str)
    def loadCards(self,deck):
        if not deck: return
        cards = backend.getCardList(deck)
        self.addCards(cards,0)
    
    def addCards(self,cards,row):
        self.beginInsertRows(QModelIndex(), row, row + len(cards) - 1)
        for card in cards:
            self.cards.insert(row, card)
            row += 1
        self.endInsertRows()
