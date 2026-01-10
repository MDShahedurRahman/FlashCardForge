from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List, Optional
from uuid import uuid4


def today_iso() -> str:
    return date.today().isoformat()


@dataclass
class Card:
    id: str
    front: str
    back: str
    deck: str

    # spaced repetition fields (SM-2 style)
    due: str = field(default_factory=today_iso)        # YYYY-MM-DD
    interval: int = 0                                 # days
    repetitions: int = 0
    ease: float = 2.5                                 # SM-2 default

    created_on: str = field(default_factory=today_iso)

    @staticmethod
    def new(front: str, back: str, deck: str) -> "Card":
        front = (front or "").strip()
        back = (back or "").strip()
        deck = (deck or "").strip()
        if not front:
            raise ValueError("Front cannot be empty.")
        if not back:
            raise ValueError("Back cannot be empty.")
        if not deck:
            raise ValueError("Deck cannot be empty.")
        return Card(
            id=str(uuid4()),
            front=front,
            back=back,
            deck=deck,
        )


@dataclass
class Library:
    cards: Dict[str, Card] = field(default_factory=dict)

    def list_cards(self) -> List[Card]:
        return sorted(self.cards.values(), key=lambda c: (c.deck.lower(), c.due, c.created_on, c.id))
