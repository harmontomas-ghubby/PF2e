from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from app.db import get_session
from app.models import Scene
from app.services.scene_engine import generate_scene

router = APIRouter(prefix="/scenes", tags=["scenes"])


@router.get("")
def page(request: Request, campaign_id: int = 1, session: Session = Depends(get_session)):
    rows = session.exec(select(Scene).where(Scene.campaign_id == campaign_id)).all()
    return request.app.state.templates.TemplateResponse(
        request, "pages/scenes.html", {"scenes": rows, "campaign_id": campaign_id}
    )


@router.post("/generate")
def gen(
    request: Request,
    campaign_id: int = Form(...),
    title: str = Form(...),
    scene_type: str = Form("exploration"),
    session: Session = Depends(get_session),
):
    fields = generate_scene(request.app.state.oracles, scene_type)
    row = Scene(campaign_id=campaign_id, title=title, **fields)
    session.add(row)
    session.commit()
    return RedirectResponse(url=f"/scenes?campaign_id={campaign_id}", status_code=303)
