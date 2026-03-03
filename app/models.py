from datetime import datetime
from typing import Any, Optional

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


def now_utc() -> datetime:
    return datetime.utcnow()


class Campaign(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    system: str = "PF2e-compatible toolkit"
    tone_tags: str = ""
    safety_lines: str = ""
    safety_veils: str = ""
    in_game_datetime: str = ""
    seed: int = 42
    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(default_factory=now_utc)


class Character(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    campaign_id: int = Field(index=True)
    name: str
    level: int = 1
    ancestry: str = ""
    heritage: str = ""
    class_name: str = ""
    background: str = ""
    max_hp: int = 10
    current_hp: int = 10
    temp_hp: int = 0
    ac: int = 10
    perception: int = 0
    speed: int = 25
    hero_points: int = 1
    conditions: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    resources: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    inventory: list[dict[str, Any]] = Field(default_factory=list, sa_column=Column(JSON))
    notes: str = ""


class NPC(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    campaign_id: int = Field(index=True)
    name: str
    role: str = ""
    disposition: int = 0
    tags: str = ""
    notes: str = ""
    first_seen_scene_id: Optional[int] = None


class Location(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    campaign_id: int = Field(index=True)
    name: str
    type: str = "wilderness"
    tags: str = ""
    notes: str = ""
    parent_location_id: Optional[int] = None
    x: int = 50
    y: int = 50
    discovered_at: datetime = Field(default_factory=now_utc)


class Scene(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    campaign_id: int = Field(index=True)
    title: str
    location_id: Optional[int] = None
    objective: str = ""
    complication: str = ""
    twist: str = ""
    stakes: str = ""
    sensory_detail: str = ""
    question_to_answer: str = ""
    involved_npcs: list[int] = Field(default_factory=list, sa_column=Column(JSON))
    status: str = "active"
    seed_used: int = 0
    created_at: datetime = Field(default_factory=now_utc)


class Encounter(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    campaign_id: int = Field(index=True)
    scene_id: Optional[int] = None
    threat_label: str = "Moderate"
    outline: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    notes: str = ""
    seed_used: int = 0
    created_at: datetime = Field(default_factory=now_utc)


class CombatSession(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    campaign_id: int = Field(index=True)
    scene_id: Optional[int] = None
    round: int = 1
    started_at: datetime = Field(default_factory=now_utc)
    ended_at: Optional[datetime] = None


class Combatant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    combat_session_id: int = Field(index=True)
    name: str
    side: str = "NPC"
    initiative: int = 0
    max_hp: int = 10
    current_hp: int = 10
    temp_hp: int = 0
    conditions: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    notes: str = ""
    is_active_turn: bool = False


class JournalEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    campaign_id: int = Field(index=True)
    created_at: datetime = Field(default_factory=now_utc)
    tags: str = ""
    title: str = ""
    body: str
    pinned: bool = False
    scene_id: Optional[int] = None
    encounter_id: Optional[int] = None
    combat_session_id: Optional[int] = None
    npc_id: Optional[int] = None
    location_id: Optional[int] = None


class Clock(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    campaign_id: int = Field(index=True)
    name: str
    segments_total: int = 4
    segments_filled: int = 0
    category: str = "mystery"
    tags: str = ""
    notes: str = ""
    auto_advance_rules: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))


class Faction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    campaign_id: int = Field(index=True)
    name: str
    archetype: str = ""
    power: int = 1
    attitude: int = 0
    tags: str = ""
    goal: str = ""
    notes: str = ""
    relationships: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))


class AppSetting(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    campaign_id: int = Field(index=True)
    auto_journal_rolls: bool = False
    auto_save_scene: bool = True
    show_safety_prompts: bool = True
    default_threat: str = "Moderate"
    advanced_dice: bool = True
    rng_mode: str = "fixed"
    datetime_format: str = "%Y-%m-%d %H:%M"
    values: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))


class RollHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    campaign_id: int = Field(index=True)
    expression: str
    total: int
    breakdown: str
    created_at: datetime = Field(default_factory=now_utc)
