from uuid import uuid4

from fastapi.testclient import TestClient

from app.db.database import get_connection
from app.main import app


client = TestClient(app)


def setup_function():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                delete from incidents
                where user_id in (
                    select id from users where email like %s
                )
                """,
                ("%@example.test",),
            )
            cur.execute(
                """
                delete from users
                where email like %s
                """,
                ("%@example.test",),
            )


def auth_headers():
    email = f"test-{uuid4()}@example.test"
    password = "secret123"

    register_response = client.post(
        "/register",
        json={
            "email": email,
            "password_plaintext": password,
        },
    )
    assert register_response.status_code == 200

    login_response = client.post(
        "/login",
        json={
            "email": email,
            "password_plaintext": password,
        },
    )
    assert login_response.status_code == 200

    body = login_response.json()
    return {
        "Authorization": f"Bearer {body['access_token']}",
    }, body["user"]


def create_incident(headers, title="Network outage"):
    return client.post(
        "/incidents",
        headers=headers,
        json={
            "id": 1,
            "title": title,
            "description": "Switch unreachable",
            "status": "open",
            "created_at": "2026-04-24T10:00:00",
        },
    )


def test_create_incident():
    headers, user = auth_headers()

    response = create_incident(headers)

    assert response.status_code == 200

    body = response.json()
    assert body["status"] == "success"
    assert isinstance(body["incident"]["id"], int)
    assert body["incident"]["title"] == "Network outage"
    assert body["incident"]["description"] == "Switch unreachable"
    assert body["incident"]["status"] == "open"
    assert body["incident"]["user_id"] == user["id"]


def test_list_incidents():
    headers, _ = auth_headers()
    create_incident(headers)

    response = client.get("/incidents", headers=headers)

    assert response.status_code == 200

    body = response.json()
    assert body["status"] == "success"
    assert len(body["incidents"]) == 1
    assert body["incidents"][0]["title"] == "Network outage"


def test_update_incident_status():
    headers, _ = auth_headers()
    created = create_incident(headers).json()
    incident_id = created["incident"]["id"]

    response = client.patch(
        "/incidents",
        headers=headers,
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
    headers, _ = auth_headers()
    created = create_incident(headers).json()
    incident_id = created["incident"]["id"]

    response = client.request(
        "DELETE",
        "/incidents",
        headers=headers,
        json={
            "id": incident_id,
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "success"

    list_response = client.get("/incidents", headers=headers)
    assert list_response.status_code == 200
    assert list_response.json()["incidents"] == []


def test_user_cannot_manage_another_users_incident():
    owner_headers, _ = auth_headers()
    other_headers, _ = auth_headers()
    created = create_incident(owner_headers, title="Private incident").json()
    incident_id = created["incident"]["id"]

    list_response = client.get("/incidents", headers=other_headers)
    assert list_response.status_code == 200
    assert list_response.json()["incidents"] == []

    update_response = client.patch(
        "/incidents",
        headers=other_headers,
        json={
            "id": incident_id,
            "status": "resolved",
        },
    )
    assert update_response.status_code == 404

    delete_response = client.request(
        "DELETE",
        "/incidents",
        headers=other_headers,
        json={
            "id": incident_id,
        },
    )
    assert delete_response.status_code == 404


def test_update_rejects_invalid_status():
    headers, _ = auth_headers()
    response = client.patch(
        "/incidents",
        headers=headers,
        json={
            "id": 0,
            "status": "closed",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Invalid Incident Status"


def test_update_returns_not_found_for_missing_incident():
    headers, _ = auth_headers()
    response = client.patch(
        "/incidents",
        headers=headers,
        json={
            "id": 999999,
            "status": "resolved",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Incident not found"
