from pydantic import BaseModel, Field

from app.module.task.enums import TaskStatus


class CreateTask(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    description: str = Field(max_length=500)


class TaskResponse(BaseModel):
    id: int
    name: str
    description: str
    user_id: int
    status: TaskStatus

    model_config = {"from_attributes": True}


class TaskUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    description: str = Field(max_length=500)


class TaskPatch(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=80)
    description: str | None = Field(default=None, max_length=500)
    status: TaskStatus | None = None
