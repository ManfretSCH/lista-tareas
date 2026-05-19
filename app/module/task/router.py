from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.module.auth.models import User
from app.module.task.enums import TaskStatus
from app.module.task.schemas import CreateTask, TaskPatch, TaskResponse, TaskUpdate
from app.module.task.service import create_task, list_tasks, task_delete, task_patch, task_update

router = APIRouter()


@router.get("/", response_model=list[TaskResponse])
async def list_task(
    status: TaskStatus | None = Query(default=None, description="filtro por estado"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await list_tasks(user_id=current_user.id, status=status, db=db)


@router.post("/", response_model=TaskResponse, status_code=201)
async def task_register(
    task: CreateTask,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await create_task(user_id=current_user.id, task=task, db=db)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await task_update(user_id=current_user.id, task_id=task_id, task_update=task, db=db)


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task_partial(
    task_id: int,
    data: TaskPatch,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await task_patch(user_id=current_user.id, task_id=task_id, data=data, db=db)


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    await task_delete(user_id=current_user.id, task_id=task_id, db=db)
