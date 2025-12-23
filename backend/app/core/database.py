from typing import Any, Dict

from tortoise import Tortoise

from app.core.config import settings

TORTOISE_ORM: Dict[str, Any] = {
    "connections": {
        "default": settings.DATABASE_URL,
    },
    "apps": {
        "models": {
            "models": ["app.models"],
            "default_connection": "default",
        },
    },
    "use_tz": True,
    "timezone": "UTC",
}


async def init_db() -> None:
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas(safe=False)


async def close_db() -> None:
    await Tortoise.close_connections()
