def test_signup_adds_participant(client):
    activities_before = client.get("/activities").json()
    before_count = len(activities_before["Chess Club"]["participants"])

    response = client.post("/activities/Chess%20Club/signup", params={"email": "newstudent@mergington.edu"})

    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

    activities_after = client.get("/activities").json()
    participants_after = activities_after["Chess Club"]["participants"]
    assert len(participants_after) == before_count + 1
    assert "newstudent@mergington.edu" in participants_after


def test_signup_rejects_duplicate_participant(client):
    response = client.post(
        "/activities/Chess%20Club/signup", params={"email": "michael@mergington.edu"}
    )

    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_returns_not_found_for_unknown_activity(client):
    response = client.post(
        "/activities/Unknown%20Club/signup", params={"email": "student@mergington.edu"}
    )

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_signup_requires_email(client):
    response = client.post("/activities/Chess%20Club/signup")

    assert response.status_code == 422
