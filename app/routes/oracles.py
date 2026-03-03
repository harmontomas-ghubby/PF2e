from fastapi import APIRouter, Request

from app.services.oracle_engine import roll_table

router = APIRouter(prefix="/oracles", tags=["oracles"])


@router.get("")
def page(request: Request):
    categories = request.app.state.oracles
    return request.app.state.templates.TemplateResponse(
        request, "pages/oracles.html", {"categories": categories, "result": ""}
    )


@router.post("/roll")
def do_roll(request: Request, category: str, table: str):
    result = roll_table(request.app.state.oracles, category, table)
    return request.app.state.templates.TemplateResponse(
        request, "pages/oracles.html", {"categories": request.app.state.oracles, "result": result}
    )
