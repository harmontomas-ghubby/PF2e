from pathlib import Path

from fastapi import Depends, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, or_, select

from app.db import get_session, init_db
from app.models import NPC, Campaign, Encounter, Faction, JournalEntry, Location, Scene
from app.routes import (
    campaigns,
    characters,
    clocks,
    combat,
    dice,
    encounters,
    exports,
    factions,
    journal,
    locations,
    loot,
    oracles,
    scenes,
    settings_ui,
)
from app.services.oracle_engine import load_oracles

app = FastAPI(title="Solo PF2e Table")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.state.templates = Jinja2Templates(directory="app/templates")


@app.on_event("startup")
def startup() -> None:
    init_db()
    app.state.oracles, app.state.data_errors = load_oracles(Path("data/oracles.yaml"))


@app.get("/")
def dashboard(request: Request, session: Session = Depends(get_session)):
    campaign = session.exec(select(Campaign)).first()
    timeline = session.exec(
        select(JournalEntry).order_by(JournalEntry.created_at.desc()).limit(20)
    ).all()
    open_clocks = 0
    return request.app.state.templates.TemplateResponse(
        request,
        "pages/dashboard.html",
        {"campaign": campaign, "timeline": timeline, "open_clocks": open_clocks},
    )


@app.get("/search")
def search(request: Request, q: str, session: Session = Depends(get_session)):
    results = {
        "journal": session.exec(select(JournalEntry).where(JournalEntry.body.contains(q))).all(),
        "npcs": session.exec(select(NPC).where(NPC.name.contains(q))).all(),
        "locations": session.exec(select(Location).where(Location.name.contains(q))).all(),
        "factions": session.exec(select(Faction).where(Faction.name.contains(q))).all(),
        "scenes": session.exec(
            select(Scene).where(or_(Scene.title.contains(q), Scene.objective.contains(q)))
        ).all(),
        "encounters": session.exec(select(Encounter).where(Encounter.notes.contains(q))).all(),
    }
    return request.app.state.templates.TemplateResponse(
        request, "pages/journal.html", {"entries": results["journal"], "campaign_id": 1, "q": q}
    )


for r in [
    campaigns.router,
    characters.router,
    journal.router,
    dice.router,
    oracles.router,
    scenes.router,
    encounters.router,
    combat.router,
    clocks.router,
    factions.router,
    locations.router,
    loot.router,
    exports.router,
    settings_ui.router,
]:
    app.include_router(r)
