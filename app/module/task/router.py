from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user, get_db
from app.module.auth.models import User
from app.module.task.service import list_tasks, create_task
from app.module.task.schemas import CreateTask, TaskResponse


router = APIRouter()



@router.get('/')
def list_task(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return list_tasks(current_user.id, db)

@router.post('/', response_model=TaskResponse)
def task_register(
    task: CreateTask,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_task(task, current_user.id, db)
    
