from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_hash_password,verify_password
from schemas import UserCreate, UserLogin
from repository import get_user_by_email, create_user_repo

def create_user(user: UserCreate, db: Session):
    user_existing = get_user_by_email(user.email, db)
    if user_existing:
        raise HTTPException(status_code=401, detail="el imail ya esta en uso")
    
    hashed_password = get_hash_password(user.password)

    return create_user_repo(user,hashed_password ,db)


def get_user(email: str, db: Session):
    user =get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


def login_user(user: UserLogin, db: Session):
    user_db = get_user_by_email(user.email, db)
    if not user_db or not verify_password(user.password, user_db.password):
        raise HTTPException(401, "credenciales invalidas")
    return user_db

