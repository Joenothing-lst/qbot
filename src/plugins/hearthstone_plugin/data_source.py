from typing import Dict, List, Tuple

from hearthstone.deckstrings import Deck
from hearthstone.cardxml import load_dbf, CardXML

format_type = ['未知', '狂野', '标准', '经典']

class HSHandle:
    db: Dict[int, CardXML]

    def __new__(cls):
        if not hasattr(cls, '_instance'):
            instance = object.__new__(cls)
            cls._instance = instance
        else:
            instance = cls._instance
        return instance

    def __init__(self):
        self.db, _ = load_dbf(locale='zhCN')

    def get_deck_from_deckstring(self, deckstring) -> Tuple[List[Tuple[int, str, int]], str, str]:
        deck = Deck.from_deckstring(deckstring)
        return sorted([(self.db[dbf_id].cost, self.db[dbf_id].name, num) for dbf_id, num in deck.cards],
                      key=lambda x: x[0]), self.db[deck.heroes[0]].name, format_type[deck.format]

    def filter(self, **kwargs):
        cards = self.db.values()
        for attr, value in kwargs.items():
            if value is not None:
                if attr == "card_class":
                    cards = [card for card in cards if value in card.classes]
                else:
                    cards = [
                        card for card in cards if
                        (isinstance(value, list) and getattr(card, attr) in value) or getattr(card, attr) == value
                    ]
        return cards
