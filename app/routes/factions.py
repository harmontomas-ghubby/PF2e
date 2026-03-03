from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from app.db import get_session
from app.models import Faction, JournalEntry
from app.services.oracle_engine import roll_table

router = APIRouter(prefix="/factions", tags=["factions"])


@router.get("")
def page(request: Request, campaign_id: int = 1, session: Session = Depends(get_session)):
    rows = session.exec(select(Faction).where(Faction.campaign_id == campaign_id)).all()
    return request.app.state.templates.TemplateResponse(
        request, "pages/factions.html", {"factions": rows, "campaign_id": campaign_id}
    )


@router.post("/create")
def create(
    campaign_id: int = Form(...),
    name: str = Form(...),
    archetype: str = Form(""),
    session: Session = Depends(get_session),
):
    session.add(Faction(campaign_id=campaign_id, name=name, archetype=archetype))
    session.commit()
    return RedirectResponse(url=f"/factions?campaign_id={campaign_id}", status_code=303)


@router.post("/advance")
def advance(request: Request, faction_id: int = Form(...), session: Session = Depends(get_session)):
    f = session.get(Faction, faction_id)
    move = roll_table(request.app.state.oracles, "faction", "moves")
    session.add(
        JournalEntry(
            campaign_id=f.campaign_id, title=f"Faction Turn: {f.name}", body=move, tags="faction"
        )
    )
    session.commit()
    return RedirectResponse(url=f"/factions?campaign_id={f.campaign_id}", status_code=303)
