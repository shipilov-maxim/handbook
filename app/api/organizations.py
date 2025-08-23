from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from starlette import status

from app.core.exceptions import OrganizationNotFound
from app.db.session import get_db_session
from app.schemas.organizations import OrganizationCreate, OrganizationUpdate, OrganizationOut
from app.crud.organizations import OrganizationCRUD

router = APIRouter(
    prefix="/organizations",
    tags=["Организацыыыы"]
)


@router.get(
    "/",
    response_model=List[OrganizationOut],
    summary="Получить список организаций",
    description="""
Возвращает список организаций с возможностью фильтрации по:
- названию (`name`)
- зданию (`building_id`)
- виду деятельности (`activity_id`)
- координатам и радиусу поиска (`lat`, `lon`, `radius_km`)

Если фильтры не указаны, возвращаются все организации.
    """,
    responses={
        200: {
            "description": "Список организаций",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "name": "ООО Ромашка",
                            "building_id": 12,
                            "activity_id": 3,
                            "latitude": 55.7558,
                            "longitude": 37.6176
                        }
                    ]
                }
            }
        },
        401: {"description": "Неавторизован (отсутствует или неверный API-ключ)"}
    }
)
async def get_organizations(
        name: str | None = Query(None, description="Название организации для поиска"),
        building_id: int | None = Query(None, description="ID здания"),
        activity_id: int | None = Query(None, description="ID вида деятельности"),
        lat: float | None = Query(None, description="Широта для геопоиска"),
        lon: float | None = Query(None, description="Долгота для геопоиска"),
        radius_km: int | None = Query(None, description="Радиус поиска в км"),
        db: AsyncSession = Depends(get_db_session),
):
    return await OrganizationCRUD.get_list(
        db=db,
        name=name,
        building_id=building_id,
        activity_id=activity_id,
        lat=lat,
        lon=lon,
        radius_km=radius_km,
    )


@router.get(
    "/{org_id}",
    response_model=OrganizationOut,
    summary="Получить организацию по ID",
    description="""
Возвращает организацию по уникальному ID.
""",
    responses={
        200: {"description": "Информация об организации"},
        404: {"description": "Организация не найдена"}
    }
)
async def get_organization(
        org_id: int = Path(..., description="ID организации"),
        db: AsyncSession = Depends(get_db_session)
):
    org = await OrganizationCRUD.get(db, org_id)
    if not org:
        raise OrganizationNotFound
    return org


@router.post(
    "/",
    response_model=OrganizationOut,
    summary="Создать организацию",
    description="""
Создать новую организацию.

Аргументы тела запроса:
- name (str): Название организацию.
- phones (List[str]): Список контактных телефонов.
- building_id (int): ID здания.
- activity_id (List[int]): Список ID деятельностей.
""",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Организация успешно создана"},
        400: {"description": "Неверные данные"}
    }
)
async def create_organization(org_in: OrganizationCreate, db: AsyncSession = Depends(get_db_session)):
    return await OrganizationCRUD.create(db, org_in)


@router.put(
    "/{org_id}",
    response_model=OrganizationOut,
    summary="Обновить данные организации",
    responses={
        200: {"description": "Организация обновлена"},
        404: {"description": "Организация не найдена"}
    }
)
async def update_organization(
        org_in: OrganizationUpdate,
        org_id: int = Path(..., description="ID организации"),
        db: AsyncSession = Depends(get_db_session)
):
    org = await OrganizationCRUD.update(db, org_id, org_in)
    if not org:
        raise OrganizationNotFound
    return org


@router.delete(
    "/{org_id}",
    summary="Удалить организацию",
    responses={
        200: {
            "description": "Успешное удаление",
            "content": {
                "application/json": {
                    "example": {"detail": "Организация удалена"}
                }
            }
        },
        404: {
            "description": "Деятельность не найдена",
            "content": {
                "application/json": {
                    "example": {"detail": "Организация не найдена"}
                }
            }
        },
    }
)
async def delete_organization(
        org_id: int = Path(..., description="ID организации"),
        db: AsyncSession = Depends(get_db_session)
):
    success = await OrganizationCRUD.delete(db, org_id)
    if not success:
        raise OrganizationNotFound
    return {"detail": "Организация удалена"}
