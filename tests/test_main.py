# tests/test_main.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_index():
    response = client.get("/")
    assert response.status_code == 200

def test_process_event():
    response = client.post("/process", data={"event_text": "Meeting on 2024-12-01 at 10 AM"})
    assert response.status_code == 200
    assert response.headers["Content-Disposition"] == 'attachment; filename="event.ics"'
