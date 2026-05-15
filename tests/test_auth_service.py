"""
Tests UNITARIOS del service. No pasan por HTTP — llaman a la función
directamente. Útil para validar reglas de negocio puras (casos borde,
excepciones) sin la sobrecarga de toda la cadena FastAPI.
"""

import pytest
from fastapi import HTTPException

from app.module.auth.schemas import UserCreate
from app.module.auth.service import change_password, create_user, login_user


@pytest.mark.asyncio
async def test_create_user_persists(db_session):
    user = await create_user(UserCreate(email="u@test.com", password="1234"), db_session)
    assert user.id is not None
    assert user.email == "u@test.com"
    # La password guardada debe estar hasheada, no en texto plano.
    assert user.password != "1234"


@pytest.mark.asyncio
async def test_create_user_duplicate_raises_409(db_session):
    await create_user(UserCreate(email="x@test.com", password="1234"), db_session)

    with pytest.raises(HTTPException) as exc:
        await create_user(UserCreate(email="x@test.com", password="1234"), db_session)
    assert exc.value.status_code == 409


@pytest.mark.asyncio
async def test_login_wrong_password_raises_401(db_session):
    await create_user(UserCreate(email="a@test.com", password="correcta"), db_session)

    with pytest.raises(HTTPException) as exc:
        await login_user("a@test.com", "incorrecta", db_session)
    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_change_password_wrong_password_raises_401(db_session):
    await create_user(UserCreate(email="a@gmail.com", password="123456"), db_session)

    with pytest.raises(HTTPException) as exc:
        await change_password("12345", "111111", "a@gmail.com", db_session)
    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_change_password_success(db_session):
    # Caso EXITOSO: el service NO lanza, devuelve un dict.
    # No usamos pytest.raises porque no hay excepción que capturar.
    await create_user(UserCreate(email="a@gmail.com", password="123456"), db_session)

    result = await change_password("123456", "111111", "a@gmail.com", db_session)

    assert result == {"message": "contraseña actualizada"}


@pytest.mark.asyncio
async def test_change_password_same_password_raises_400(db_session):
    # Otro caso de ERROR: nueva == vieja.
    await create_user(UserCreate(email="a@gmail.com", password="123456"), db_session)

    with pytest.raises(HTTPException) as exc:
        await change_password("123456", "123456", "a@gmail.com", db_session)
    assert exc.value.status_code == 400
