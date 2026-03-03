from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from app.db import get_session
from app.models import RollHistory
from app.services.dice_engine import roll

router = APIRouter(prefix="/dice", tags=["dice"])


@router.get("")
def page(request: Request, campaign_id: int = 1, session: Session = Depends(get_session)):
    history = session.exec(
        select(RollHistory)
        .where(RollHistory.campaign_id == campaign_id)
        .order_by(RollHistory.created_at.desc())
    ).all()
    return request.app.state.templates.TemplateResponse(
        request, "pages/dice.html", {"history": history, "campaign_id": campaign_id}
    )


@router.post("/roll")
def do_roll(
    campaign_id: int = Form(...),
    expression: str = Form(...),
    session: Session = Depends(get_session),
):
    result = roll(expression)
    row = RollHistory(
        campaign_id=campaign_id,
        expression=expression,
        total=result["total"],
        breakdown=result["breakdown"],
    )
    session.add(row)
    session.commit()
    return RedirectResponse(url=f"/dice?campaign_id={campaign_id}", status_code=303)
