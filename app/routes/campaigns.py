from __future__ import annotations

import sqlite3

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.services.template_loader import TemplateApplyError, apply_template

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect("app.db")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


@router.get("/campaigns/{campaign_id}/templates/shattered-titan-vault/confirm", response_class=HTMLResponse)
def confirm_apply_template(request: Request, campaign_id: int):
    return templates.TemplateResponse(
        request,
        "components/template_confirm_modal.html",
        {"campaign_id": campaign_id, "template_slug": "shattered-titan-vault"},
    )


@router.post("/campaigns/{campaign_id}/templates/shattered-titan-vault/apply")
def apply_shattered_titan_vault(campaign_id: int, request: Request, conn: sqlite3.Connection = Depends(get_db)):
    try:
        apply_template(conn, campaign_id, "shattered_titan_vault")
    except TemplateApplyError as exc:
        return templates.TemplateResponse(
            request,
            "components/template_apply_error.html",
            {"campaign_id": campaign_id, "error_message": str(exc)},
            status_code=400,
        )

    response = RedirectResponse(url=f"/campaigns/{campaign_id}?template_applied=1", status_code=303)
    response.headers["HX-Trigger"] = "templateApplied"
    return response
