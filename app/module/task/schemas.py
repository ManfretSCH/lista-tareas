from pydantic import BaseModel


class CreateTask(BaseModel):
    name: str
    description: str


class TaskResponse(BaseModel):
    id: int
    name: str
    description: str
    user_id: int

    model_config = {"from_attributes": True}


class TaskUpdate(BaseModel):
    name: str
    description: str
