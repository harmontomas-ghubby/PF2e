from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from app.db import get_session
from app.models import JournalEntry

router = APIRouter(prefix="/journal", tags=["journal"])


@router.get("")
def page(
    request: Request, campaign_id: int = 1, q: str = "", session: Session = Depends(get_session)
):
    stmt = select(JournalEntry).where(JournalEntry.campaign_id == campaign_id)
    if q:
        stmt = stmt.where(JournalEntry.body.contains(q))
    entries = session.exec(stmt.order_by(JournalEntry.created_at.desc())).all()
    return request.app.state.templates.TemplateResponse(
        request, "pages/journal.html", {"entries": entries, "campaign_id": campaign_id, "q": q}
    )


@router.post("/create")
def create(
    campaign_id: int = Form(...),
    title: str = Form(""),
    body: str = Form(...),
    tags: str = Form(""),
    session: Session = Depends(get_session),
):
    entry = JournalEntry(campaign_id=campaign_id, title=title, body=body, tags=tags)
    session.add(entry)
    session.commit()
    return RedirectResponse(url=f"/journal?campaign_id={campaign_id}", status_code=303)
