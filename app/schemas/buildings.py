from pydantic import BaseModel, Field
from typing import Optional


class BuildingBase(BaseModel):
    address: str = Field(..., example="ул. Ленина, 1")
    latitude: float = Field(..., example=55.7558)
    longitude: float = Field(..., example=37.6173)


class BuildingCreate(BuildingBase):
    pass


class BuildingUpdate(BaseModel):
    address: Optional[str] = Field(None, example="ул. Ленина, 1")
    latitude: Optional[float] = Field(None, example=55.7558)
    longitude: Optional[float] = Field(None, example=37.6173)


class BuildingOut(BuildingBase):
    id: int

    class Config:
        from_attributes = True
