from app.services.oracle_engine import roll_table


def generate_scene(oracles, scene_type: str, seed: int | None = None):
    return {
        "objective": roll_table(oracles, "scene", "objective", seed),
        "complication": roll_table(oracles, "scene", "complication", seed),
        "twist": roll_table(oracles, "scene", "twist", seed),
        "stakes": roll_table(oracles, "scene", "stakes", seed),
        "sensory_detail": roll_table(oracles, "scene", "sensory", seed),
        "question_to_answer": f"Can the heroes resolve this {scene_type} challenge?",
    }
