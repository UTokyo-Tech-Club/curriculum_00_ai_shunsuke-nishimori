# api/schemas/task.py

from typing import Optional
from pydantic import BaseModel, Field

class TaskBase(BaseModel):
    query: Optional[str] = Field(None, example="低カロリーな晩御飯の提案をして")

class TaskCreate(TaskBase):
    pass

class TaskCreateResponse(TaskCreate):
    id: int
    result: str

    class Config:
        orm_mode = True

class Task(TaskBase):
    id: int
    result: str
    done: bool = Field(False, description="完了フラグ")

    class Config:
        orm_mode = True