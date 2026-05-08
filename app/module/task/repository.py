from sqlalchemy.orm import Session
from app.module.task.models import Task

def get_tasks_by_id_user(id_user: int, db: Session):
    return db.query(Task).filter(Task.user_id == id_user).all()

def get_task_by_id(id_task: int, db: Session):
    return db.query(Task).filter(Task.id == id_task).first()

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

def count_task_by_user(id_user: int, db: Session):
    return db.query(Task).filter(Task.user_id == id_user).count()

def modify_task(id_task, task: dict, db: Session):
    task_update = db.query(Task).filter(Task.id == id_task).update(
        {
            Task.name: task.name,
            Task.description: task.description
        }
    )

    db.commit()
    return task_update > 0

def verify_task_for_user(user_id, task_id, db: Session):
    if db.query(Task).filter(Task.id == task_id, 
                             Task.user_id == user_id).first():
        return True
    return False


