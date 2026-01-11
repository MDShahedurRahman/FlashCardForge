import pytest
from flashcardforge.core.engine import FlashcardEngine


def test_add_card_and_decks():
    e = FlashcardEngine()
    e.add_card("Q1", "A1", "Python")
    e.add_card("Q2", "A2", "AWS")
    assert e.decks() == ["AWS", "Python"]


def test_due_cards_limit_and_filter():
    e = FlashcardEngine()
    c1 = e.add_card("Q1", "A1", "Python")
    c2 = e.add_card("Q2", "A2", "Python")
    c1.due = "2026-01-01"
    c2.due = "2026-02-01"

    due = e.due_cards(deck="Python", on_day="2026-01-10", limit=10)
    assert len(due) == 1
    assert due[0].id == c1.id

    with pytest.raises(ValueError):
        e.due_cards(limit=0)


def test_review_updates_card():
    e = FlashcardEngine()
    c = e.add_card("Q", "A", "Deck")
    c.due = "2026-01-01"

    e.review(c.id, grade=5, today="2026-01-10")
    assert e.lib.cards[c.id].due == "2026-01-11"
