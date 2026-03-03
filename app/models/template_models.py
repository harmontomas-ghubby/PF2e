from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class Metadata(BaseModel):
    id: str
    name: str
    version: int
    description: str
    recommended_levels: str
    tags: List[str] = Field(default_factory=list)


class CampaignDefaults(BaseModel):
    tone_tags: List[str] = Field(default_factory=list)
    safety_lines: str = ""
    safety_veils: str = ""
    tension_start: int = 0
    seed: int | None = None


class Defaults(BaseModel):
    campaign: CampaignDefaults


class Zone(BaseModel):
    key: str
    name: str
    depth: int
    theme_tags: List[str] = Field(default_factory=list)
    danger_tags: List[str] = Field(default_factory=list)
    notes: str = ""


class Connection(BaseModel):
    from_zone: str = Field(alias="from")
    to_zone: str = Field(alias="to")
    type: str
    is_one_way: bool = False
    notes: str = ""


class Faction(BaseModel):
    key: str
    name: str
    archetype: str
    power: int
    attitude: int
    tags: List[str] = Field(default_factory=list)
    goal: str = ""
    notes: str = ""


class Clock(BaseModel):
    key: str
    name: str
    segments_total: int
    segments_filled: int
    category: str
    tags: List[str] = Field(default_factory=list)
    notes: str = ""


class Beat(BaseModel):
    key: str
    title: str
    description: str
    zone: str
    prerequisites: List[str] = Field(default_factory=list)


class Gate(BaseModel):
    key: str
    zone: str
    name: str
    gate_type: str
    requirement_text: str
    signals: List[str] = Field(default_factory=list)
    bypass_options: List[str] = Field(default_factory=list)
    status: str = "locked"


class Discoverable(BaseModel):
    key: str
    zone: str
    category: str
    prompt: str
    implication: str
    truth: str
    status: str
    tags: List[str] = Field(default_factory=list)


class CampaignTemplate(BaseModel):
    metadata: Metadata
    defaults: Defaults
    zones: List[Zone]
    connections: List[Connection]
    factions: List[Faction]
    clocks: List[Clock]
    beats: List[Beat]
    gates: List[Gate]
    discoverables: List[Discoverable]
