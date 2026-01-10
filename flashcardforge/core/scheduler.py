from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

from .models import Card


@dataclass(frozen=True)
class Grade:
    """
    0..5 grading like SM-2:
    5 = perfect response
    4 = correct with hesitation
    3 = correct but difficult
    2 = incorrect; remembered after seeing answer
    1 = incorrect; familiar
    0 = complete blackout
    """
    value: int


def _parse(d: str) -> date:
    return date.fromisoformat(d)


def _iso(d: date) -> str:
    return d.isoformat()


def update_card(card: Card, grade: Grade, today: str) -> Card:
    """
    SM-2 inspired scheduling:
    - If grade < 3: repetitions reset, interval set to 1, due tomorrow.
    - Else: repetitions++, interval grows, ease updated.
    """
    g = grade.value
    if g < 0 or g > 5:
        raise ValueError("grade must be 0..5")

    t = _parse(today)

    ease = card.ease + (0.1 - (5 - g) * (0.08 + (5 - g) * 0.02))
    if ease < 1.3:
        ease = 1.3

    if g < 3:
        repetitions = 0
        interval = 1
        due = t + timedelta(days=1)
    else:
        repetitions = card.repetitions + 1
        if repetitions == 1:
            interval = 1
        elif repetitions == 2:
            interval = 6
        else:
            interval = int(round(card.interval * ease))
            if interval < 1:
                interval = 1
        due = t + timedelta(days=interval)

    # mutate safely by returning a new Card-like state (but Card is mutable; we update in place)
    card.ease = float(ease)
    card.repetitions = int(repetitions)
    card.interval = int(interval)
    card.due = _iso(due)
    return card
