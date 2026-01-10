from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

from flashcardforge.core.engine import FlashcardEngine


@dataclass(frozen=True)
class StorePaths:
    base_dir: Path
    db_file: Path


def get_paths() -> StorePaths:
    home = Path(os.path.expanduser("~"))
    base = home / ".flashcardforge"
    return StorePaths(base_dir=base, db_file=base / "db.json")


class JsonStore:
    def __init__(self, db_file: Path | None = None) -> None:
        self.db_file = db_file or get_paths().db_file

    def load(self) -> FlashcardEngine:
        if not self.db_file.exists():
            return FlashcardEngine()
        try:
            data = json.loads(self.db_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return FlashcardEngine()
        return FlashcardEngine.from_dict(data)

    def save(self, engine: FlashcardEngine) -> None:
        self.db_file.parent.mkdir(parents=True, exist_ok=True)
        self.db_file.write_text(json.dumps(
            engine.to_dict(), indent=2), encoding="utf-8")
