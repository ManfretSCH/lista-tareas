from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.module.auth.service import login_user, create_user, change_password
from app.module.auth.schemas import UserCreate, Token, ChangePassword


router = APIRouter()


@router.post('/login', response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)):
    return login_user(form_data.username,form_data.password ,db)


@router.post('/register')
def register(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)


@router.put('/change-password')
def change_password(
    payload: ChangePassword,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return change_password(payload.old_password, 
                           payload.new_password, 
                           current_user.email, db)

