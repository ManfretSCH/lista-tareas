from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.module.task.models import Task
from app.module.task.schemas import CreateTask, TaskUpdate


async def get_tasks_by_id_user(user_id: int, db: AsyncSession):
    result = await db.execute(select(Task).where(Task.user_id == user_id))
    return result.scalars().all()


async def create_task_repo(task_data: CreateTask, user_id, db: AsyncSession):
    task_db = Task(name=task_data.name, description=task_data.description, user_id=user_id)

    db.add(task_db)
    await db.commit()
    await db.refresh(task_db)
    return task_db


async def count_task_by_user(user_id: int, db: AsyncSession) -> int:
    result = await db.execute(select(func.count()).select_from(Task).where(Task.user_id == user_id))

    return result.scalar() or 0


async def modify_task(user_id: int, task_id: int, task: TaskUpdate, db: AsyncSession):
    result = await db.execute(
        update(Task)
        .where(Task.id == task_id, Task.user_id == user_id)
        .values(name=task.name, description=task.description)
    )

    await db.commit()
    return result.rowcount > 0  # type: ignore[attr-defined]


async def delete_task_repo(user_id: int, task_id: int, db: AsyncSession):
    result = await db.execute(delete(Task).where(Task.user_id == user_id, Task.id == task_id))

    await db.commit()
    return result.rowcount > 0  # type: ignore[attr-defined]
