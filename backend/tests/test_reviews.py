# import pytest
# from httpx import Request

# def test_get_all_reviews_pagination(client):
#     """Тест пагинации на существующих рецензиях"""
#     # Тест 1: Первая страница
#     response = client.get("/api/v1/reviews?page=1&page_size=10")
#     assert response.status_code == 200
#     data = response.json()
#     assert "items" in data
#     assert "total" in data
#     assert data["page"] == 1
#     assert data["page_size"] == 10
#     assert isinstance(data["pages"], int)
    
#     # Тест 2: Вторая страница
#     response = client.get("/api/v1/reviews?page=2&page_size=10")
#     assert response.status_code == 200
#     data = response.json()
#     assert data["page"] == 2
    
#     # Тест 3: Разный page_size
#     response = client.get("/api/v1/reviews?page=1&page_size=5")
#     assert response.status_code == 200
#     data = response.json()
#     assert data["page_size"] == 5
    
#     # Тест 4: Большая страница (может быть пустой)
#     response = client.get("/api/v1/reviews?page=10&page_size=5")
#     assert response.status_code == 200

# def test_get_all_reviews_validation(client):
#     """Тест валидации параметров"""
#     # Неверный page
#     response = client.get("/api/v1/reviews?page=0")
#     assert response.status_code == 422
    
#     # Неверный page_size
#     response = client.get("/api/v1/reviews?page_size=0")
#     assert response.status_code == 422
    
#     # Слишком большой page_size
#     response = client.get("/api/v1/reviews?page_size=200")
#     assert response.status_code == 422
    
#     # Не число
#     response = client.get("/api/v1/reviews?page=abc")
#     assert response.status_code == 422
