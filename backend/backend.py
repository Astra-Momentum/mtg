import re
import ssl
import json as js
from PIL import Image
from io import BytesIO
import os
import os.path as fs
from urllib.request import Request, urlopen
from backend.cardfields import *
from backend.classes import *
from backend.label_dictionnary import *
import random
import datetime

CARDS_CACHE = "Cards"
REGULARS_CACHE = "regulars"
TOKENS_CACHE = "tokens"
DOUBLES_CACHE = "doubles"
DECKS_CACHE = "Decks"
DOUBLE_CARD_NAMES = ["Front", "Back"]
HTTP_HEADERS = {"User-Agent": "Mozilla/5.0"}

CARD_SEPARATOR = "##"
CARD_DATA = []

# region Paths/URLs

EXCEPTIONS_JSON = "./backend/exceptions.json"
CARDS_JSON = "./backend/cards.json"
CARD_BLACKLIST = "./backend/cardblacklist.txt"
SCRYFALL_URL = "https://data.scryfall.io/default-cards/default-cards-20230716211530.json"

# endregion

def init():
    ssl._create_default_https_context = ssl._create_unverified_context
    with open(CARD_BLACKLIST, "r") as blacklist_file: BLACKLIST = blacklist_file.read().splitlines()

    make_dir(f"./{DECKS_CACHE}")
    make_dir(f"./{CARDS_CACHE}")
    make_dir(f"./{CARDS_CACHE}/{TOKENS_CACHE}")
    make_dir(f"./{CARDS_CACHE}/{REGULARS_CACHE}")
    make_dir(f"./{CARDS_CACHE}/{DOUBLES_CACHE}")

    print(LOADING_CARDS)
    if not fs.exists(CARDS_JSON):
        with open(CARDS_JSON, "w") as cards_file:
            js.dump(js.loads(urlopen(Request(SCRYFALL_URL, headers=HTTP_HEADERS)).read()), cards_file, indent=4)

    with open(CARDS_JSON, "r+") as cards_file:
        was_modified = False
        temp_data = js.load(cards_file)
        initial_length = len(temp_data)

        temp_data = list(filter(lambda card: card[ID] not in BLACKLIST, temp_data))
        if initial_length != len(temp_data): was_modified = True

        for card in temp_data:
            for key in KEYS_TO_DELETE:
                if key in card:
                    was_modified = True
                    del card[key]
            for key in SUB_KEYS_TO_DELETE:
                if FACES in card:
                    for face in card[FACES]:
                        if key in face:
                            was_modified = True
                            del face[key]
                for sub in SUB_FIELDS_TO_TRIM:
                    if sub in card:
                        if key in card[sub]:
                            was_modified = True
                            del card[sub][key]
        if was_modified:
            cards_file.seek(0)
            js.dump(temp_data, cards_file, indent=4)
            cards_file.truncate()

    with open(EXCEPTIONS_JSON, "r") as card_exceptions_file:
        temp_data.extend(list(js.load(card_exceptions_file)))

    CARD_DATA.extend(temp_data)
    fetch_card()

def fetch_card():
    for card in CARD_DATA:
        if IMAGES in card: generate_regular_image(card, TOKENS_CACHE if "Token" in card[TYPE] else REGULARS_CACHE)
        elif FACES in card: generate_double_image(card)


def make_dir(path):
    if not fs.exists(path): os.mkdir(path)


def generate_regular_image(card, card_dir: str):
    card_name = normalize(card[NAME])
    make_dir(f"./{CARDS_CACHE}/{card_dir}/{card_name}")
    if not fs.exists(f"./{CARDS_CACHE}/{card_dir}/{card_name}/{card[ID]}.png"):
        try : Image.open(BytesIO(urlopen(Request(card[IMAGES][SMALL], headers=HTTP_HEADERS)).read())).save(f"./{CARDS_CACHE}/{card_dir}/{card_name}/{card[ID]}.png")
        except : print(f"Card {card[NAME]} could not be found.") 


