from sqlalchemy.orm import Session
from app.module.task.models import Task

def get_tasks_by_id(id: str, db: Session):
    return db.query(Task).filter(Task.user_id == id).all()

def create_task_repo(task_data: dict,user_id ,db: Session):
    task_db = Task(
        name = task_data.name,
        description = task_data.description,
        user_id = user_id
    )

    db.add(task_db)
    db.commit()
    db.refresh(task_db)
    return task_db

def count_task_by_user(user_id: int, db: Session):
    return db.query(Task).filter(Task.user_id == user_id).count()
