from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.module.task.repository import get_tasks_by_id_user, create_task_repo, verify_task_for_user
from app.module.task.repository import count_task_by_user, modify_task, get_task_by_id
from app.module.task.schemas import CreateTask, TaskUpdate

def list_tasks(id_user: str, db: Session) -> list:
    return get_tasks_by_id_user(id_user, db)

def create_task(task: CreateTask,user_id:int ,db: Session):
    count = count_task_by_user(user_id, db)
    if count > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail='Limite de tareas alcanzado')
    return create_task_repo(task,user_id ,db)

def task_update(user_id: int, task_id: int, task_update: TaskUpdate,db: Session):
    if verify_task_for_user(user_id, task_id, db):
        return modify_task(task_id,task_update,db)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No autorizado')