def generate_double_image(card):
    if IMAGES in card[FACES][FRONT] and IMAGES in card[FACES][BACK]:
        card_name = normalize(card[NAME])
        make_dir(f"./{CARDS_CACHE}/{DOUBLES_CACHE}/{card_name}")
        make_dir(f"./{CARDS_CACHE}/{DOUBLES_CACHE}/{card_name}/{card[ID]}")
        for side, face in enumerate(card[FACES]):
            if not fs.exists(f"./{CARDS_CACHE}/{DOUBLES_CACHE}/{card_name}/{card[ID]}/{DOUBLE_CARD_NAMES[side]}.png"):
                try : 
                    Image.open(BytesIO(urlopen(Request(face[IMAGES][SMALL], headers=HTTP_HEADERS)).read())).save(f"./{CARDS_CACHE}/{DOUBLES_CACHE}/{card_name}/{card[ID]}/{DOUBLE_CARD_NAMES[side]}.png")
                except : print(f"Card {card[NAME]} could not be found.") 


def normalize(string): return re.sub('[!@:."_?]', "", f"{string.__str__().replace(' ','')}").replace("//", "&&").replace("A-", "")

# region Deck

def append_deck_file(new_sub_deck: list[dict], deck_name: str, amount: str):
    with open(f"./{DECKS_CACHE}/{deck_name}.txt", "a") as deck_file:
        for card in new_sub_deck: 
            card_back = "" if card["back"] is None else f"{card['back']}{CARD_SEPARATOR}"
            deck_file.write(f"{card['front']}{CARD_SEPARATOR}{card_back}{amount}\n")


def reset_deck_file(deck: list[dict], deck_name: str):
    with open(f"{DECKS_CACHE}/{deck_name}.txt", "w") as deck_file:
        deck_file.truncate(0)
        append_deck_file(deck)


def parse_deck_file(deck: str) -> list[Card]:
    cards = []
    with open(f"./{DECKS_CACHE}/{deck}", "r") as deck_file: cards = [ create_card_from_deck(line) for line in deck_file.read().splitlines() ]
    return cards


def list_decks(): return os.listdir(f"./{DECKS_CACHE}")


def create_deck(file: str) -> Deck:
    name = file.removesuffix(".txt")
    cards = parse_deck_file(file)
    return Deck(name, file, cards)


def create_decks() -> list[Deck]:
    decks = []
    for file in list_decks(): decks.append(create_deck(file))
    return decks


def create_card_from_deck(line: str) -> Card:
    sides = line.split(CARD_SEPARATOR)
    name = ""
    front = sides[FRONT]
    back = sides[BACK] if len(sides) == DOUBLE_CARD_LENGTH else None
    amount = int(sides[LAST])
    selected = False
    return [Card(name, front, back, selected), amount]


def _JSONCard(card_name, front_path, back_path) -> dict:
    return {
        "name": card_name,
        "front": front_path,
        "back": back_path
    }


def playable_deck(deck: Deck):
    cards = []
    for card in deck.cards:
        for i in range(card[AMOUNT]):
            cards.append(card[CARD])
    return Playable_Deck(cards)


def get_deck_size(deck: Deck):
    total = 0
    for card in deck.cards: total += card[AMOUNT]
    return total


def shuffle(bundle):
    shuffled_bundle = []
    while bundle: 
        random_element = random.choice(bundle)
        shuffled_bundle.append(random_element)
        bundle.remove(random_element)
    return shuffled_bundle

# endregion

# region Search

def _get_simples(card_name: str) -> list[dict]:
    root = f"./{CARDS_CACHE}/{REGULARS_CACHE}/{normalize(card_name)}"
    results = []
    if (fs.exists(root)): results = [ _JSONCard(card_name, f"{root}/{id}", None) for id in os.listdir(root) ]
    return results


