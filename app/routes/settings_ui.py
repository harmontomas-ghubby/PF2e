from pathlib import Path

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from app.db import get_session
from app.models import AppSetting
from app.services.oracle_engine import load_oracles

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("")
def page(request: Request, campaign_id: int = 1, session: Session = Depends(get_session)):
    s = session.exec(select(AppSetting).where(AppSetting.campaign_id == campaign_id)).first()
    return request.app.state.templates.TemplateResponse(
        request,
        "pages/settings.html",
        {"setting": s, "campaign_id": campaign_id, "data_errors": request.app.state.data_errors},
    )


@router.post("/save")
def save(
    campaign_id: int = Form(...),
    auto_journal_rolls: bool = Form(False),
    default_threat: str = Form("Moderate"),
    session: Session = Depends(get_session),
):
    s = session.exec(select(AppSetting).where(AppSetting.campaign_id == campaign_id)).first()
    if not s:
        s = AppSetting(campaign_id=campaign_id)
    s.auto_journal_rolls = auto_journal_rolls
    s.default_threat = default_threat
    session.add(s)
    session.commit()
    return RedirectResponse(url=f"/settings?campaign_id={campaign_id}", status_code=303)


@router.post("/reload-data")
def reload_data(request: Request):
    request.app.state.oracles, request.app.state.data_errors = load_oracles(
        Path("data/oracles.yaml")
    )
    return RedirectResponse(url="/settings", status_code=303)
