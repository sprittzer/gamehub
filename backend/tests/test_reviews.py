from unittest.mock import patch


def test_get_all_reviews(client):
    response = client.get("/api/v1/reviews?page=1&page_size=5")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data


def test_get_recent_reviews(client):
    response = client.get("/api/v1/reviews/recent?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 5
    assert all("games" in review for review in data)


def test_get_review_complete(client):
    response = client.get("/api/v1/reviews/999")
    assert response.status_code == 404
    assert "Рецензия не найдена" in response.json()["detail"]

    with patch("fastapi.Request.client") as mock_client:
        mock_client.host = "127.0.0.1"

        review_data = {
            "game_id": 1,
            "rating": 9,
            "text": "Отличная игра с полной поддержкой!",
        }
        review_resp = client.post("/api/v1/reviews", json=review_data)
        assert review_resp.status_code == 201
        review_id = review_resp.json()["id"]

        response = client.get(f"/api/v1/reviews/{review_id}")
        assert response.status_code == 200
        data = response.json()

        assert data["id"] == review_id
        assert data["rating"] == 9
        assert data["text"] == "Отличная игра с полной поддержкой!"
        assert "games" in data
        assert data["games"]["id"] == 1

        delete_resp = client.delete(f"/api/v1/reviews/{review_id}")
        assert delete_resp.status_code == 204

        get_resp = client.get(f"/api/v1/reviews/{review_id}")
        assert get_resp.status_code == 404


def test_review_crud_complete(client):
    game_data = {
        "title": "CRUD Test Game",
        "release_year": 2024,
        "genres": ["RPG"],
        "platforms": ["PC"],
    }
    game_resp = client.post("/api/v1/games", json=game_data)
    game_id = game_resp.json()["id"]

    with patch("fastapi.Request.client") as mock_client:
        mock_client.host = "127.0.0.1"

        review_data = {"game_id": game_id, "rating": 5, "text": "Начальный отзыв"}
        create_resp = client.post("/api/v1/reviews", json=review_data)
        review_id = create_resp.json()["id"]

        update_data = {"rating": 9, "text": "Обновленный отзыв! Лучшая игра!"}
        update_resp = client.patch(f"/api/v1/reviews/{review_id}", json=update_data)
        assert update_resp.status_code == 200
        assert update_resp.json()["rating"] == 9

        delete_resp = client.delete(f"/api/v1/reviews/{review_id}")
        assert delete_resp.status_code == 204

        get_resp = client.get(f"/api/v1/reviews/{review_id}")
        assert get_resp.status_code == 404

    delete_game_resp = client.delete(f"/api/v1/games/{game_id}")
    assert delete_game_resp.status_code == 204


def test_get_game_reviews(client):
    non_exist_resp = client.get("/api/v1/reviews/game/999")
    assert non_exist_resp.status_code == 404
    assert "Игра не найдена" in non_exist_resp.json()["detail"]

    response = client.get("/api/v1/reviews/game/1")
    assert response.status_code == 200
    data = response.json()

    assert data["game_id"] == 1
    assert "game_title" in data
    assert isinstance(data["reviews_count"], int)
    assert isinstance(data["items"], list)
    assert all("games" in review for review in data["items"])
