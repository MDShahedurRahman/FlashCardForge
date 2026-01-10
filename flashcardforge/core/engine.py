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

    def edit_card(self, card_id: str, front: Optional[str] = None, back: Optional[str] = None, deck: Optional[str] = None) -> Card:
        card = self.lib.cards.get(card_id)
        if card is None:
            raise KeyError("Card not found.")

        if front is not None:
            f = front.strip()
            if not f:
                raise ValueError("Front cannot be empty.")
            card.front = f
        if back is not None:
            b = back.strip()
            if not b:
                raise ValueError("Back cannot be empty.")
            card.back = b
        if deck is not None:
            d = deck.strip()
            if not d:
                raise ValueError("Deck cannot be empty.")
            card.deck = d
        return card

    def decks(self) -> List[str]:
        names = sorted({c.deck for c in self.lib.cards.values()},
                       key=lambda s: s.lower())
        return names

    def due_cards(self, deck: Optional[str] = None, on_day: Optional[str] = None, limit: int = 20) -> List[Card]:
        if limit <= 0:
            raise ValueError("limit must be > 0")
        day = on_day or today_iso()
        out = []
        for c in self.lib.cards.values():
            if deck and c.deck.lower() != deck.lower():
                continue
            if is_due(c, day):
                out.append(c)
        out.sort(key=lambda c: (c.due, c.created_on, c.id))
        return out[:limit]

    def review(self, card_id: str, grade: int, today: Optional[str] = None) -> Card:
        card = self.lib.cards.get(card_id)
        if card is None:
            raise KeyError("Card not found.")
        day = today or today_iso()
        return update_card(card, Grade(grade), day)

    def stats(self, deck: Optional[str] = None, on_day: Optional[str] = None) -> Dict:
        day = on_day or today_iso()
        cards = [c for c in self.lib.cards.values() if (
            not deck or c.deck.lower() == deck.lower())]
        due = [c for c in cards if is_due(c, day)]
        return {
            "total_cards": len(cards),
            "due_today": len(due),
            "decks": len({c.deck for c in self.lib.cards.values()}),
        }
