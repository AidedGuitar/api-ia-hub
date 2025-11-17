import uuid
from fastapi import status

def test_register_user_success(client):
    payload = {
        "use_name": "Carlos Test",
        "use_email": "test@example.com",
        "password": "Password123",
        "use_career": "ingenieria",
        "use_academic_level": "pregrado",
    }

    response = client.post("/auth/register", json=payload)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["use_email"] == payload["use_email"]
    assert "id" in data


def test_register_duplicate_email(client):
    payload = {
        "use_name": "Carlos Test",
        "use_email": "duplicate@example.com",
        "password": "Password123",
        "use_career": "ingenieria",
        "use_academic_level": "pregrado",
    }

    client.post("/auth/register", json=payload)  # primera vez OK
    response = client.post("/auth/register", json=payload)  # duplicado

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "El correo electrónico ya está registrado."


def test_login_success(client):
    # Primero registramos un usuario
    payload = {
        "use_name": "Login User",
        "use_email": "login@example.com",
        "password": "Password123",
        "use_career": "medicina",
        "use_academic_level": "pregrado",
    }

    client.post("/auth/register", json=payload)

    # Ahora probamos el login
    login_payload = {
        "use_email": "login@example.com",
        "password": "Password123"
    }

    response = client.post("/auth/login", json=login_payload)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    login_payload = {
        "use_email": "noexiste@example.com",
        "password": "Invalid123"
    }

    response = client.post("/auth/login", json=login_payload)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_logout(client):
    response = client.post("/auth/logout")
    assert response.status_code == 200
    assert response.json() == {"msg": "Desconectado"}
