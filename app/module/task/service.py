from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.module.task.repository import get_tasks_by_id, create_task_repo, count_task_by_user
from app.module.task.schemas import CreateTask

def list_tasks(id: str, db: Session) -> list:
    return get_tasks_by_id(id, db)

def create_task(task: CreateTask,user_id ,db: Session):
    count = count_task_by_user(user_id, db)
    if count > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail='Limite de tareas alcanzado')
    return create_task_repo(task,user_id ,db)