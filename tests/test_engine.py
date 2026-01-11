import pytest
from flashcardforge.core.engine import FlashcardEngine


def test_add_card_and_decks():
    e = FlashcardEngine()
    e.add_card("Q1", "A1", "Python")
    e.add_card("Q2", "A2", "AWS")
    assert e.decks() == ["AWS", "Python"]
