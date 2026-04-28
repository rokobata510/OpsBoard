from fastapi.testclient import TestClient

from app.api.routes import incidents as incidents_module
from app.main import app


client = TestClient(app)


def setup_function():
    incidents_module.incidents.clear()


def create_incident():
    return client.post(
        "/incidents",
        json={
            "id": 1,
            "title": "Network outage",
            "description": "Switch unreachable",
            "status": "open",
            "created_at": "2026-04-24T10:00:00",
        },
    )


def test_create_incident():
    response = create_incident()

    assert response.status_code == 200

    body = response.json()
    assert body["status"] == "success"
    assert body["incident"]["id"] == 0
    assert body["incident"]["title"] == "Network outage"
    assert body["incident"]["description"] == "Switch unreachable"
    assert body["incident"]["status"] == "open"


def test_list_incidents():
    create_incident()

    response = client.get("/incidents")

    assert response.status_code == 200

    body = response.json()
    assert body["status"] == "success"
    assert len(body["incidents"]) == 1
    assert body["incidents"][0]["title"] == "Network outage"


def test_update_incident_status():
    created = create_incident().json()
    incident_id = created["incident"]["id"]

    response = client.patch(
        "/incidents",
        json={
            "id": incident_id,
            "status": "in_progress",
        },
    )

    assert response.status_code == 200

    body = response.json()
    assert body["status"] == "success"
    assert body["incident"]["id"] == incident_id
    assert body["incident"]["status"] == "in_progress"


def test_delete_incident():
    created = create_incident().json()
    incident_id = created["incident"]["id"]

    response = client.request(
        "DELETE",
        "/incidents",
        json={
            "id": incident_id,
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "success"

    list_response = client.get("/incidents")
    assert list_response.status_code == 200
    assert list_response.json()["incidents"] == []


def test_update_rejects_invalid_status():
    response = client.patch(
        "/incidents",
        json={
            "id": 0,
            "status": "closed",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Invalid Incident Status"


def test_update_returns_not_found_for_missing_incident():
    response = client.patch(
        "/incidents",
        json={
            "id": 999,
            "status": "resolved",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Incident not found"
