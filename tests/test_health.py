import pytest
from fastapi.testclient import TestClient

from resume_scanner.main import app

client = TestClient(app)


def test_health_status():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "1.0.0"}


def test_health_response_structure():
    response = client.get("/health")
    data = response.json()
    assert "status" in data
    assert "version" in data


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Resume Analyzer API is running!"}
