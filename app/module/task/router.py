from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.module.auth.models import User
from app.module.task.schemas import CreateTask, TaskResponse, TaskUpdate
from app.module.task.service import create_task, list_tasks, task_update

router = APIRouter()


@router.get("/")
async def list_task(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    return await list_tasks(user_id=current_user.id, db=db)


@router.post("/", response_model=TaskResponse)
async def task_register(
    task: CreateTask,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await create_task(user_id=current_user.id, task=task, db=db)


@router.put("/{task_id}")
async def update_task(
    task_id: int,
    task: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await task_update(user_id=current_user.id, task_id=task_id, task_update=task, db=db)
