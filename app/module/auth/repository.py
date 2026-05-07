from sqlalchemy.orm import Session
from app.module.auth.models import User


def get_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()


def create_user_repo(user_data, hashed_password, db: Session):
    user_db = User(
        email= user_data.email,
        password=hashed_password
    )

    db.add(user_db)
    db.commit()
    db.refresh(user_db)

    return user_db

def change_password_repo(email, new_password_hashed, db: Session):
    rows_updated = db.query(User).filter(User.email == email).update({User.password: new_password_hashed})

    db.commit()
    return rows_updated > 0

        