from pydantic import BaseModel, Field
from typing import List, Optional


class ActivityOut(BaseModel):
    id: int
    name: str = Field(..., example="Деятельность")

    class Config:
        from_attributes = True


class OrganizationBase(BaseModel):
    name: str = Field(..., example="ООО Организация")
    phones: List[str] = Field(..., example=["2-222-222", "3-333-333"])
    building_id: int


class OrganizationCreate(OrganizationBase):
    activity_ids: List[int]


class OrganizationUpdate(BaseModel):
    name: Optional[str] = Field(None, example="ООО Организация")
    phones: Optional[List[str]] = Field(None, example=["2-222-222", "3-333-333"])
    building_id: Optional[int] = None
    activity_ids: Optional[List[int]] = None


class OrganizationOut(OrganizationBase):
    id: int
    activities: List[ActivityOut]

    class Config:
        from_attributes = True
