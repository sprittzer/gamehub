import uuid
from typing import List, Optional

from fastapi import APIRouter, File, HTTPException, Query, UploadFile
from postgrest.exceptions import APIError

from app.core.database import (
    delete_game,
    get_all_genres,
    get_all_platforms,
    get_game,
    get_games,
    get_recent_games,
    get_top_games,
    supabase,
    update_game,
)
from app.schemas.game import (
    GameCreate,
    GameDetailResponse,
    GameFilter,
    GameListResponse,
    GameResponse,
    GameUpdate,
)

router = APIRouter(prefix="/games", tags=["Игры"])


@router.get("/top", response_model=List[GameResponse])
async def get_top_games_handler(limit: int = Query(10, ge=1, le=50)):
    return await get_top_games(limit)


@router.get("/recent", response_model=List[GameResponse])
async def get_recent_games_handler(limit: int = Query(10, ge=1, le=50)):
    return await get_recent_games(limit)


@router.get("/genres", response_model=List[str])
async def get_all_genres_handler():
    return await get_all_genres()


@router.get("/platforms", response_model=List[str])
async def get_all_platforms_handler():
    return await get_all_platforms()


@router.get("", response_model=GameListResponse)
async def list_games(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    q: Optional[str] = None,
    genres: Optional[str] = None,
    platforms: Optional[str] = None,
    developer: Optional[str] = None,
    min_year: Optional[int] = None,
    max_year: Optional[int] = None,
    min_rating: Optional[float] = None,
    max_rating: Optional[float] = None,
):
    genres_list = (
        [x.strip() for x in genres.split(",") if x.strip()] if genres else None
    )
    platforms_list = (
        [x.strip() for x in platforms.split(",") if x.strip()] if platforms else None
    )

    filter_obj = GameFilter(
        q=q,
        genres=genres_list,
        platforms=platforms_list,
        developer=developer,
        min_year=min_year,
        max_year=max_year,
        min_rating=min_rating,
        max_rating=max_rating,
    )

    games, total = await get_games(page, page_size, filter_obj)

    return GameListResponse(
        items=games,
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size,
    )


@router.get("/{game_id}", response_model=GameDetailResponse)
async def get_game_handler(game_id: int):
    game = await get_game(game_id)

    reviews_response = (
        supabase.table("reviews")
        .select("count", count="exact")
        .eq("game_id", game_id)
        .execute()
    )

    return {**game, "reviews_count": reviews_response.count or 0}


@router.post("", response_model=GameResponse, status_code=201)
async def create_game_handler(game: GameCreate):
    existing = (
        supabase.table("games")
        .select("id")
        .eq("title", game.title)
        .maybe_single()
        .execute()
    )

    if existing:
        raise HTTPException(
            status_code=409, detail="Игра с таким названием уже существует"
        )

    try:
        response = supabase.table("games").insert(game.model_dump()).execute()

        if not response.data:
            raise HTTPException(status_code=500, detail="Не удалось создать игру")

        return response.data[0]

    except APIError as e:
        if e.code == "23505":
            raise HTTPException(
                status_code=409, detail="Игра с таким названием уже существует"
            )
        raise HTTPException(status_code=422, detail="Ошибка валидации данных")

    except Exception:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.patch("/{game_id}/cover", response_model=dict, status_code=200)
async def update_game_cover(game_id: int, cover_image: UploadFile = File(...)):
    game = (
        supabase.table("games")
        .select("id,title")
        .eq("id", game_id)
        .maybe_single()
        .execute()
    )
    if not game:
        raise HTTPException(status_code=404, detail="Игра не найдена")

    file_extension = cover_image.filename.split(".")[-1].lower()
    if file_extension not in ["jpg", "jpeg", "png", "webp"]:
        raise HTTPException(
            status_code=422, detail="Поддерживаемые форматы: jpg, png, webp"
        )

    file_path = f"covers/{uuid.uuid4()}.{file_extension}"
    file_content = await cover_image.read()

    upload_result = supabase.storage.from_("game-covers").upload(
        file_path,
        file_content,
        {"content-type": cover_image.content_type or "image/jpeg"},
    )

    if not upload_result:
        raise HTTPException(status_code=500, detail="Ошибка загрузки обложки")

    cover_path = (
        supabase.storage.from_("game-covers").get_public_url(file_path).rstrip("/")
    )

    supabase.table("games").update({"cover_image_path": cover_path}).eq(
        "id", game_id
    ).execute()

    return {"cover_image_path": cover_path, "game_id": game_id}


@router.patch("/{game_id}", response_model=GameResponse)
async def update_game_handler(game_id: int, game_data: GameUpdate):
    return await update_game(game_id, game_data)


@router.delete("/{game_id}", status_code=204)
async def delete_game_handler(game_id: int):
    await delete_game(game_id)
    return None