def _get_doubles(card_name: str) -> list[dict]:
    root = f"./{CARDS_CACHE}/{DOUBLES_CACHE}/{normalize(card_name)}"
    results = []
    if (fs.exists(root)): 
        results = [ _JSONCard(card_name, f"{root}/{id}/{DOUBLE_CARD_NAMES[FRONT]}.png", f"{root}/{id}/{DOUBLE_CARD_NAMES[BACK]}.png") for id in os.listdir(root) ]
    return results


def search_cards_advanced(filters: dict) -> list[dict]:
    compared_keys = filters.keys()
    all_cards = []
    for non_token_card in list(filter(lambda card: TYPE not in card or "Token" not in card[TYPE], CARD_DATA)):
        if all(analyze_card_filter(non_token_card, key, filters[key]) for key in compared_keys):  
            found_cards = _get_simples(non_token_card[NAME]) if IMAGES in non_token_card else _get_doubles(non_token_card[NAME])
            if len(found_cards) > 0 and found_cards[0] not in all_cards:
                all_cards.extend(found_cards)
    return all_cards

            
def analyze_card_filter(card, expected_key: str, expected_value: str):
    if expected_key in card: return expected_value.lower() in (card[expected_key].__str__()).lower()
    if FACES in card: 
        for side in card[FACES]:
            if expected_key in side: return expected_value.lower() in (side[expected_key].__str__()).lower()
    return False

# endregion

def display_large_format(card_path):
    dirs = card_path.split("/")
    id = dirs[LAST].removesuffix(".png")
    if id in DOUBLE_CARD_NAMES:
        side = DOUBLE_CARD_NAMES.index(id)
        id = dirs[LAST - 1]
    for card in CARD_DATA:
        if card[ID] == id:
            if id == dirs[LAST - 1]:
                return Image.open(BytesIO(urlopen(Request(card[FACES][side][IMAGES][LARGE], headers=HTTP_HEADERS)).read())).show()
            return Image.open(BytesIO(urlopen(Request(card[IMAGES][LARGE], headers=HTTP_HEADERS)).read())).show()


def full_card_text(card):
    full_text = card[NAME]
    if FACES in card:
        for face in card[FACES]:
            full_text.join(["" if not TYPE in face else face[TYPE],"" if not TEXT in face else face[TEXT]])
    return full_text.join([card[LAYOUT], "" if not TYPE in card else card[TYPE], "" if not TEXT in card else card[TEXT],
                           "" if not SET in card else card[SET]])




# ajout de function pour bien formater les retours
# a Alex, tu peut modifier l'interieur, mais pas les signatures
# ni les retours

def getDeckList(): 
    file_list = os.listdir(f"./{DECKS_CACHE}")
    return [{"name": name.split('.')[0], "file": name} for name in file_list]

def newDeck():
    name = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    with open(f"./{DECKS_CACHE}/{name}.txt", "a") as deck_file: pass
    return name

def copyDeck(name):
    time = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    with open(f"./{DECKS_CACHE}/{name}.txt", 'rb') as src:
        with open(f"./{DECKS_CACHE}/{name} {time}.txt", 'wb') as dest:
            dest.write(src.read())
    return f"{name} {time}"

def deleteDeck(name):
    os.remove(f"./{DECKS_CACHE}/{name}.txt")

def renameDeck(newName,oldName):
    os.rename(f"./{DECKS_CACHE}/{oldName}.txt", f"./{DECKS_CACHE}/{newName}.txt")


def getCardList(deck: str): 
    cards = []
    with open(f"./{DECKS_CACHE}/{deck}", "r") as file: cards =  [ parse_card(line) for line in file.read().splitlines() ]
    cards = list(filter(lambda x: x is not None, cards))
    return cards

def parse_card(cardString):
    if not cardString : return
    parts = cardString.split(CARD_SEPARATOR)
    card_info = parts[FIRST].split("/")
    card_name = card_info[3]
    card_name = ""
    front_image = "../." + parts[FIRST]
    back_image = None
    amount = parts[LAST]
    if len(parts) == DOUBLE_CARD_LENGTH: back_image = "../." + parts[1]
    return { "name": card_name, "front": front_image, "back": back_image, "selected": False, "amount": amount }