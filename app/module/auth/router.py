from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.module.auth.schemas import ChangePassword, Token, UserCreate
from app.module.auth.service import change_password, create_user, login_user

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    return await login_user(form_data.username, form_data.password, db)


@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(user, db)


@router.put("/change-password")
async def update_password(
    payload: ChangePassword,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await change_password(payload.old_password, payload.new_password, current_user.email, db)
