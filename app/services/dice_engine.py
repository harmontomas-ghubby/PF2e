import random
import re

DICE_RE = re.compile(r"(\d*)d(\d+)(kh\d+|kl\d+|dh\d+|dl\d+)?(!)?")


def _roll_term(term: str, rng: random.Random) -> tuple[int, str]:
    m = DICE_RE.fullmatch(term.strip())
    if not m:
        return int(eval(term, {"__builtins__": {}}, {})), term
    n = int(m.group(1) or 1)
    sides = int(m.group(2))
    kd = m.group(3)
    exploding = bool(m.group(4))
    rolls = []
    for _ in range(n):
        r = rng.randint(1, sides)
        rolls.append(r)
        while exploding and r == sides:
            r = rng.randint(1, sides)
            rolls.append(r)
    kept = rolls[:]
    if kd:
        kind, amt = kd[:2], int(kd[2:])
        sorted_rolls = sorted(rolls)
        if kind == "kh":
            kept = sorted_rolls[-amt:]
        elif kind == "kl":
            kept = sorted_rolls[:amt]
        elif kind == "dh":
            kept = sorted_rolls[:-amt] if amt < len(sorted_rolls) else []
        elif kind == "dl":
            kept = sorted_rolls[amt:]
    return sum(kept), f"{term}=>{rolls} kept {kept}"


def roll(expression: str, seed: int | None = None) -> dict:
    rng = random.Random(seed)
    label = ""
    expr = expression
    if ":" in expression:
        label, expr = [x.strip() for x in expression.split(":", 1)]
    expr = expr.replace("d20 adv", "2d20kh1").replace("d20 dis", "2d20kl1")
    details = []

    def repl(match):
        t = match.group(0)
        total, d = _roll_term(t, rng)
        details.append(d)
        return str(total)

    replaced = DICE_RE.sub(repl, expr)
    total = int(eval(replaced, {"__builtins__": {}}, {}))
    return {
        "label": label,
        "expression": expression,
        "total": total,
        "breakdown": "; ".join(details),
    }
