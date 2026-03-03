from pathlib import Path

import yaml

from app.services.rng import get_rng


def generate_loot(path: Path, table: str, seed: int | None = None):
    data = yaml.safe_load(path.read_text()) or {}
    entries = data.get(table, ["mysterious trinket"])
    rng = get_rng(seed)
    return rng.choice(entries)
