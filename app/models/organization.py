from sqlalchemy import Column, String, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from app.db.base import Base

organization_activities = Table(
    "organization_activities",
    Base.metadata,
    Column("organization_id", Integer, ForeignKey("organizations.id"), primary_key=True),
    Column("activity_id", Integer, ForeignKey("activities.id"), primary_key=True),
)


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    phones = Column(ARRAY(String), nullable=False)
    building_id = Column(Integer, ForeignKey("buildings.id"))

    building = relationship("Building")
    activities = relationship(
        "Activity",
        secondary=organization_activities,
        backref="organizations",
        lazy="selectin"
    )
