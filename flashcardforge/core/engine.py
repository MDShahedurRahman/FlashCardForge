from __future__ import annotations

from datetime import date
from typing import Dict, List, Optional, Tuple

from .models import Card, Library, today_iso
from .scheduler import Grade, update_card


def is_due(card: Card, on_day: str) -> bool:
    return card.due <= on_day


class FlashcardEngine:
    """
    Core operations: add/edit/delete cards, choose due cards, apply reviews.
    """

    def __init__(self, library: Optional[Library] = None) -> None:
        self.lib = library or Library()

    def add_card(self, front: str, back: str, deck: str) -> Card:
        card = Card.new(front=front, back=back, deck=deck)
        self.lib.cards[card.id] = card
        return card

    def delete_card(self, card_id: str) -> bool:
        return self.lib.cards.pop(card_id, None) is not None
