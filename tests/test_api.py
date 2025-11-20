"""Tests for general API endpoints."""

import json


def test_index(client):
    """Test the index endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "message" in data
    assert "endpoints" in data


def test_health(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "healthy"
    assert "timestamp" in data


def test_statistics(client):
    """Test the statistics endpoint."""
    response = client.get("/api/stats")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "total_users" in data
    assert "total_tasks" in data
    assert "total_categories" in data
    assert "tasks_by_status" in data
    assert "tasks_by_priority" in data


def test_404_error(client):
    """Test 404 error handling."""
    response = client.get("/nonexistent")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data
