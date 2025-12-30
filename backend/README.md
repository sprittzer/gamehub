# GameHub Backend

Бэкенд для GameHub — сервис для хранения и отображения информации об играх и рецензиях.  
Проект построен на **FastAPI** с использованием **Supabase** в качестве базы данных.

---

## Структура проекта
```python
backend/
├── app/
│ ├── api/v1/ # Роутеры (игры, рецензии)
│ ├── core/ # Подключение к базе, конфигурация
│ ├── schemas/ # Pydantic-модели
│ ├── services/ # Вспомогательные функции
│ └── main.py # Точка входа FastAPI
├── tests/ # Тесты на pytest
├── .env # Переменные окружения
├── pyproject.toml # Конфигурация Poetry и зависимости
└── poetry.lock # Зафиксированные версии зависимостей
```

---

## Установка

Проект использует **Poetry** для управления зависимостями.  

1. Клонируем репозиторий:

```bash
git clone https://github.com/sprittzer/gamehub
cd backend
git checkout backend
```

2. Устанавливаем зависимости:

```bash
poetry install
```

3. Создаём файл .env на основе примера:

```bash
cp .env.example .env
```

## Запуск сервера
Запуск через Uvicorn:

```python
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
``` 

- --reload — авто-перезагрузка при изменении кода (удобно для разработки)
- --host 0.0.0.0 — доступ снаружи (например в Docker)
- --port 8000 — порт API

Swagger UI: `https://0.0.0.0:8000/docs`

### Проверить код на ошибки
```python
poetry run ruff check .
```

### Автоисправить что можно
```python
poetry run ruff check --fix .
```

### Отформатировать код
```python
poetry run ruff format .
```

### Запустить тесты
```python
poetry run pytest
```
