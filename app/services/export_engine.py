import json
from pathlib import Path

from sqlmodel import Session, select

from app.models import (
    NPC,
    Character,
    Clock,
    CombatSession,
    Encounter,
    Faction,
    JournalEntry,
    Location,
    Scene,
)

TABLES = [Character, NPC, Location, Scene, Encounter, CombatSession, JournalEntry, Clock, Faction]


def export_json(session: Session, campaign_id: int, out: Path):
    payload = {}
    for t in TABLES:
        rows = session.exec(select(t).where(t.campaign_id == campaign_id)).all()
        payload[t.__name__] = [r.model_dump() for r in rows]
    out.write_text(json.dumps(payload, default=str, indent=2))
    return out


def markdown_journal(entries: list[JournalEntry], out: Path):
    content = "\n\n".join([f"## {e.title or 'Entry'}\n\n{e.body}" for e in entries])
    out.write_text(content)
    return out
