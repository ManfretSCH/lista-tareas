"""
Tests de endpoints de auth (integración: HTTP -> router -> service -> DB).
Estructura típica de un test:
    1. Arrange: preparar datos / estado
    2. Act:     llamar al endpoint
    3. Assert:  verificar respuesta y/o estado de la DB
"""

import pytest


@pytest.mark.asyncio
async def test_register_creates_user(client):
    response = await client.post(
        "/auth/register",
        json={"email": "nuevo@test.com", "password": "1234"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "nuevo@test.com"
    # La contraseña nunca debería volver al cliente
    assert "password" not in body or body.get("password") != "1234"


@pytest.mark.asyncio
async def test_register_duplicate_email_returns_409(client):
    payload = {"email": "dup@test.com", "password": "1234"}
    await client.post("/auth/register", json=payload)

    response = await client.post("/auth/register", json=payload)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_login_returns_token(client):
    await client.post(
        "/auth/register",
        json={"email": "login@test.com", "password": "1234"},
    )
    # /auth/login usa OAuth2PasswordRequestForm: form-data, no JSON.
    response = await client.post(
        "/auth/login",
        data={"username": "login@test.com", "password": "1234"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_invalid_credentials(client):
    response = await client.post(
        "/auth/login",
        data={"username": "noexiste@test.com", "password": "x"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_change_password_ok(client, auth_headers):
    response = await client.put(
        "/auth/change-password",
        json={"old_password": "secret123", "new_password": "nuevopass"},
        headers=auth_headers,
    )
    assert response.status_code == 200

    # Verifica que la contraseña vieja ya no sirve y la nueva sí.
    bad = await client.post(
        "/auth/login",
        data={"username": "test@test.com", "password": "secret123"},
    )
    assert bad.status_code == 401

    good = await client.post(
        "/auth/login",
        data={"username": "test@test.com", "password": "nuevopass"},
    )
    assert good.status_code == 200


@pytest.mark.asyncio
async def test_change_password_requires_auth(client):
    response = await client.put(
        "/auth/change-password",
        json={"old_password": "x", "new_password": "y"},
    )
    assert response.status_code == 401
