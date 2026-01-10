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
