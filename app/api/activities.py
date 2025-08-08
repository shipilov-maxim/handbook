from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.exceptions import ActivityNotFound
from app.db.session import get_db_session
from app.schemas.activities import ActivityCreate, ActivityRead, ActivityUpdate, ActivityWithChildren
from app.crud.activities import ActivityCRUD

router = APIRouter(
    prefix="/activities",
    tags=["Деятельности"],
)


@router.post(
    "/",
    response_model=ActivityRead,
    summary="Создать деятельность",
    description="""
Создаёт новую деятельность.

Аргументы тела запроса:
- name (str): Название деятельности.
- parent_id (int, optional): ID родительской деятельности. Если отсутствует, считается корневая деятельность.
""",
    responses={
        200: {
            "description": "Созданная деятельность",
            "content": {
                "application/json": {
                    "example": {
                        "id": 10,
                        "name": "Разработка ПО",
                        "parent_id": None
                    }
                }
            },
        }
    },
)
async def create_activity(activity_in: ActivityCreate, db: AsyncSession = Depends(get_db_session)):
    return await ActivityCRUD.create(db, activity_in)


@router.get(
    "/",
    response_model=List[ActivityRead],
    summary="Получить список деятельностей",
    description="""
Возвращает список всех деятельностей (плоский список).
""",
    responses={
        200: {
            "description": "Список деятельностей",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "name": "Медицина",
                            "parent_id": None
                        },
                        {
                            "id": 2,
                            "name": "Стоматология",
                            "parent_id": 1
                        }
                    ]
                }
            }
        }
    },
)
async def list_activities(db: AsyncSession = Depends(get_db_session)):
    return await ActivityCRUD.get_all(db)


@router.get(
    "/tree",
    response_model=List[ActivityWithChildren],
    summary="Получить дерево деятельностей",
    description="""
Возвращает иерархическое дерево деятельностей с вложенными дочерними элементами.
""",
    responses={
        200: {
            "description": "Дерево деятельностей",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "name": "Медицина",
                            "parent_id": None,
                            "children": [
                                {
                                    "id": 2,
                                    "name": "Стоматология",
                                    "parent_id": 1,
                                    "children": []
                                }
                            ]
                        }
                    ]
                }
            }
        }
    },
)
async def get_activity_tree(db: AsyncSession = Depends(get_db_session)):
    return await ActivityCRUD.get_hierarchical(db)


@router.get(
    "/{activity_id}",
    response_model=ActivityRead,
    summary="Получить деятельность по ID",
    description="""
Возвращает деятельность по уникальному ID.
""",
    responses={
        200: {
            "description": "Деятельность",
            "content": {
                "application/json": {
                    "example": {
                        "id": 2,
                        "name": "Стоматология",
                        "parent_id": 1
                    }
                }
            },
        },
        404: {
            "description": "Деятельность не найдена",
            "content": {
                "application/json": {
                    "example": {"detail": "Деятельность не найдена"}
                }
            },
        },
    },
)
async def get_activity(
        activity_id: int = Path(..., description="ID деятельности"),
        db: AsyncSession = Depends(get_db_session)
):
    activity = await ActivityCRUD.get(db, activity_id)
    if not activity:
        raise ActivityNotFound
    return activity


@router.put(
    "/{activity_id}",
    response_model=ActivityRead,
    summary="Обновить деятельность",
    description="""
Обновляет деятельность по её ID.

Аргументы тела запроса:
- name (str, optional): Новое название деятельности.
- parent_id (int, optional): Новый ID родительской деятельности.
""",
    responses={
        200: {
            "description": "Обновлённая деятельность",
            "content": {
                "application/json": {
                    "example": {
                        "id": 2,
                        "name": "Обновлённое имя",
                        "parent_id": None
                    }
                }
            }
        },
        404: {
            "description": "Деятельность не найдена",
            "content": {
                "application/json": {
                    "example": {"detail": "Деятельность не найдена"}
                }
            },
        },
    },
)
async def update_activity(
        activity_in: ActivityUpdate,
        activity_id: int = Path(..., description="ID деятельности"),
        db: AsyncSession = Depends(get_db_session)
):
    activity = await ActivityCRUD.update(db, activity_id, activity_in)
    if not activity:
        raise ActivityNotFound
    return activity


@router.delete(
    "/{activity_id}",
    summary="Удалить деятельность",
    description="""
Удаляет деятельность по её ID.
""",
    responses={
        200: {
            "description": "Успешное удаление",
            "content": {
                "application/json": {
                    "example": {"detail": "Деятельность удалена"}
                }
            }
        },
        404: {
            "description": "Деятельность не найдена",
            "content": {
                "application/json": {
                    "example": {"detail": "Деятельность не найдена"}
                }
            }
        },
    },
)
async def delete_activity(
        activity_id: int = Path(..., description="ID деятельности"),
        db: AsyncSession = Depends(get_db_session)
):
    success = await ActivityCRUD.delete(db, activity_id)
    if not success:
        raise ActivityNotFound
    return {"detail": "Деятельность удалена"}
