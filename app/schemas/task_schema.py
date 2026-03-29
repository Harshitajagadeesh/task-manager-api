from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, List
from app.schemas.response_schema import APIResponse

class TaskBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    status: str = Field(..., pattern="^(pending|in-progress|completed)$")

class TaskRead(TaskBase):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SingleTaskResponse(APIResponse[TaskRead]):
    pass

class TaskListResponse(APIResponse[List[TaskRead]]):
    pass