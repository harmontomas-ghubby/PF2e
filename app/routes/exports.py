import json
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from fastapi.responses import FileResponse, RedirectResponse
from sqlmodel import Session, select

from app.db import get_session
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
from app.services.export_engine import export_json, markdown_journal

router = APIRouter(prefix="/exports", tags=["exports"])


@router.get("")
def page(request: Request):
    return request.app.state.templates.TemplateResponse(request, "pages/exports.html", {})


@router.post("/json")
def do_json(campaign_id: int = Form(...), session: Session = Depends(get_session)):
    path = export_json(session, campaign_id, Path(f"campaign_{campaign_id}.json"))
    return FileResponse(path)


@router.post("/markdown")
def do_md(campaign_id: int = Form(...), session: Session = Depends(get_session)):
    entries = session.exec(
        select(JournalEntry).where(JournalEntry.campaign_id == campaign_id)
    ).all()
    path = markdown_journal(entries, Path(f"campaign_{campaign_id}.md"))
    return FileResponse(path)


@router.post("/import")
def do_import(
    campaign_id: int = Form(...),
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
):
    payload = json.loads(file.file.read().decode())
    tables = [
        Character,
        NPC,
        Location,
        Scene,
        Encounter,
        CombatSession,
        JournalEntry,
        Clock,
        Faction,
    ]
    for t in tables:
        for row in payload.get(t.__name__, []):
            row.pop("id", None)
            row["campaign_id"] = campaign_id
            session.add(t(**row))
    session.commit()
    return RedirectResponse(url="/exports", status_code=303)
