from pydantic import BaseModel, Field


class CreateTask(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    description: str = Field(max_length=500)


class TaskResponse(BaseModel):
    id: int
    name: str
    description: str
    user_id: int

    model_config = {"from_attributes": True}


class TaskUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    description: str = Field(max_length=500)


class TaskPatch(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=80)
    description: str | None = Field(default=None, max_length=500)
