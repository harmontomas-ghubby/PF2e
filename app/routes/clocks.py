from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from app.db import get_session
from app.models import Clock

router = APIRouter(prefix="/clocks", tags=["clocks"])


@router.get("")
def page(request: Request, campaign_id: int = 1, session: Session = Depends(get_session)):
    rows = session.exec(select(Clock).where(Clock.campaign_id == campaign_id)).all()
    return request.app.state.templates.TemplateResponse(
        request, "pages/clocks.html", {"clocks": rows, "campaign_id": campaign_id}
    )


@router.post("/create")
def create(
    campaign_id: int = Form(...),
    name: str = Form(...),
    segments_total: int = Form(4),
    session: Session = Depends(get_session),
):
    session.add(Clock(campaign_id=campaign_id, name=name, segments_total=segments_total))
    session.commit()
    return RedirectResponse(url=f"/clocks?campaign_id={campaign_id}", status_code=303)


@router.post("/tick")
def tick(clock_id: int = Form(...), delta: int = Form(1), session: Session = Depends(get_session)):
    c = session.get(Clock, clock_id)
    c.segments_filled = max(0, min(c.segments_total, c.segments_filled + delta))
    session.commit()
    return RedirectResponse(url="/clocks", status_code=303)
