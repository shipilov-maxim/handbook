from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.building import Building
from app.schemas.buildings import BuildingCreate, BuildingUpdate
from sqlalchemy import and_


class BuildingCRUD:
    @staticmethod
    async def get_list(db: AsyncSession, address: str | None = None):
        query = select(Building)
        filters = []

        if address:
            filters.append(Building.address.ilike(f"%{address}%"))

        if filters:
            query = query.where(and_(*filters))

        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get(session: AsyncSession, building_id: int):
        return await session.get(Building, building_id)

    @staticmethod
    async def create(session: AsyncSession, building_in: BuildingCreate):
        building = Building(**building_in.dict())
        session.add(building)
        await session.commit()
        await session.refresh(building)
        return building

    @staticmethod
    async def update(session: AsyncSession, building_id: int, building_in: BuildingUpdate):
        building = await session.get(Building, building_id)
        if not building:
            return None
        for field, value in building_in.dict(exclude_unset=True).items():
            setattr(building, field, value)
        await session.commit()
        await session.refresh(building)
        return building

    @staticmethod
    async def delete(session: AsyncSession, building_id: int):
        building = await session.get(Building, building_id)
        if not building:
            return None
        await session.delete(building)
        await session.commit()
        return building
