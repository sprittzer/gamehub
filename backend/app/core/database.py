from typing import Dict, List

from fastapi import HTTPException
from supabase import Client, create_client

from app.core.config import settings
from app.schemas.game import GameFilter, GameUpdate

supabase: Client = create_client(
    supabase_url=settings.SUPABASE_URL,
    supabase_key=settings.SUPABASE_KEY,
)


async def get_games(
    page: int = 1, page_size: int = 10, filter_obj: GameFilter = None
) -> tuple[list[dict], int]:
    offset = (page - 1) * page_size

    query = supabase.table("games").select("*", count="exact").order("id")

    if filter_obj:
        if filter_obj.q:
            query = query.or_(
                f"title.ilike.%{filter_obj.q}%,description.ilike.%{filter_obj.q}%"
            )
        if filter_obj.genres:
            query = query.contains("genres", filter_obj.genres)
        if filter_obj.platforms:
            query = query.contains("platforms", filter_obj.platforms)
        if filter_obj.developer:
            query = query.ilike("developer", f"%{filter_obj.developer}%")
        if filter_obj.min_rating is not None:
            query = query.gte("average_rating", filter_obj.min_rating)
        if filter_obj.max_rating is not None:
            query = query.lte("average_rating", filter_obj.max_rating)
        if filter_obj.min_year is not None:
            query = query.gte("release_year", filter_obj.min_year)
        if filter_obj.max_year is not None:
            query = query.lte("release_year", filter_obj.max_year)

    total_response = query.execute()
    total_count = total_response.count or 0

    data_response = query.range(offset, offset + page_size - 1).execute()
    items = data_response.data or []

    return items, total_count


async def get_game(game_id: int) -> Dict:
    response = (
        supabase.table("games").select("*").eq("id", game_id).maybe_single().execute()
    )
    if not response:
        raise HTTPException(status_code=404, detail="Игра не найдена")
    return response.data


async def update_game(game_id: int, game_data: GameUpdate) -> Dict:
    data = game_data.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(400, "Нет данных для обновления")

    response = supabase.table("games").update(data).eq("id", game_id).execute()
    if not response.data:
        raise HTTPException(404, "Игра не найдена")
    return response.data[0]


async def delete_game(game_id: int) -> bool:
    await get_game(game_id)
    response = supabase.table("games").delete().eq("id", game_id).execute()
    return bool(response.data)


async def update_game_average_rating(game_id: int) -> None:
    response = (
        supabase.table("reviews")
        .select("rating", count="exact")
        .eq("game_id", game_id)
        .execute()
    )

    if response.count and response.count > 0:
        ratings = [r["rating"] for r in response.data]
        avg_rating = round(sum(ratings) / len(ratings), 1)
        supabase.table("games").update({"average_rating": avg_rating}).eq(
            "id", game_id
        ).execute()
    else:
        supabase.table("games").update({"average_rating": 0.0}).eq(
            "id", game_id
        ).execute()


async def get_top_games(limit: int = 10) -> List[Dict]:
    response = (
        supabase.table("games")
        .select("*", count="exact")
        .order("average_rating", desc=True)
        .limit(limit)
        .execute()
    )
    return response.data


async def get_recent_games(limit: int = 10) -> List[Dict]:
    response = (
        supabase.table("games")
        .select("*", count="exact")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return response.data


async def get_all_genres() -> List[str]:
    response = supabase.table("games").select("genres").execute()
    genres = set()
    for game in response.data:
        genres.update(game.get("genres", []))
    return sorted(list(genres))


async def get_all_platforms() -> List[str]:
    response = supabase.table("games").select("platforms").execute()
    platforms = set()
    for game in response.data:
        platforms.update(game.get("platforms", []))
    return sorted(list(platforms))
