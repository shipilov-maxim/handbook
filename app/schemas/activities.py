from pydantic import BaseModel, Field
from typing import Optional, List


class ActivityBase(BaseModel):
    name: str = Field(..., example="Деятельность")
    parent_id: Optional[int] = None


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Деятельность")
    parent_id: Optional[int] = None


class ActivityRead(ActivityBase):
    id: int
    parent_id: Optional[int]
    level: Optional[int] = None

    class Config:
        from_attributes = True


class ActivityWithChildren(ActivityRead):
    children: List["ActivityWithChildren"] = []

    class Config:
        from_attributes = True


ActivityWithChildren.update_forward_refs()
