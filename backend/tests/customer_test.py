from sqlalchemy import select
from app.db import get_session
from app.models.customer import Customer

def test_health(client):
    res = client.get("/healthz")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"
    