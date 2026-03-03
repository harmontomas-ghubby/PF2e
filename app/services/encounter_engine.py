from app.services.rng import get_rng


def generate_encounter(
    level: int, threat: str, environment: str, scene_type: str, seed: int | None = None
):
    rng = get_rng(seed)
    count = rng.randint(1, 4)
    return {
        "foe_count": f"{count}-{count + 1}",
        "roles": ["brute", "skirmisher", "controller"][: rng.randint(1, 3)],
        "terrain": f"{environment} obstacle",
        "hazard": "unstable ground",
        "morale": "Retreat at heavy losses",
        "reward_outline": "Roll on loot table: encounter_reward",
        "note": f"Outline only for level {level} and {threat} threat in {scene_type}.",
    }
