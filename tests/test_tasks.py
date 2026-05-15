"""Tests de endpoints de tasks. Requieren un usuario autenticado, así que
todos reciben la fixture `auth_headers`."""

import pytest


@pytest.mark.asyncio
async def test_create_task(client, auth_headers):
    response = await client.post(
        "/tasks/",
        json={"name": "comprar pan", "description": "ir a la panaderia"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "comprar pan"
    assert body["id"] > 0


@pytest.mark.asyncio
async def test_list_tasks_empty(client, auth_headers):
    response = await client.get("/tasks/", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_list_tasks_returns_created(client, auth_headers):
    await client.post(
        "/tasks/",
        json={"name": "t1", "description": "d1"},
        headers=auth_headers,
    )
    await client.post(
        "/tasks/",
        json={"name": "t2", "description": "d2"},
        headers=auth_headers,
    )
    response = await client.get("/tasks/", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_update_task(client, auth_headers):
    created = await client.post(
        "/tasks/",
        json={"name": "viejo", "description": "vieja"},
        headers=auth_headers,
    )
    task_id = created.json()["id"]

    response = await client.put(
        f"/tasks/{task_id}",
        json={"name": "nuevo", "description": "nueva"},
        headers=auth_headers,
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_tasks_require_auth(client):
    response = await client.get("/tasks/")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_task_id_invalid(client, auth_headers):
    response = await client.put(
        "/tasks/9999",
        json={"name": "hola", "description": "que tal"},
        headers=auth_headers,
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_task_of_userA_cannot_by_userB(client, auth_headers, auth_headers2):
    response_user_a = await client.post(
        "/tasks/", json={"name": "hola", "description": "que tal"}, headers=auth_headers
    )
    assert response_user_a.status_code == 200

    task_id = response_user_a.json()["id"]

    response_user_b = await client.put(
        f"/tasks/{task_id}",
        json={"name": "nuevo", "description": "nueva"},
        headers=auth_headers2,
    )
    # 404 porque el service busca por (user_id, task_id): para B la task no existe.
    assert response_user_b.status_code == 404
