from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.db.session import sessionLocal
from app.module.auth.models import User
from app.core.security import decode_access_token
from app.module.auth.repository import get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

def get_db():
    db = sessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_current_user(
        token: str = Depends(oauth2_scheme), 
        db: Session = Depends(get_db) 
    )-> User:

        payload = decode_access_token(token)
        email: str = payload.get('sub')
        if email is None:
             raise HTTPException(
                  status_code=status.HTTP_401_UNAUTHORIZED,
                  detail='Token sin sujeto'
             )
        user = get_user_by_email(email, db)
        if user is None:
             raise HTTPException(
                  status_code=status.HTTP_401_UNAUTHORIZED,
                  detail='Usuario no encontrado'
             )
        return user