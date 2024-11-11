import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from main import app

# Configura el transporte ASGI para usar la aplicación FastAPI en las pruebas
transport = ASGITransport(app=app)

@pytest.mark.asyncio
async def test_associate_totp():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/mfa/associate-totp", json={
            "session": "example_session"
        })
    assert response.status_code == 200
    assert "secret_code" in response.json()
    assert response.json()["message"] == "Asociación de TOTP exitosa"

@pytest.mark.asyncio
async def test_verify_totp():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/mfa/verify-totp", json={
            "session": "example_session",
            "user_code": "123456"
        })
    assert response.status_code == 200
    assert response.json()["message"] == "TOTP configurado"
