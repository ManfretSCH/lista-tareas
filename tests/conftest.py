"""
conftest.py: pytest descubre este archivo automáticamente y todas las
fixtures definidas aquí están disponibles en cualquier test_*.py sin importar.
"""

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.core.dependencies import get_db
from app.db.base import Base
from app.main import app

# Importar los modelos para que SQLAlchemy los registre en Base.metadata
# antes de crear las tablas.
from app.module.auth import models  # noqa: F401
from app.module.task import models as task_models  # noqa: F401

# ---------- DB de pruebas ----------


# SQLite ":memory:" vive dentro de UNA conexión. Si cada sesión abre su propia
# conexión, cada una ve una DB distinta y vacía. StaticPool fuerza a que todas
# las sesiones reusen la misma conexión, así comparten datos.
@pytest_asyncio.fixture
async def engine():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(engine) -> AsyncSession:
    """Sesión async para tests unitarios que necesiten hablar con la DB
    sin pasar por HTTP."""
    SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with SessionLocal() as session:
        yield session


# ---------- Cliente HTTP ----------


@pytest_asyncio.fixture
async def client(engine):
    """
    Reemplaza la dependencia get_db de FastAPI para que los endpoints
    usen la DB de tests en vez de la real. Después limpia el override.
    """
    SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

    async def override_get_db():
        async with SessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    # ASGITransport llama a la app en memoria, sin levantar uvicorn.
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


# ---------- Helpers de autenticación ----------
"""Registra un usuario, hace login y devuelve los headers Authorization
    listos para usar en endpoints protegidos."""


@pytest_asyncio.fixture
async def auth_headers(client):
    await client.post(
        "/auth/register",
        json={"email": "test@test.com", "password": "secret123"},
    )
    resp = await client.post(
        "/auth/login",
        data={"username": "test@test.com", "password": "secret123"},
    )
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def auth_headers2(client):
    await client.post(
        "/auth/register",
        json={"email": "test2@test.com", "password": "123456789"},
    )
    resp = await client.post(
        "/auth/login",
        data={"username": "test2@test.com", "password": "123456789"},
    )
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
