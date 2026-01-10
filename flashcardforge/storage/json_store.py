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
