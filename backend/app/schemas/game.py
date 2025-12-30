from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, validator


class GameBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Название игры",
        examples=["The Witcher 3: Wild Hunt"],
    )
    description: Optional[str] = Field(
        None,
        description="Описание игры",
        examples=["Эпическая ролевая игра в открытом мире..."],
    )
    genres: List[str] = Field(
        default_factory=list,
        description="Список жанров игры",
        examples=[["RPG", "Action", "Open World"]],
    )
    developer: Optional[str] = Field(
        None,
        max_length=255,
        description="Разработчик игры",
        examples=["CD Projekt Red"],
    )
    publisher: Optional[str] = Field(
        None,
        max_length=255,
        description="Издатель игры",
        examples=["CD Projekt"],
    )
    release_year: int = Field(
        ...,
        ge=1900,
        le=2030,
        description="Год выхода игры",
        examples=[2015],
    )
    platforms: List[str] = Field(
        default_factory=list,
        description="Платформы, на которых доступна игра",
        examples=[["PC", "PS4", "Xbox One", "Nintendo Switch"]],
    )
    cover_image_path: Optional[str] = Field(
        None,
        max_length=512,
        description="Путь к обложке",
        examples=["images/image.png"],
    )
    average_rating: float = Field(
        0.0,
        ge=0,
        le=10,
        description="Средний рейтинг",
        examples=[8.5],
    )


class GameCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Название игры",
        examples=["The Witcher 3: Wild Hunt"],
    )
    description: Optional[str] = Field(
        None,
        description="Описание игры",
        examples=["Эпическая ролевая игра в открытом мире..."],
    )
    genres: List[str] = Field(
        default_factory=list,
        description="Список жанров игры",
        examples=[["RPG", "Action", "Open World"]],
    )
    developer: Optional[str] = Field(
        None,
        max_length=255,
        description="Разработчик игры",
        examples=["CD Projekt Red"],
    )
    publisher: Optional[str] = Field(
        None,
        max_length=255,
        description="Издатель игры",
        examples=["CD Projekt"],
    )
    release_year: int = Field(
        ...,
        ge=1900,
        le=2030,
        description="Год выхода игры",
        examples=[2015],
    )
    platforms: List[str] = Field(
        default_factory=list,
        description="Платформы, на которых доступна игра",
        examples=[["PC", "PS4", "Xbox One", "Nintendo Switch"]],
    )
    average_rating: float = Field(
        0.0,
        ge=0,
        le=10,
        description="Средний рейтинг",
        examples=[8.5],
    )


class GameUpdate(BaseModel):
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="Название игры",
        examples=["Doom Eternal"],
    )
    description: Optional[str] = Field(
        None,
        description="Описание игры",
        examples=["Шутер от первого лица..."],
    )
    genres: Optional[List[str]] = Field(
        None,
        description="Список жанров игры",
        examples=[["shooter", "action", "fps"]],
    )
    developer: Optional[str] = Field(
        None,
        max_length=255,
        description="Разработчик игры",
        examples=["id Software"],
    )
    publisher: Optional[str] = Field(
        None,
        max_length=255,
        description="Издатель игры",
        examples=["Bethesda"],
    )
    release_year: Optional[int] = Field(
        None,
        ge=1900,
        le=2030,
        description="Год выхода игры",
        examples=[2020],
    )
    platforms: Optional[List[str]] = Field(
        None,
        description="Платформы игры",
        examples=[["PC", "PS5", "Xbox Series X"]],
    )
    cover_image_path: Optional[str] = Field(
        None,
        max_length=512,
        description="Путь к обложке игры",
        examples=["covers/doom_eternal.jpg"],
    )


class GameFilter(BaseModel):
    q: Optional[str] = None
    genres: Optional[List[str]] = None
    platforms: Optional[List[str]] = None
    developer: Optional[str] = None
    min_year: Optional[int] = None
    max_year: Optional[int] = None
    min_rating: Optional[float] = None
    max_rating: Optional[float] = None

    @validator("genres", "platforms", pre=True)
    def split_comma(cls, v):
        if isinstance(v, str):
            return [x.strip() for x in v.split(",") if x.strip()]
        return v


class GameResponse(GameBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="ID игры")
    average_rating: float = Field(
        ...,
        ge=0,
        le=10,
        description="Средний рейтинг игры",
    )
    created_at: datetime = Field(..., description="Дата добавления в каталог")


class GameListResponse(BaseModel):
    items: List[GameResponse] = Field(..., description="Список игр")
    total: int = Field(..., description="Общее количество игр")
    page: int = Field(..., ge=1, description="Текущая страница")
    page_size: int = Field(..., ge=1, description="Размер страницы")
    pages: int = Field(..., ge=0, description="Общее количество страниц")


class GameDetailResponse(GameResponse):
    reviews_count: int = Field(
        default=0,
        description="Количество рецензий на игру",
    )
