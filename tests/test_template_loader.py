import sqlite3

import pytest

from app.services.template_loader import TemplateApplyError, apply_template


def init_db(conn: sqlite3.Connection):
    conn.executescript(
        """
        CREATE TABLE campaigns (
          id INTEGER PRIMARY KEY,
          name TEXT,
          template_id TEXT,
          tension_current INTEGER DEFAULT 0,
          seed INTEGER
        );
        CREATE TABLE zones (
          id INTEGER PRIMARY KEY,
          campaign_id INTEGER,
          zone_key TEXT,
          name TEXT,
          depth INTEGER,
          theme_tags TEXT,
          danger_tags TEXT,
          notes TEXT
        );
        CREATE TABLE connections (
          id INTEGER PRIMARY KEY,
          campaign_id INTEGER,
          from_zone_id INTEGER,
          to_zone_id INTEGER,
          type TEXT,
          is_one_way INTEGER,
          notes TEXT
        );
        CREATE TABLE factions (
          id INTEGER PRIMARY KEY,
          campaign_id INTEGER,
          faction_key TEXT,
          name TEXT,
          archetype TEXT,
          power INTEGER,
          attitude INTEGER,
          tags TEXT,
          goal TEXT,
          notes TEXT
        );
        CREATE TABLE clocks (
          id INTEGER PRIMARY KEY,
          campaign_id INTEGER,
          clock_key TEXT,
          name TEXT,
          segments_total INTEGER,
          segments_filled INTEGER,
          category TEXT,
          tags TEXT,
          notes TEXT
        );
        CREATE TABLE beats (
          id INTEGER PRIMARY KEY,
          campaign_id INTEGER,
          beat_key TEXT,
          zone_id INTEGER,
          title TEXT,
          description TEXT
        );
        CREATE TABLE beat_prerequisites (
          id INTEGER PRIMARY KEY,
          campaign_id INTEGER,
          beat_id INTEGER,
          prerequisite_beat_id INTEGER
        );
        CREATE TABLE gates (
          id INTEGER PRIMARY KEY,
          campaign_id INTEGER,
          gate_key TEXT,
          zone_id INTEGER,
          name TEXT,
          gate_type TEXT,
          requirement_text TEXT,
          signals TEXT,
          bypass_options TEXT,
          status TEXT
        );
        CREATE TABLE discoverables (
          id INTEGER PRIMARY KEY,
          campaign_id INTEGER,
          discoverable_key TEXT,
          zone_id INTEGER,
          category TEXT,
          prompt TEXT,
          implication TEXT,
          truth TEXT,
          status TEXT,
          tags TEXT
        );
        """
    )


@pytest.fixture
def conn():
    connection = sqlite3.connect(":memory:")
    init_db(connection)
    connection.execute("INSERT INTO campaigns(id, name, tension_current) VALUES(1, 'Test', 0)")
    yield connection
    connection.close()


def test_apply_template_creates_scaffold(conn):
    apply_template(conn, 1, "shattered_titan_vault")

    assert conn.execute("SELECT COUNT(*) FROM zones WHERE campaign_id = 1").fetchone()[0] == 6
    assert conn.execute("SELECT COUNT(*) FROM connections WHERE campaign_id = 1").fetchone()[0] >= 5
    assert conn.execute("SELECT COUNT(*) FROM factions WHERE campaign_id = 1").fetchone()[0] == 3

    totals = dict(conn.execute("SELECT clock_key, segments_total FROM clocks WHERE campaign_id = 1").fetchall())
    assert totals["containment_stability"] == 8
    assert totals["awakening_hymn"] == 10
    assert totals["delver_support"] == 6

    assert conn.execute("SELECT COUNT(*) FROM beats WHERE campaign_id = 1").fetchone()[0] >= 7
    assert conn.execute("SELECT COUNT(*) FROM beat_prerequisites WHERE campaign_id = 1").fetchone()[0] >= 6
    assert conn.execute("SELECT COUNT(*) FROM gates WHERE campaign_id = 1").fetchone()[0] >= 3
    assert conn.execute("SELECT COUNT(*) FROM discoverables WHERE campaign_id = 1").fetchone()[0] >= 6

    campaign = conn.execute(
        "SELECT template_id, tension_current, seed FROM campaigns WHERE id = 1"
    ).fetchone()
    assert campaign[0] == "shattered_titan_vault"
    assert campaign[1] == 3
    assert campaign[2] == 12345


def test_apply_template_rejects_non_empty_campaign(conn):
    conn.execute(
        "INSERT INTO zones(campaign_id, zone_key, name, depth, theme_tags, danger_tags, notes) VALUES(1, 'z', 'Z', 1, '[]', '[]', '')"
    )

    with pytest.raises(TemplateApplyError, match="new campaign"):
        apply_template(conn, 1, "shattered_titan_vault")
