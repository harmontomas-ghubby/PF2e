from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import yaml
from pydantic import ValidationError

from app.models.template_models import CampaignTemplate


DATA_DIR = Path(__file__).resolve().parents[2] / "data"
TEMPLATE_DIR = DATA_DIR / "templates"


class TemplateApplyError(Exception):
    """User-facing template apply failure."""


def load_template_yaml(template_id: str) -> CampaignTemplate:
    template_path = TEMPLATE_DIR / f"{template_id}.yaml"
    if not template_path.exists():
        raise TemplateApplyError(f"Template '{template_id}' was not found.")
    raw = yaml.safe_load(template_path.read_text(encoding="utf-8"))
    try:
        return CampaignTemplate.model_validate(raw)
    except ValidationError as exc:
        raise TemplateApplyError(f"Template '{template_id}' is invalid: {exc.errors()[0]['msg']}") from exc


def campaign_has_content(conn: sqlite3.Connection, campaign_id: int) -> bool:
    checks = ["zones", "beats", "gates", "clocks", "factions", "discoverables"]
    for table in checks:
        value = conn.execute(
            f"SELECT COUNT(1) FROM {table} WHERE campaign_id = ?", (campaign_id,)
        ).fetchone()[0]
        if value > 0:
            return True
    return False


def apply_template(conn: sqlite3.Connection, campaign_id: int, template_id: str) -> dict:
    template = load_template_yaml(template_id)

    row = conn.execute(
        "SELECT id, template_id FROM campaigns WHERE id = ?", (campaign_id,)
    ).fetchone()
    if not row:
        raise TemplateApplyError("Campaign not found.")
    if row[1]:
        raise TemplateApplyError("Template already applied.")
    if campaign_has_content(conn, campaign_id):
        raise TemplateApplyError("Template can only be applied to a new campaign.")

    zone_ids: dict[str, int] = {}
    beat_ids: dict[str, int] = {}

    try:
        with conn:
            conn.execute(
                "UPDATE campaigns SET template_id = ?, tension_current = ?, seed = ? WHERE id = ?",
                (
                    template.metadata.id,
                    template.defaults.campaign.tension_start,
                    template.defaults.campaign.seed,
                    campaign_id,
                ),
            )

            for zone in template.zones:
                cur = conn.execute(
                    """
                    INSERT INTO zones(campaign_id, zone_key, name, depth, theme_tags, danger_tags, notes)
                    VALUES(?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        campaign_id,
                        zone.key,
                        zone.name,
                        zone.depth,
                        json.dumps(zone.theme_tags),
                        json.dumps(zone.danger_tags),
                        zone.notes,
                    ),
                )
                zone_ids[zone.key] = cur.lastrowid

            for connection in template.connections:
                conn.execute(
                    """
                    INSERT INTO connections(campaign_id, from_zone_id, to_zone_id, type, is_one_way, notes)
                    VALUES(?, ?, ?, ?, ?, ?)
                    """,
                    (
                        campaign_id,
                        zone_ids[connection.from_zone],
                        zone_ids[connection.to_zone],
                        connection.type,
                        int(connection.is_one_way),
                        connection.notes,
                    ),
                )

            for faction in template.factions:
                conn.execute(
                    """
                    INSERT INTO factions(campaign_id, faction_key, name, archetype, power, attitude, tags, goal, notes)
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        campaign_id,
                        faction.key,
                        faction.name,
                        faction.archetype,
                        faction.power,
                        faction.attitude,
                        json.dumps(faction.tags),
                        faction.goal,
                        faction.notes,
                    ),
                )

            for clock in template.clocks:
                conn.execute(
                    """
                    INSERT INTO clocks(campaign_id, clock_key, name, segments_total, segments_filled, category, tags, notes)
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        campaign_id,
                        clock.key,
                        clock.name,
                        clock.segments_total,
                        clock.segments_filled,
                        clock.category,
                        json.dumps(clock.tags),
                        clock.notes,
                    ),
                )

            for beat in template.beats:
                cur = conn.execute(
                    """
                    INSERT INTO beats(campaign_id, beat_key, zone_id, title, description)
                    VALUES(?, ?, ?, ?, ?)
                    """,
                    (campaign_id, beat.key, zone_ids[beat.zone], beat.title, beat.description),
                )
                beat_ids[beat.key] = cur.lastrowid

            for beat in template.beats:
                for prereq in beat.prerequisites:
                    conn.execute(
                        "INSERT INTO beat_prerequisites(campaign_id, beat_id, prerequisite_beat_id) VALUES(?, ?, ?)",
                        (campaign_id, beat_ids[beat.key], beat_ids[prereq]),
                    )

            for gate in template.gates:
                conn.execute(
                    """
                    INSERT INTO gates(campaign_id, gate_key, zone_id, name, gate_type, requirement_text, signals, bypass_options, status)
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        campaign_id,
                        gate.key,
                        zone_ids[gate.zone],
                        gate.name,
                        gate.gate_type,
                        gate.requirement_text,
                        json.dumps(gate.signals),
                        json.dumps(gate.bypass_options),
                        gate.status,
                    ),
                )

            for discoverable in template.discoverables:
                conn.execute(
                    """
                    INSERT INTO discoverables(
                      campaign_id, discoverable_key, zone_id, category, prompt, implication, truth, status, tags
                    ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        campaign_id,
                        discoverable.key,
                        zone_ids[discoverable.zone],
                        discoverable.category,
                        discoverable.prompt,
                        discoverable.implication,
                        discoverable.truth,
                        discoverable.status,
                        json.dumps(discoverable.tags),
                    ),
                )
    except KeyError as exc:
        raise TemplateApplyError(f"Template references unknown key: {exc}") from exc

    return {"campaign_id": campaign_id, "template_id": template.metadata.id}


def resolve_campaign_data_file(campaign_template_id: str | None, domain: str) -> Path:
    mapping = {
        "shattered_titan_vault": {
            "wandering": DATA_DIR / "wandering" / "titan_vault.yaml",
            "next_questions": DATA_DIR / "next_questions" / "titan_vault.yaml",
            "tension_rules": DATA_DIR / "tension_rules" / "titan_vault.yaml",
        }
    }
    defaults = {
        "wandering": DATA_DIR / "wandering" / "default.yaml",
        "next_questions": DATA_DIR / "next_questions" / "default.yaml",
        "tension_rules": DATA_DIR / "tension_rules" / "default.yaml",
    }
    if campaign_template_id in mapping:
        return mapping[campaign_template_id][domain]
    return defaults[domain]
