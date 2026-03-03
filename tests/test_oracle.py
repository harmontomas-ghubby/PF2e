from pathlib import Path

from app.services.oracle_engine import load_oracles, roll_table


def test_weights_nested_and_tokens():
    cats, errs = load_oracles(Path("data/oracles.yaml"))
    assert not errs
    out = roll_table(cats, "faction", "moves", seed=1)
    assert "{" not in out
