import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from main import app

# Configura el transporte ASGI para usar la aplicación FastAPI en las pruebas
transport = ASGITransport(app=app)

@pytest.mark.asyncio
async def test_forgot_password():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/forgot-password/forgot-password", json={
            "username": "testuser"
        })
    assert response.status_code == 200
    assert response.json()["message"] == "Código de verificación enviado"

@pytest.mark.asyncio
async def test_confirm_forgot_password():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/forgot-password/confirm-forgot-password", json={
            "username": "testuser",
            "confirmation_code": "654321",
            "new_password": "newsecurepassword123"
        })
    assert response.status_code == 200
    assert response.json()["message"] == "Contraseña restablecida"
