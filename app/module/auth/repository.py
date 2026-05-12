from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.module.auth.models import User


async def get_user_by_email(email: str, db: AsyncSession):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def create_user_repo(user_data, hashed_password, db: AsyncSession):
    user_db = User(email=user_data.email, password=hashed_password)

    db.add(user_db)
    await db.commit()
    await db.refresh(user_db)

    return user_db


async def change_password_repo(email, new_password_hashed, db: AsyncSession) -> int:
    result = await db.execute(
        update(User).where(User.email == email).values(password=new_password_hashed)
    )

    await db.commit()
    return result.rowcount > 0  # type: ignore[attr-defined]
