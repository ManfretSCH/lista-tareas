from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.module.task.repository import (
    count_task_by_user,
    create_task_repo,
    delete_task_repo,
    get_tasks_by_id_user,
    modify_task,
)
from app.module.task.schemas import CreateTask, TaskUpdate


async def list_tasks(user_id: int, db: AsyncSession):
    return await get_tasks_by_id_user(user_id, db)


async def create_task(task: CreateTask, user_id: int, db: AsyncSession):
    count = await count_task_by_user(user_id, db)
    if count >= 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Limite de tareas alcanzado"
        )
    return await create_task_repo(task, user_id, db)


async def task_update(user_id: int, task_id: int, task_update: TaskUpdate, db: AsyncSession):
    row = await modify_task(user_id, task_id, task_update, db)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return await get_tasks_by_id_user(user_id, db)


async def task_delete(user_id: int, task_id: int, db: AsyncSession):
    row = await delete_task_repo(user_id, task_id, db)

    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
