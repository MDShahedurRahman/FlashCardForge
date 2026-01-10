from __future__ import annotations

from pathlib import Path

from flashcardforge.core.engine import FlashcardEngine
from flashcardforge.storage.json_store import JsonStore
from flashcardforge.storage.csv_io import export_csv, import_csv


MENU = """
FlashCardForge 🧠
-----------------
1) Add card
2) List decks
3) List cards (by deck)
4) Review due cards
5) Stats
6) Export CSV
7) Import CSV
8) Save
9) Quit
"""
