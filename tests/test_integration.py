from fastapi.testclient import TestClient

from app.db import init_db
from app.main import app


def test_flow():
    init_db()
    with TestClient(app) as client:
        client.post("/campaigns/create", data={"title": "Test", "seed": 7})
        client.post("/characters/create", data={"campaign_id": 1, "name": "PC", "level": 1})
        client.post(
            "/scenes/generate",
            data={"campaign_id": 1, "title": "S1", "scene_type": "exploration"},
        )
        client.post("/combat/start", data={"campaign_id": 1})
        resp = client.post("/exports/json", data={"campaign_id": 1})
        assert resp.status_code == 200
