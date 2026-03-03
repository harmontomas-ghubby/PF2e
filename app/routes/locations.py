from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from app.db import get_session
from app.models import Location

router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("")
def page(request: Request, campaign_id: int = 1, session: Session = Depends(get_session)):
    rows = session.exec(select(Location).where(Location.campaign_id == campaign_id)).all()
    return request.app.state.templates.TemplateResponse(
        request, "pages/locations.html", {"locations": rows, "campaign_id": campaign_id}
    )


@router.post("/create")
def create(
    campaign_id: int = Form(...),
    name: str = Form(...),
    x: int = Form(100),
    y: int = Form(100),
    session: Session = Depends(get_session),
):
    session.add(Location(campaign_id=campaign_id, name=name, x=x, y=y))
    session.commit()
    return RedirectResponse(url=f"/locations?campaign_id={campaign_id}", status_code=303)


@router.post("/move")
def move(
    location_id: int = Form(...),
    x: int = Form(...),
    y: int = Form(...),
    session: Session = Depends(get_session),
):
    loc = session.get(Location, location_id)
    loc.x = x
    loc.y = y
    session.commit()
    return {"ok": True}
