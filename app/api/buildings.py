from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.exceptions import BuildingNotFound
from app.db.session import get_db_session
from app.schemas.buildings import BuildingOut, BuildingCreate, BuildingUpdate
from app.crud.buildings import BuildingCRUD

router = APIRouter(
    prefix="/buildings",
    tags=["Здания"],
)


@router.post(
    "/",
    response_model=BuildingOut,
    summary="Создать здание",
    description="""
Создаёт новое здание.

Аргументы тела запроса:
- address (str): Адрес здания.
- latitude (float, optional): Широта.
- longitude (float, optional): Долгота.
""",
    responses={
        200: {
            "description": "Созданное здание",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "address": "ул. Ленина, 1",
                        "latitude": 55.7558,
                        "longitude": 37.6173
                    }
                }
            },
        }
    },
)
async def create_building(building_in: BuildingCreate, db: AsyncSession = Depends(get_db_session)):
    return await BuildingCRUD.create(db, building_in)


@router.get(
    "/",
    response_model=List[BuildingOut],
    summary="Получить список зданий",
    description="""
Возвращает список всех зданий.

Параметры запроса (необязательные):
- address (str): Фильтр по адресу здания.
""",
    responses={
        200: {
            "description": "Список зданий",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "address": "ул. Ленина, 1",
                            "latitude": 55.7558,
                            "longitude": 37.6173
                        },
                        {
                            "id": 2,
                            "address": "Невский пр., 10",
                            "latitude": 59.9311,
                            "longitude": 30.3609
                        }
                    ]
                }
            },
        }
    },
)
async def list_buildings(
        address: str | None = Query(None, description="Фильтр по адресу здания"),
        db: AsyncSession = Depends(get_db_session),
):
    return await BuildingCRUD.get_list(db, address=address)


@router.get(
    "/{building_id}",
    response_model=BuildingOut,
    summary="Получить здание по ID",
    description="""
Возвращает здание по уникальному ID.
""",
    responses={
        200: {
            "description": "Здание",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "address": "ул. Ленина, 1",
                        "latitude": 55.7558,
                        "longitude": 37.6173
                    }
                }
            },
        },
        404: {
            "description": "Здание не найдено",
            "content": {
                "application/json": {
                    "example": {"detail": "Здание не найдено"}
                }
            },
        },
    },
)
async def get_building(
        building_id: int = Path(..., description="ID здания"),
        db: AsyncSession = Depends(get_db_session)
):
    building = await BuildingCRUD.get(db, building_id)
    if not building:
        raise BuildingNotFound
    return building


@router.put(
    "/{building_id}",
    response_model=BuildingOut,
    summary="Обновить здание",
    description="""
Обновляет здание по его ID.

Аргументы тела запроса:
- address (str, optional): Новый адрес здания.
- latitude (float, optional): Новая широта.
- longitude (float, optional): Новая долгота.
""",
    responses={
        200: {
            "description": "Обновлённое здание",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "address": "ул. Ленина, 1",
                        "latitude": 55.7558,
                        "longitude": 37.6173
                    }
                }
            },
        },
        404: {
            "description": "Здание не найдено",
            "content": {
                "application/json": {
                    "example": {"detail": "Здание не найдено"}
                }
            },
        },
    },
)
async def update_building(
        building_in: BuildingUpdate,
        building_id: int = Path(..., description="ID здания"),
        db: AsyncSession = Depends(get_db_session)
):
    building = await BuildingCRUD.update(db, building_id, building_in)
    if not building:
        raise BuildingNotFound
    return building


@router.delete(
    "/{building_id}",
    summary="Удалить здание",
    description="""
Удаляет здание по его ID.
""",
    responses={
        200: {
            "description": "Успешное удаление",
            "content": {
                "application/json": {
                    "example": {"detail": "Здание удалено"}
                }
            },
        },
        404: {
            "description": "Здание не найдено",
            "content": {
                "application/json": {
                    "example": {"detail": "Здание не найдено"}
                }
            },
        },
    },
)
async def delete_building(
        building_id: int = Path(..., description="ID здания"),
        db: AsyncSession = Depends(get_db_session)
):
    success = await BuildingCRUD.delete(db, building_id)
    if not success:
        raise BuildingNotFound
    return {"detail": "Здание удалено"}
