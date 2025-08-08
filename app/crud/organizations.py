from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from typing import Optional
from app.models.organization import Organization
from app.models.activity import Activity
from app.models.building import Building
from app.schemas.organizations import OrganizationCreate, OrganizationUpdate
from app.core.utils import get_nested_activity_ids, haversine


class OrganizationCRUD:
    @staticmethod
    async def get_list(
            db: AsyncSession,
            name: str | None,
            building_id: int | None,
            activity_id: int | None,
            lat: float | None,
            lon: float | None,
            radius_km: int,
    ) -> list[Organization]:
        query = select(Organization).options(joinedload(Organization.activities))

        if name:
            query = query.where(Organization.name.ilike(f"%{name}%"))

        if building_id:
            query = query.where(Organization.building_id == building_id)

        if activity_id:
            all_ids = await get_nested_activity_ids(activity_id, db)
            query = query.join(Organization.activities).where(Activity.id.in_(all_ids))

        if lat is not None and lon is not None:
            buildings = await db.execute(select(Building))
            building_map = buildings.scalars().all()
            nearby_ids = [
                b.id for b in building_map
                if haversine(b.longitude, b.latitude, lon, lat) <= radius_km
            ]
            query = query.where(Organization.building_id.in_(nearby_ids))
        result = await db.execute(query)
        return result.scalars().unique().all()

    @staticmethod
    async def get(db: AsyncSession, org_id: int) -> Optional[Organization]:
        result = await db.execute(select(Organization).where(Organization.id == org_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, org_in: OrganizationCreate) -> Organization:
        activities_result = await db.execute(
            select(Activity).where(Activity.id.in_(org_in.activity_ids))
        )
        activities = activities_result.scalars().all()

        org = Organization(
            name=org_in.name,
            phones=org_in.phones,
            building_id=org_in.building_id,
            activities=activities
        )

        db.add(org)
        await db.commit()
        await db.refresh(org)
        return org

    @staticmethod
    async def update(db: AsyncSession, org_id: int, org_in: OrganizationUpdate) -> Optional[Organization]:
        org = await OrganizationCRUD.get(db, org_id)
        if not org:
            return None

        if org_in.name is not None:
            org.name = org_in.name
        if org_in.phones is not None:
            org.phones = org_in.phones
        if org_in.building_id is not None:
            org.building_id = org_in.building_id
        if org_in.activity_ids is not None:
            activities_result = await db.execute(
                select(Activity).where(Activity.id.in_(org_in.activity_ids))
            )
            org.activities = activities_result.scalars().all()

        await db.commit()
        await db.refresh(org)
        return org

    @staticmethod
    async def delete(db: AsyncSession, org_id: int) -> bool:
        org = await OrganizationCRUD.get(db, org_id)
        if not org:
            return False
        await db.delete(org)
        await db.commit()
        return True
