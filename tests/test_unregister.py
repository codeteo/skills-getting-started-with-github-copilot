def test_unregister_removes_participant(client):
    activities_before = client.get("/activities").json()
    before_count = len(activities_before["Chess Club"]["participants"])

    response = client.delete(
        "/activities/Chess%20Club/participants", params={"email": "michael@mergington.edu"}
    )

    assert response.status_code == 200
    assert "Removed" in response.json()["message"]

    activities_after = client.get("/activities").json()
    participants_after = activities_after["Chess Club"]["participants"]
    assert len(participants_after) == before_count - 1
    assert "michael@mergington.edu" not in participants_after


def test_unregister_returns_not_found_for_unknown_activity(client):
    response = client.delete(
        "/activities/Unknown%20Club/participants", params={"email": "student@mergington.edu"}
    )

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_unregister_rejects_non_participant(client):
    response = client.delete(
        "/activities/Chess%20Club/participants", params={"email": "absent@mergington.edu"}
    )

    assert response.status_code == 404
    assert "not signed up" in response.json()["detail"].lower()


def test_unregister_requires_email(client):
    response = client.delete("/activities/Chess%20Club/participants")

    assert response.status_code == 422
