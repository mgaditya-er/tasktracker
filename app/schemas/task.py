from pydantic import BaseModel, Field
from typing import Optional


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    description: Optional[str] = None
    owner_id: int


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = None
    status: Optional[str] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    owner_id: int

    class Config:
        from_attributes = True