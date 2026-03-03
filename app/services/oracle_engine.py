from pathlib import Path

import yaml

from app.schemas import OracleCategory
from app.services.rng import get_rng


def load_oracles(path: Path) -> tuple[list[OracleCategory], list[str]]:
    errors = []
    try:
        raw = yaml.safe_load(path.read_text()) or []
    except Exception as e:
        return [], [f"oracles.yaml: {e}"]
    parsed = []
    for idx, item in enumerate(raw):
        try:
            parsed.append(OracleCategory.model_validate(item))
        except Exception as e:
            errors.append(f"entry {idx}: {e}")
    return parsed, errors


def roll_table(
    categories: list[OracleCategory], category: str, table: str, seed: int | None = None
):
    rng = get_rng(seed)
    for c in categories:
        if c.category == category:
            for t in c.tables:
                if t.name == table:
                    pop = [e.text for e in t.entries]
                    weights = [e.weight for e in t.entries]
                    result = rng.choices(population=pop, weights=weights, k=1)[0]
                    return result.format(npc_name="Rook", settlement="Rivergate", mood="tense")
    return "No oracle match"
