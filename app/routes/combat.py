from datetime import datetime

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from app.db import get_session
from app.models import Combatant, CombatSession, JournalEntry

router = APIRouter(prefix="/combat", tags=["combat"])


@router.get("")
def page(request: Request, campaign_id: int = 1, session: Session = Depends(get_session)):
    combats = session.exec(
        select(CombatSession).where(CombatSession.campaign_id == campaign_id)
    ).all()
    active = combats[-1] if combats else None
    combatants = []
    if active:
        combatants = session.exec(
            select(Combatant)
            .where(Combatant.combat_session_id == active.id)
            .order_by(Combatant.initiative.desc())
        ).all()
    return request.app.state.templates.TemplateResponse(
        request,
        "pages/combat.html",
        {"campaign_id": campaign_id, "active": active, "combatants": combatants},
    )


@router.post("/start")
def start(campaign_id: int = Form(...), session: Session = Depends(get_session)):
    row = CombatSession(campaign_id=campaign_id)
    session.add(row)
    session.commit()
    return RedirectResponse(url=f"/combat?campaign_id={campaign_id}", status_code=303)


@router.post("/add")
def add(
    combat_session_id: int = Form(...),
    name: str = Form(...),
    initiative: int = Form(0),
    side: str = Form("NPC"),
    session: Session = Depends(get_session),
):
    row = Combatant(
        combat_session_id=combat_session_id, name=name, initiative=initiative, side=side
    )
    session.add(row)
    session.commit()
    return RedirectResponse(url="/combat", status_code=303)


@router.post("/next")
def next_turn(combat_session_id: int = Form(...), session: Session = Depends(get_session)):
    rows = session.exec(
        select(Combatant)
        .where(Combatant.combat_session_id == combat_session_id)
        .order_by(Combatant.initiative.desc())
    ).all()
    if rows:
        idx = next((i for i, c in enumerate(rows) if c.is_active_turn), -1)
        if idx >= 0:
            rows[idx].is_active_turn = False
        nxt = rows[(idx + 1) % len(rows)]
        nxt.is_active_turn = True
        if idx == len(rows) - 1:
            cs = session.get(CombatSession, combat_session_id)
            cs.round += 1
        session.commit()
    return RedirectResponse(url="/combat", status_code=303)


@router.post("/end")
def end(
    combat_session_id: int = Form(...),
    outcome: str = Form(""),
    session: Session = Depends(get_session),
):
    cs = session.get(CombatSession, combat_session_id)
    cs.ended_at = datetime.utcnow()
    session.add(
        JournalEntry(
            campaign_id=cs.campaign_id,
            title="Combat Summary",
            body=outcome,
            combat_session_id=cs.id,
            tags="combat",
        )
    )
    session.commit()
    return RedirectResponse(url=f"/combat?campaign_id={cs.campaign_id}", status_code=303)
