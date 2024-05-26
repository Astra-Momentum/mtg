from dataclasses import dataclass
from typing import Optional


@dataclass
class Card:
    """"""
    name: str  # name of the card
    front: str  # front image path of the card
    back: str  # back image path of the card
    selected: bool  # if the user selected the card


@dataclass
class Deck:
    """"""
    name: str
    file: str
    cards: list[Card, int]


@dataclass
class Playable_Deck:
    """"""
    cards: list[Card]
