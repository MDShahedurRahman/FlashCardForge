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


def _prompt(msg: str) -> str:
    return input(msg).strip()


def run() -> None:
    store = JsonStore()
    engine: FlashcardEngine = store.load()

    while True:
        print(MENU)
        choice = _prompt("Choose (1-9): ")

        try:
            if choice == "9":
                store.save(engine)
                print("Saved. Bye!")
                break

            elif choice == "1":
                deck = _prompt("Deck: ")
                front = _prompt("Front: ")
                back = _prompt("Back: ")
                engine.add_card(front, back, deck)
                print("Added.\n")

            elif choice == "2":
                decks = engine.decks()
                if not decks:
                    print("No decks yet.\n")
                else:
                    for d in decks:
                        print(f"- {d}")
                    print()

            elif choice == "3":
                deck = _prompt("Deck (blank=all): ")
                cards = engine.lib.list_cards()
                if deck:
                    cards = [c for c in cards if c.deck.lower() ==
                             deck.lower()]
                if not cards:
                    print("No cards.\n")
                else:
                    for c in cards:
                        print(
                            f"{c.id} | [{c.deck}] due={c.due} reps={c.repetitions} ease={c.ease:.2f}")
                        print(f"  Q: {c.front}")
                        print(f"  A: {c.back}\n")

            elif choice == "4":
                deck = _prompt("Deck (blank=all): ")
                due = engine.due_cards(deck=deck or None, limit=20)
                if not due:
                    print("No due cards. Nice!\n")
                    continue

                print(
                    "\nReview grades: 0..5 (5=easy/perfect, 3=hard but correct, <3=incorrect)\n")
                for c in due:
                    print(f"[{c.deck}] Q: {c.front}")
                    _ = _prompt("Press Enter to show answer...")
                    print(f"A: {c.back}")
                    g_txt = _prompt("Grade (0-5): ")
                    try:
                        g = int(g_txt)
                    except ValueError:
                        print("Invalid grade, skipping.\n")
                        continue
                    engine.review(c.id, g)
                    print(f"Next due: {engine.lib.cards[c.id].due}\n")

                print("Review session complete.\n")

            elif choice == "5":
                deck = _prompt("Deck (blank=all): ")
                s = engine.stats(deck=deck or None)
                print(f"\nTotal cards: {s['total_cards']}")
                print(f"Due today : {s['due_today']}")
                print(f"Decks     : {s['decks']}\n")

            elif choice == "6":
                out = Path(_prompt("CSV output path: ")).expanduser().resolve()
                export_csv(engine, out)
                print(f"Exported to {out}\n")

            elif choice == "7":
                inp = Path(_prompt("CSV input path: ")).expanduser().resolve()
                added = import_csv(engine, inp)
                print(f"Imported {added} card(s).\n")

        except Exception as e:
            print(f"Error: {e}\n")
