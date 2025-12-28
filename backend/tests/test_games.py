def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "GameHub API"


def test_list_games(client):
    response = client.get("/api/v1/games?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data


def test_get_game_detail(client):
    response = client.get("/api/v1/games/1")
    assert response.status_code in [200, 404]
    assert "title" in response.json()

    response = client.get("/api/v1/games/1000")
    assert response.status_code == 404
    assert "Игра не найдена" in response.json()["detail"]


def test_create_game(client):
    game_data = {
        "title": "Test Game RPG",
        "release_year": 2024,
        "genres": ["RPG"],
        "platforms": ["PC"],
    }
    response = client.post("/api/v1/games", json=game_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Game RPG"
    assert "id" in data
    assert data["release_year"] == 2024

    no_title = {"release_year": 2024, "genres": ["Action"]}
    response = client.post("/api/v1/games", json=no_title)
    assert response.status_code == 422
    assert "title" in str(response.json()["detail"])

    empty_title = {"title": "", "release_year": 2024}
    response = client.post("/api/v1/games", json=empty_title)
    assert response.status_code == 422
    assert "title" in str(response.json()["detail"])

    duplicate_data = {"title": "Test Game RPG", "release_year": 2024, "genres": ["FPS"]}
    response = client.post("/api/v1/games", json=duplicate_data)
    assert response.status_code == 409
    assert "уже существует" in response.json()["detail"]

    invalid_year = {"title": "Bad Year", "release_year": 1800}
    response = client.post("/api/v1/games", json=invalid_year)
    assert response.status_code == 422


def test_update_game(client):
    game_response = client.get("/api/v1/games?page_size=100")
    games = game_response.json()["items"]
    test_game = next((g for g in games if g["title"] == "Test Game RPG"), None)
    assert test_game is not None, "Test Game RPG должна существовать"
    game_id = test_game["id"]

    update_data = {
        "title": "Test Game RPG Updated",
        "release_year": 2025,
        "genres": ["RPG", "Action"],
    }
    response = client.patch(f"/api/v1/games/{game_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Game RPG Updated"
    assert data["release_year"] == 2025

    response = client.patch("/api/v1/games/999", json=update_data)
    assert response.status_code == 404

    invalid_update = {"release_year": 1800}
    response = client.patch(f"/api/v1/games/{game_id}", json=invalid_update)
    assert response.status_code == 422


def test_delete_game(client):
    game_response = client.get("/api/v1/games?page_size=100")
    games = game_response.json()["items"]
    test_game = next((g for g in games if "Test Game RPG Updated" in g["title"]), None)
    assert test_game is not None, "Test Game RPG Updated должна существовать"
    game_id = test_game["id"]

    response = client.delete(f"/api/v1/games/{game_id}")
    assert response.status_code == 204

    response = client.get(f"/api/v1/games/{game_id}")
    assert response.status_code == 404

    response = client.delete("/api/v1/games/999")
    assert response.status_code == 404


def test_top_games(client):
    response = client.get("/api/v1/games/top?limit=5")
    assert response.status_code == 200


def test_recent_games(client):
    response = client.get("/api/v1/games/recent?limit=5")
    assert response.status_code == 200


def test_genres(client):
    response = client.get("/api/v1/games/genres")
    assert response.status_code == 200


def test_platforms(client):
    response = client.get("/api/v1/games/platforms")
    assert response.status_code == 200


def test_upload_cover(client):
    game_data = {
        "title": "Game With Cover Test",
        "release_year": 2024,
        "genres": ["RPG"],
        "platforms": ["PC"],
    }
    create_response = client.post("/api/v1/games", json=game_data)
    assert create_response.status_code == 201
    game_id = create_response.json()["id"]

    with open("tests/test_cover.jpg", "rb") as image_file:
        response = client.patch(
            f"/api/v1/games/{game_id}/cover",
            files={"cover_image": ("test_cover.jpg", image_file, "image/jpeg")},
        )

    assert response.status_code == 200
    data = response.json()
    assert "cover_image_path" in data
    assert "game_id" in data
    assert data["game_id"] == game_id
    assert data["cover_image_path"].startswith("https://")

    with open("tests/test_cover.jpg", "rb") as image_file:
        response = client.patch(
            "/api/v1/games/999/cover",
            files={"cover_image": ("test_cover.jpg", image_file, "image/jpeg")},
        )
    assert response.status_code == 404

    with open("tests/test_cover.jpg", "rb") as image_file:
        response = client.patch(
            f"/api/v1/games/{game_id}/cover",
            files={"cover_image": ("test_cover.txt", image_file, "text/plain")},
        )
    assert response.status_code == 422
    assert "Поддерживаемые форматы" in response.json()["detail"]
