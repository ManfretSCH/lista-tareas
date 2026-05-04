from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.module.auth.service import login_user, create_user
from app.module.auth.schemas import UserLogin, UserCreate


router = APIRouter()


@router.post('/login')
def login(user: UserLogin, db: Session = Depends(get_db)):
    if login_user(user, db):
        return {
            'message': 'Iniciando Sesion'
        }

@router.post('/register')
def register(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)