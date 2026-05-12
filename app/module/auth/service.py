from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, get_hash_password, verify_password
from app.module.auth.repository import change_password_repo, create_user_repo, get_user_by_email
from app.module.auth.schemas import UserCreate


async def create_user(user: UserCreate, db: AsyncSession):
    user_existing = await get_user_by_email(user.email, db)
    if user_existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="el imail ya esta en uso")

    hashed_password = get_hash_password(user.password)

    return await create_user_repo(user, hashed_password, db)


async def get_user(email: str, db: AsyncSession):
    user = await get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return user


async def login_user(email, password, db: AsyncSession):
    user_db = await get_user_by_email(email, db)
    if not user_db or not verify_password(password, user_db.password):
        raise HTTPException(401, "credenciales invalidas")
    access_token = create_access_token(data={"sub": user_db.email})

    return {"access_token": access_token, "token_type": "Bearer"}


async def change_password(old_password, new_password, email, db: AsyncSession):
    user = await get_user_by_email(email, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    if not verify_password(old_password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Contraseña incorrecta"
        )
    if old_password == new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ya usaste esta contraseña"
        )

    hash_password = get_hash_password(new_password)
    if await change_password_repo(email, hash_password, db):
        return {"message": "contraseña actualizada"}
