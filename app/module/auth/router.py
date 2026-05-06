from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.module.auth.service import login_user, create_user
from app.module.auth.schemas import UserLogin, UserCreate, Token


router = APIRouter()


@router.post('/login', response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)):
    return login_user(form_data.username,form_data.password ,db)


@router.post('/register')
def register(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)