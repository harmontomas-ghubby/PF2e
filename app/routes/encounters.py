from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from app.db import get_session
from app.models import Encounter
from app.services.encounter_engine import generate_encounter

router = APIRouter(prefix="/encounters", tags=["encounters"])


@router.get("")
def page(request: Request, campaign_id: int = 1, session: Session = Depends(get_session)):
    rows = session.exec(select(Encounter).where(Encounter.campaign_id == campaign_id)).all()
    return request.app.state.templates.TemplateResponse(
        request, "pages/encounters.html", {"encounters": rows, "campaign_id": campaign_id}
    )


@router.post("/generate")
def generate(
    campaign_id: int = Form(...),
    level: int = Form(1),
    threat: str = Form("Moderate"),
    environment: str = Form("wilderness"),
    scene_type: str = Form("exploration"),
    session: Session = Depends(get_session),
):
    outline = generate_encounter(level, threat, environment, scene_type)
    row = Encounter(campaign_id=campaign_id, threat_label=threat, outline=outline)
    session.add(row)
    session.commit()
    return RedirectResponse(url=f"/encounters?campaign_id={campaign_id}", status_code=303)
