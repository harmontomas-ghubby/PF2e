import json
from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine

from app.models import Character
from app.services.export_engine import export_json


def test_json_roundtrip(tmp_path: Path):
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as s:
        s.add(Character(campaign_id=1, name="Hero"))
        s.commit()
        out = export_json(s, 1, tmp_path / "out.json")
    payload = json.loads(out.read_text())
    assert payload["Character"][0]["name"] == "Hero"
