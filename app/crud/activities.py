from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.exceptions import ParentActivityNotFound, MaxLevelReached
from app.models.activity import Activity
from app.schemas.activities import ActivityCreate, ActivityUpdate


class ActivityCRUD:

    @staticmethod
    async def get_all(session: AsyncSession):
        result = await session.execute(select(Activity))
        return result.scalars().all()

    @staticmethod
    async def get(session: AsyncSession, activity_id: int):
        return await session.get(Activity, activity_id)

    @staticmethod
    async def create(session: AsyncSession, data: ActivityCreate):
        if data.parent_id is not None:
            parent = await session.get(Activity, data.parent_id)
            if not parent:
                raise ParentActivityNotFound
            level = parent.level + 1
            if level > 2:
                raise MaxLevelReached
        else:
            level = 0

        activity = Activity(
            name=data.name,
            parent_id=data.parent_id,
            level=level
        )
        session.add(activity)
        await session.commit()
        await session.refresh(activity)
        return activity

    @staticmethod
    async def update(session: AsyncSession, activity_id: int, activity_in: ActivityUpdate):
        activity = await session.get(Activity, activity_id)
        if not activity:
            return None
        for field, value in activity_in.dict(exclude_unset=True).items():
            setattr(activity, field, value)
        await session.commit()
        await session.refresh(activity)
        return activity

    @staticmethod
    async def delete(session: AsyncSession, activity_id: int):
        activity = await session.get(Activity, activity_id)
        if not activity:
            return None
        await session.delete(activity)
        await session.commit()
        return activity

    @staticmethod
    async def get_hierarchical(session: AsyncSession):
        result = await session.execute(
            select(Activity).where(Activity.level <= 3).options(selectinload(Activity.children))
        )
        activities = result.scalars().unique().all()

        activity_dict = {a.id: a for a in activities}
        for a in activity_dict.values():
            a.children = []

        tree = []
        for a in activity_dict.values():
            if a.parent_id:
                parent = activity_dict.get(a.parent_id)
                if parent:
                    parent.children.append(a)
            else:
                tree.append(a)

        return tree
