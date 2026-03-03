from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from app.db import get_session
from app.models import Campaign

router = APIRouter(prefix="/campaigns", tags=["campaigns"])


@router.get("")
def list_campaigns(request: Request, session: Session = Depends(get_session)):
    campaigns = session.exec(select(Campaign)).all()
    return request.app.state.templates.TemplateResponse(
        request, "pages/campaigns.html", {"campaigns": campaigns}
    )


@router.post("/create")
def create_campaign(
    title: str = Form(...), seed: int = Form(42), session: Session = Depends(get_session)
):
    c = Campaign(title=title, seed=seed)
    session.add(c)
    session.commit()
    return RedirectResponse(url="/campaigns", status_code=303)
