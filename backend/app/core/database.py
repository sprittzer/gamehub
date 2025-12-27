from typing import Dict, List

from fastapi import HTTPException
from supabase import Client, create_client

from app.core.config import settings
from app.schemas.game import GameCreate, GameFilter, GameUpdate

supabase: Client = create_client(
    supabase_url=settings.SUPABASE_URL,
    supabase_key=settings.SUPABASE_KEY,
)


async def get_games(
    page: int = 1, page_size: int = 10, filter_obj: GameFilter = None
) -> tuple[List[Dict], int]:
    offset = (page - 1) * page_size
    query = supabase.table("games").select("*", count="exact")

    if filter_obj:
        if filter_obj.q:
            query = query.or_(
                f"title.ilike.%%{filter_obj.q}%%,description.ilike.%%{filter_obj.q}%%"
            )
        if filter_obj.genres:
            query = query.contains("genres", [filter_obj.genres])
        if filter_obj.platforms:
            query = query.contains("platforms", [filter_obj.platforms])
        if filter_obj.developer:
            query = query.ilike("developer", f"%{filter_obj.developer}%")
        if filter_obj.publisher:
            query = query.ilike("publisher", f"%{filter_obj.publisher}%")
        if filter_obj.min_rating:
            query = query.gte("average_rating", filter_obj.min_rating)
        if filter_obj.max_rating:
            query = query.lte("average_rating", filter_obj.max_rating)
        if filter_obj.min_year:
            query = query.gte("release_year", filter_obj.min_year)
        if filter_obj.max_year:
            query = query.lte("release_year", filter_obj.max_year)

    total_response = query.execute()
    data_response = query.range(offset, offset + page_size - 1).execute()

    return data_response.data, total_response.count or 0


async def create_game(game_data: GameCreate) -> Dict:
    try:
        response = (
            await supabase.table("games").insert(game_data.model_dump()).execute()
        )
        return response.data[0]
    except Exception as e:
        raise HTTPException(400, f"Ошибка создания: {str(e)}")


async def get_game(game_id: int) -> Dict:
    response = (
        await supabase.table("games").select("*").eq("id", game_id).single().execute()
    )
    if not response.data:
        raise HTTPException(404, "Игра не найдена")
    return response.data


async def update_game(game_id: int, game_data: GameUpdate) -> Dict:
    data = game_data.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(400, "Нет данных для обновления")

    response = await supabase.table("games").update(data).eq("id", game_id).execute()
    if not response.data:
        raise HTTPException(404, "Игра не найдена")
    return response.data[0]


async def delete_game(game_id: int) -> bool:
    response = await supabase.table("games").delete().eq("id", game_id).execute()
    return bool(response.data)


async def update_game_average_rating(game_id: int) -> None:
    response = (
        await supabase.table("reviews")
        .select("avg(rating)", count="exact")
        .eq("game_id", game_id)
        .single()
        .execute()
    )

    if response.data and response.data.get("count", 0) > 0:
        avg_rating = round(float(response.data["avg"]), 1)
        await (
            supabase.table("games")
            .update({"average_rating": avg_rating})
            .eq("id", game_id)
            .execute()
        )
    else:
        await (
            supabase.table("games")
            .update({"average_rating": 0.0})
            .eq("id", game_id)
            .execute()
        )


async def get_game_detail(game_id: int) -> Dict:
    game = await get_game(game_id)
    reviews_count = (
        await supabase.table("reviews")
        .select("count", count="exact")
        .eq("game_id", game_id)
        .execute()
    )
    return {**game, "reviews_count": reviews_count.count or 0}


async def get_top_games(limit: int = 10) -> List[Dict]:
    response = (
        await supabase.table("games")
        .select("*")
        .gt("average_rating", 0)
        .order("average_rating", desc=True)
        .limit(limit)
        .execute()
    )
    return response.data


async def get_recent_games(limit: int = 10) -> List[Dict]:
    response = (
        await supabase.table("games")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return response.data


async def get_all_genres() -> List[str]:
    response = await supabase.table("games").select("genres").execute()
    genres = set()
    for game in response.data:
        genres.update(game.get("genres", []))
    return sorted(list(genres))


async def get_all_platforms() -> List[str]:
    response = await supabase.table("games").select("platforms").execute()
    platforms = set()
    for game in response.data:
        platforms.update(game.get("platforms", []))
    return sorted(list(platforms))
