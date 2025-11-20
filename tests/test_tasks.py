"""Tests for task endpoints."""

import json
from datetime import datetime, timedelta


def test_create_task(client):
    """Test creating a new task."""
    # Create a user first
    user_response = client.post(
        "/api/users",
        data=json.dumps({"username": "testuser", "email": "test@example.com"}),
        content_type="application/json",
    )
    user_id = json.loads(user_response.data)["id"]

    # Create a task
    response = client.post(
        "/api/tasks",
        data=json.dumps(
            {
                "title": "Test task",
                "description": "Test description",
                "status": "pending",
                "priority": "high",
                "user_id": user_id,
            }
        ),
        content_type="application/json",
    )

    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["title"] == "Test task"
    assert data["status"] == "pending"
    assert data["priority"] == "high"


def test_get_tasks(client):
    """Test getting all tasks."""
    # Create a user and task first
    user_response = client.post(
        "/api/users",
        data=json.dumps({"username": "testuser", "email": "test@example.com"}),
        content_type="application/json",
    )
    user_id = json.loads(user_response.data)["id"]

    client.post(
        "/api/tasks",
        data=json.dumps(
            {"title": "Test task", "description": "Test description", "user_id": user_id}
        ),
        content_type="application/json",
    )

    response = client.get("/api/tasks")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1


def test_update_task(client):
    """Test updating a task."""
    # Create a user and task first
    user_response = client.post(
        "/api/users",
        data=json.dumps({"username": "testuser", "email": "test@example.com"}),
        content_type="application/json",
    )
    user_id = json.loads(user_response.data)["id"]

    task_response = client.post(
        "/api/tasks",
        data=json.dumps(
            {"title": "Test task", "description": "Test description", "user_id": user_id}
        ),
        content_type="application/json",
    )
    task_id = json.loads(task_response.data)["id"]

    # Update the task
    response = client.put(
        f"/api/tasks/{task_id}",
        data=json.dumps({"status": "completed", "priority": "low"}),
        content_type="application/json",
    )

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "completed"
    assert data["priority"] == "low"


def test_delete_task(client):
    """Test deleting a task."""
    # Create a user and task first
    user_response = client.post(
        "/api/users",
        data=json.dumps({"username": "testuser", "email": "test@example.com"}),
        content_type="application/json",
    )
    user_id = json.loads(user_response.data)["id"]

    task_response = client.post(
        "/api/tasks",
        data=json.dumps(
            {"title": "Test task", "description": "Test description", "user_id": user_id}
        ),
        content_type="application/json",
    )
    task_id = json.loads(task_response.data)["id"]

    # Delete the task
    response = client.delete(f"/api/tasks/{task_id}")
    assert response.status_code == 200

    # Verify task is deleted
    get_response = client.get(f"/api/tasks/{task_id}")
    assert get_response.status_code == 404


def test_filter_tasks_by_status(client):
    """Test filtering tasks by status."""
    # Create a user and multiple tasks
    user_response = client.post(
        "/api/users",
        data=json.dumps({"username": "testuser", "email": "test@example.com"}),
        content_type="application/json",
    )
    user_id = json.loads(user_response.data)["id"]

    client.post(
        "/api/tasks",
        data=json.dumps(
            {"title": "Task 1", "status": "pending", "user_id": user_id}
        ),
        content_type="application/json",
    )

    client.post(
        "/api/tasks",
        data=json.dumps(
            {"title": "Task 2", "status": "completed", "user_id": user_id}
        ),
        content_type="application/json",
    )

    # Filter by status
    response = client.get("/api/tasks?status=pending")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]["status"] == "pending"
