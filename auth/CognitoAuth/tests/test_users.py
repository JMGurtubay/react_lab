import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from main import app

# Configura el transporte ASGI para usar la aplicación FastAPI en las pruebas
transport = ASGITransport(app=app)

@pytest.mark.asyncio
async def test_register_user():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/users/register", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepassword123"
        })
    assert response.status_code == 200
    assert response.json()["message"] == "Registro exitoso"

@pytest.mark.asyncio
async def test_confirm_email():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/users/confirm-email", json={
            "username": "testuser",
            "confirmation_code": "123456"
        })
    assert response.status_code == 200
    assert response.json()["message"] == "Email confirmado"

@pytest.mark.asyncio
async def test_login_user():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/users/login", json={
            "username": "testuser",
            "password": "securepassword123"
        })
    assert response.status_code == 200
    assert "session" in response.json()["data"]
