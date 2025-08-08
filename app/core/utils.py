from math import radians, cos, sin, asin, sqrt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.activity import Activity


def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r


async def get_nested_activity_ids(root_id: int, db: AsyncSession) -> list[int]:
    result = await db.execute(select(Activity))
    all_activities = result.scalars().all()

    ids = set()

    def recurse(parent_id, level=0):
        for a in all_activities:
            if a.parent_id == parent_id:
                ids.add(a.id)
                if level < 2:  # max 3 уровня
                    recurse(a.id, level + 1)

    ids.add(root_id)
    recurse(root_id)
    return list(ids)
