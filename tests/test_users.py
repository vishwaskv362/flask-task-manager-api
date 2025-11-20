"""Tests for user endpoints."""

import json


def test_create_user(client):
    """Test creating a new user."""
    response = client.post(
        "/api/users",
        data=json.dumps({"username": "testuser", "email": "test@example.com"}),
        content_type="application/json",
    )

    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"


def test_get_users(client):
    """Test getting all users."""
    # Create a user first
    client.post(
        "/api/users",
        data=json.dumps({"username": "testuser", "email": "test@example.com"}),
        content_type="application/json",
    )

    response = client.get("/api/users")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1


def test_get_user(client):
    """Test getting a specific user."""
    # Create a user first
    create_response = client.post(
        "/api/users",
        data=json.dumps({"username": "testuser", "email": "test@example.com"}),
        content_type="application/json",
    )
    user_id = json.loads(create_response.data)["id"]

    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["username"] == "testuser"


def test_delete_user(client):
    """Test deleting a user."""
    # Create a user first
    create_response = client.post(
        "/api/users",
        data=json.dumps({"username": "testuser", "email": "test@example.com"}),
        content_type="application/json",
    )
    user_id = json.loads(create_response.data)["id"]

    response = client.delete(f"/api/users/{user_id}")
    assert response.status_code == 200

    # Verify user is deleted
    get_response = client.get(f"/api/users/{user_id}")
    assert get_response.status_code == 404
