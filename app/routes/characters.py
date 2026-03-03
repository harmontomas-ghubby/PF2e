from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from app.db import get_session
from app.models import Character

router = APIRouter(prefix="/characters", tags=["characters"])


@router.get("")
def page(request: Request, campaign_id: int = 1, session: Session = Depends(get_session)):
    rows = session.exec(select(Character).where(Character.campaign_id == campaign_id)).all()
    return request.app.state.templates.TemplateResponse(
        request, "pages/characters.html", {"characters": rows, "campaign_id": campaign_id}
    )


@router.post("/create")
def create(
    campaign_id: int = Form(...),
    name: str = Form(...),
    level: int = Form(1),
    session: Session = Depends(get_session),
):
    row = Character(campaign_id=campaign_id, name=name, level=level)
    session.add(row)
    session.commit()
    return RedirectResponse(url=f"/characters?campaign_id={campaign_id}", status_code=303)
