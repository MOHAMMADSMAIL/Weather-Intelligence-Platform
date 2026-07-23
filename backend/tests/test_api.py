import os
import sys
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
if str(ROOT_DIR.parent) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR.parent))

try:
    from backend.main import app
except ImportError:
    from main import app

client = TestClient(app)


def test_weather_location_not_found():
    response = client.get("/weather/this-location-does-not-exist-12345")
    assert response.status_code == 404
    assert response.json()["detail"] == "Location not found"


def test_weather_with_coordinates():
    response = client.get("/weather?latitude=40.7128&longitude=-74.0060")
    assert response.status_code == 200
    data = response.json()
    assert data["latitude"] == 40.7128
    assert data["longitude"] == -74.0060
    assert "temperature" in data


def test_crud_create_read_delete():
    payload = {
        "location": "London",
        "start_date": "2024-01-01",
        "end_date": "2024-01-02",
    }
    create_response = client.post("/requests", json=payload)
    assert create_response.status_code == 200
    record = create_response.json()
    record_id = record["id"]

    read_response = client.get(f"/requests/{record_id}")
    assert read_response.status_code == 200
    assert read_response.json()["location"] == "London"

    delete_response = client.delete(f"/requests/{record_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["detail"] == "Record deleted"
