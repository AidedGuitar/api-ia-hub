from unittest.mock import patch

# ---------------------------
# /register
# ---------------------------
@patch("app.routers.auth.create_user")
def test_register_exitoso(mock_create_user, client):
    mock_create_user.return_value = {
    "id": "60138a22-3ce4-48e8-b49f-60229d0edfbb",
    "use_name": "Juan Perez",
    "use_email": "testUser@example.com",
    "use_rol_id": "d6d8d99a-e713-4d03-b2e2-6b66f05bdd6e"
    }
    user_data = {"use_name": "Juan Perez", "use_email": "testUser@example.com", "password": "Password1"}
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    json_data = response.json()
    assert "id" in json_data
    assert json_data["use_email"] == "testUser@example.com"

def test_register_email_invalido(client):
    response = client.post("/auth/register", json={"use_name": "Juan Perez", "use_email": "invalidom", "password": "Password1"})
    assert response.status_code == 400
    
def test_register_password_invalido(client):
    response = client.post("/auth/register", json={"use_name": "Juan Perez", "use_email": "invalido@example.com", "password": "Pad1"})
    assert response.status_code == 400

# ---------------------------
# /logout
# ---------------------------
def test_logout(client):
    response = client.post("/auth/logout")
    assert response.status_code == 200
    assert response.json()["msg"] == "Desconectado"
