def test_get_activities_returns_expected_shape(client):
    response = client.get("/activities")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

    chess_club = data["Chess Club"]
    assert {"description", "schedule", "max_participants", "participants"}.issubset(chess_club.keys())
    assert isinstance(chess_club["description"], str)
    assert isinstance(chess_club["schedule"], str)
    assert isinstance(chess_club["max_participants"], int)
    assert isinstance(chess_club["participants"], list)
