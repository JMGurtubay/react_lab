import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from main import app

# Configura el transporte ASGI para usar la aplicación FastAPI en las pruebas
transport = ASGITransport(app=app)

@pytest.mark.asyncio
async def test_auth_flow():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Registro de usuario
        response = await client.post("/users/register", json={
            "username": "integration_user",
            "email": "integration@example.com",
            "password": "password123"
        })
        assert response.status_code == 200
        assert response.json()["message"] == "Registro exitoso"

        # Confirmación de email
        response = await client.post("/users/confirm-email", json={
            "username": "integration_user",
            "confirmation_code": "123456"
        })
        assert response.status_code == 200
        assert response.json()["message"] == "Email confirmado"

        # Primer login para requerir MFA
        response = await client.post("/users/login", json={
            "username": "integration_user",
            "password": "password123"
        })
        assert response.status_code == 200
        assert "session" in response.json()["data"]

        # Asociación de TOTP
        response = await client.post("/mfa/associate-totp", json={
            "session": response.json()["data"]["session"]
        })
        assert response.status_code == 200
        assert "secret_code" in response.json()

        # Verificación de TOTP
        response = await client.post("/mfa/verify-totp", json={
            "session": response.json()["session"],
            "user_code": "123456"
        })
        assert response.status_code == 200
        assert response.json()["message"] == "TOTP configurado"

        # Segundo login con MFA
        response = await client.post("/users/login", json={
            "username": "integration_user",
            "password": "password123"
        })
        assert response.status_code == 200
        assert "session" in response.json()["data"]

        # Responder al desafío de TOTP
        response = await client.post("/mfa/respond-to-auth-challenge", json={
            "session": response.json()["data"]["session"],
            "username": "integration_user",
            "user_code": "123456"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()

        # Cierre de sesión
        response = await client.post("/users/logout", headers={
            "Authorization": f"Bearer {response.json()['access_token']}"
        })
        assert response.status_code == 200
        assert response.json()["message"] == "Sesión cerrada"

@pytest.mark.asyncio
async def test_password_recovery_flow():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Solicitar recuperación de contraseña
        response = await client.post("/forgot-password/forgot-password", json={
            "username": "integration_user"
        })
        assert response.status_code == 200
        assert response.json()["message"] == "Código de verificación enviado"

        # Confirmar recuperación de contraseña
        response = await client.post("/forgot-password/confirm-forgot-password", json={
            "username": "integration_user",
            "confirmation_code": "654321",
            "new_password": "newpassword123"
        })
        assert response.status_code == 200
        assert response.json()["message"] == "Contraseña restablecida"
