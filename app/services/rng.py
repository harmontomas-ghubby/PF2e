import random


def get_rng(seed: int | None = None) -> random.Random:
    return random.Random(seed)
