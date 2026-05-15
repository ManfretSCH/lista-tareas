from pydantic import BaseModel, Field


class CreateTask(BaseModel):
    name: str = Field(..., min_length=8, max_length=24)
    description: str = Field(..., min_length=20, max_length=150)


class TaskResponse(BaseModel):
    id: int
    name: str
    description: str
    user_id: int

    model_config = {"from_attributes": True}


class TaskUpdate(BaseModel):
    name: str
    description: str
