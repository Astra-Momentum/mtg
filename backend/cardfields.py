'''Actual card fields from the json'''

IMAGES = "image_uris"
FACES = "card_faces"
LAYOUT = "layout"
NAME = "name"
SMALL = "small"
LARGE = "large"
ID = "id"
TYPE = "type_line"
TEXT = "oracle_text"
SET = "set_name"
COLOR = "colors"
RARITY = "rarity"
CMC = "cmc" #converted mana cost
MANA_COST = "mana_cost"
POWER = "power"
TOUGHNESS = "toughness"
COLOR = "colors"
COLOR_IDENTITY = "color_identity"

'''Useful constants'''

KEY = 0
VALUE = 1
FRONT = 0
BACK = 1
CARD = 0
AMOUNT = 1
DOUBLE_CARD_LENGTH = 3
LAST = -1
FIRST = 0

'''Useless card fields'''

KEYS_TO_DELETE = ["object","oracle_id","multiverse_ids","lang","released_at","highres_image","image_status","keywords","mtgo_id","cardmarket_id","legalities","games","reserved",
"foil","nonfoil","finishes","oversized","promo","reprint","variation","rulings_uri","prints_search_uri","digital","card_back_id","artist","artist_ids","illustration_id",
"border_color","frame","full_art","textless","booster","story_spotlight","edhrec_rank","penny_rank","prices","related_uris","mtgo_foil_id","tcgplayer_id","all_parts","security_stamp",
"frame_effects","promo_types","preview","collector_number"]
SUB_FIELDS_TO_TRIM = ["image_uris"]
SUB_KEYS_TO_DELETE = ["art_crop","border_crop","object","artist","artist_id","illustration_id"]