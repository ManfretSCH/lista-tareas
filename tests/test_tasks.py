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
    assert response.status_code == 201
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
    response = await client.post(
        "/tasks/",
        json={"name": "copiar", "description": "tareas"},
        headers=auth_headers,
    )
    assert response.status_code == 201

    task_id = response.json()["id"]

    response = await client.put(
        f"/tasks/{task_id}",
        json={"name": "escribir", "description": "lo que sea"},
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
async def test_create_task_invalid_name(client, auth_headers):
    response = await client.post(
        "/tasks/",
        json={"name": "", "description": "que tal"},
        headers=auth_headers,
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_task_of_userA_cannot_by_userB(client, auth_headers, auth_headers2):
    response_user_a = await client.post(
        "/tasks/",
        json={"name": "hola", "description": "que tal"},
        headers=auth_headers,
    )
    assert response_user_a.status_code == 201

    task_id = response_user_a.json()["id"]

    response_user_b = await client.put(
        f"/tasks/{task_id}",
        json={"name": "nuevo", "description": "nueva"},
        headers=auth_headers2,
    )
    # 404 porque el service busca por (user_id, task_id): para B la task no existe.
    assert response_user_b.status_code == 404


@pytest.mark.asyncio
async def test_task_ok(client, auth_headers):
    response = await client.post(
        "/tasks/",
        json={"name": "tarea1", "description": "qdescripcion de tarea 1"},
        headers=auth_headers,
    )
    assert response.status_code == 201

    task_id = response.json()["id"]

    response = await client.delete(
        f"/tasks/{task_id}",
        headers=auth_headers,
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_task_not_found(client, auth_headers):
    response = await client.delete(
        "/tasks/9999",
        headers=auth_headers,
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_task_of_other_user(client, auth_headers, auth_headers2):
    response = await client.post(
        "/tasks/",
        json={"name": "hola mundo", "description": ""},
        headers=auth_headers,
    )
    assert response.status_code == 201

    task_id = response.json()["id"]

    response = await client.delete(
        f"/tasks/{task_id}",
        headers=auth_headers2,
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_patch_task_partial(client, auth_headers):
    response = await client.post(
        "/tasks/",
        json={"name": "hola", "description": "mundo"},
        headers=auth_headers,
    )
    assert response.status_code == 201

    task_id = response.json()["id"]

    response = await client.patch(
        f"/tasks/{task_id}",
        json={"name": "come"},
        headers=auth_headers,
    )
    assert response.status_code == 200

    task = response.json()

    assert task["description"] == "mundo"


@pytest.mark.asyncio
async def test_patch_task_empty_body(client, auth_headers):
    response = await client.post(
        "/tasks/",
        json={"name": "hola", "description": "mundo"},
        headers=auth_headers,
    )
    assert response.status_code == 201

    task_id = response.json()["id"]

    response = await client.patch(f"/tasks/{task_id}", json={}, headers=auth_headers)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_patch_task_not_found(client, auth_headers):
    response = await client.patch(
        "/tasks/9999",
        json={"name": "hola", "description": "mundo"},
        headers=auth_headers,
    )
    assert response.status_code == 404
