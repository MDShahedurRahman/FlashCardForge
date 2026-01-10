from flashcardforge.core.models import Card
from flashcardforge.core.scheduler import update_card, Grade


def test_update_card_incorrect_resets():
    c = Card.new("Q", "A", "Deck")
    c.due = "2026-01-01"
    c.interval = 10
    c.repetitions = 5
    c.ease = 2.5

    update_card(c, Grade(2), today="2026-01-10")
    assert c.repetitions == 0
    assert c.interval == 1
    assert c.due == "2026-01-11"


def test_update_card_correct_increases_interval():
    c = Card.new("Q", "A", "Deck")
    c.due = "2026-01-01"
    c.interval = 0
    c.repetitions = 0
    c.ease = 2.5

    update_card(c, Grade(5), today="2026-01-10")
    assert c.repetitions == 1
    assert c.interval == 1
    assert c.due == "2026-01-11"

    update_card(c, Grade(5), today="2026-01-11")
    assert c.repetitions == 2
    assert c.interval == 6
    assert c.due == "2026-01-17"
