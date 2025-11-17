from uuid import uuid4

# ---------------------------------------
# 1. CREAR USUARIO
# ---------------------------------------
def test_create_user(client):
    payload = {
        "use_name": "Juan Pérez",
        "use_email": "juan@example.com",
        "password": "Password123",
        "use_career": "ingenieria",
        "use_academic_level": "pregrado",
        "use_rol_id": "d6d8d99a-e713-4d03-b2e2-6b66f05bdd6e"
    }

    response = client.post("/users/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["use_email"] == "juan@example.com"
    assert data["use_name"] == "Juan Pérez"


# ---------------------------------------
# 2. GET USERS (LISTA)
# ---------------------------------------
def test_get_users(client):
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ---------------------------------------
# 3. GET USER BY ID
# ---------------------------------------
def test_get_user_by_id(client):
    # crear un usuario primero
    payload = {
        "use_name": "Pedro",
        "use_email": "pedro@example.com",
        "password": "Password123",
        "use_career": "fisica",
        "use_academic_level": "pregrado",
        "use_rol_id": "d6d8d99a-e713-4d03-b2e2-6b66f05bdd6e"
    }

    created = client.post("/users/", json=payload).json()
    user_id = created["id"]

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["id"] == user_id


# ---------------------------------------
# 4. UPDATE USER
# ---------------------------------------
def test_update_user(client):
    payload = {
        "use_name": "Ana",
        "use_email": "ana@example.com",
        "password": "Password123",
        "use_career": "medicina",
        "use_academic_level": "pregrado",
        "use_rol_id":"fbfa60c1-2888-44b5-9eea-de384cc92a95"
    }

    created = client.post("/users/", json=payload).json()
    user_id = created["id"]

    update_payload = {
        "use_name": "Ana Actualizada",
        "use_email": "ana@example.com",
        "password": "Password123",
        "use_career": "psicologia",
        "use_academic_level": "maestria",
        "use_rol_id": "d6d8d99a-e713-4d03-b2e2-6b66f05bdd6e"
    }

    response = client.put(f"/users/{user_id}", json=update_payload)

    assert response.status_code == 200
    assert response.json()["use_name"] == "Ana Actualizada"
    assert response.json()["use_career"] == "psicologia"

# ---------------------------------------
# 5. DELETE USER
# ---------------------------------------
def test_delete_user(client):
    payload = {
        "use_name": "Carlos",
        "use_email": "carlos@example.com",
        "password": "Password123",
        "use_career": "ingenieria",
        "use_academic_level": "pregrado",
        "use_rol_id": "fbfa60c1-2888-44b5-9eea-de384cc92a95"
    }

    created = client.post("/users/", json=payload).json()
    user_id = created["id"]

    response = client.delete(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.json() == {"message": "User deleted successfully"} or isinstance(response.json(), dict)
