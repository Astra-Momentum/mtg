from PySide6.QtCore import (QObject, Slot, Signal, Property)
from PySide6.QtQml import QmlElement
from PySide6.QtWidgets import QInputDialog
import backend as backend
from backend.cardfields import *

# To be used on the @QmlElement decorator
# (QML_IMPORT_MINOR_VERSION is optional)
QML_IMPORT_NAME = "SearchModel"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class SearchModel(QObject):
    paramsChanged = Signal()
    deckChanged = Signal()
    resultsChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init()
    
    def init(self):
        self._params = [
        {"param":NAME,"label":"NAME","type":"text","options":""},
        {"param":TYPE,"label":"TYPE","type":"text","options":""},
        {"param":TEXT,"label":"TEXT","type":"text","options":""},
        {"param":SET,"label":"SET","type":"combo","options":""},
        {"param":COLOR,"label":"COLOR","type":"radio","options":""},
        {"param":RARITY,"label":"RARITY","type":"combo","options":""},
        {"param":CMC,"label":"CMC","type":"number","options":""},
        {"param":MANA_COST,"label":"MANA_COST","type":"number","options":""},
        {"param":POWER,"label":"POWER","type":"number","options":""},
        {"param":TOUGHNESS,"label":"TOUGHNESS","type":"number","options":""},
        {"param":COLOR,"label":"COLOR","type":"radio","options":""},
        {"param":COLOR_IDENTITY,"label":"COLOR_IDENTITY","type":"radio","options":""},
        {"param":"deck","label":"DECK","type":"combo","options":""},
        {"param":"amount","label":"amount","type":"number","options":""},
        ]
        self._results = []

    @Property(list, notify=paramsChanged)
    def params(self):
        return self._params
    @Property(list, notify=deckChanged)
    def deck(self):
        return self._deck
    @Property(list, notify=resultsChanged)
    def results(self):
        return self._results
    
    @params.setter
    def params(self, value):
        self._params = value
        self.paramsChanged.emit()
    @deck.setter
    def deck(self, value):
        self._deck = value
        self.deckChanged.emit()
    @results.setter
    def results(self, value):
        self._results = value
        self.resultsChanged.emit()

    @Slot()
    def reset(self):
        self.init()
    
    @Slot(dict)
    def search(self,params):
        if all(value == "" for value in params.values()): return
        self._results = backend.search_cards_advanced(params)
        print(self._results)
        self.resultsChanged.emit()
   
    @Slot(str,list,str)
    def save(self,deck,selected_cards,amount):
        if not deck : deck = backend.newDeck()
        # backend.append_deck_file(deck,selected_cards)
        print("save")
        print(deck)
        print(selected_cards)
        amount = amount if amount else 1
        backend.append_deck_file(selected_cards,deck,amount)
        