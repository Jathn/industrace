import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_user():
    response = client.post(
        "/users",
        json={
            "email": "test@example.com",
            "password": "test123",
            "name": "Test User",
            "role_id": "00000000-0000-0000-0000-000000000001",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
