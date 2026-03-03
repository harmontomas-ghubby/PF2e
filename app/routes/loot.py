from pathlib import Path

from fastapi import APIRouter, Form, Request

from app.services.loot_engine import generate_loot

router = APIRouter(prefix="/loot", tags=["loot"])


@router.get("")
def page(request: Request):
    return request.app.state.templates.TemplateResponse(request, "pages/loot.html", {"result": ""})


@router.post("/generate")
def gen(request: Request, table: str = Form("treasure")):
    result = generate_loot(Path("data/loot_tables.yaml"), table)
    return request.app.state.templates.TemplateResponse(
        request, "pages/loot.html", {"result": result}
    )
