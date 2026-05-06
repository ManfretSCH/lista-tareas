from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_hash_password,verify_password
from app.module.auth.schemas import UserCreate, UserLogin
from app.module.auth.repository import get_user_by_email, create_user_repo
from app.core.security import create_access_token

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


def login_user(email, password, db: Session):
    user_db = get_user_by_email(email, db)
    if not user_db or not verify_password(password, user_db.password):
        raise HTTPException(401, "credenciales invalidas")
    access_token = create_access_token(data={ 'sub':user_db.email })

    return {'access_token': access_token, 'token_type':'Bearer'}



