import pytest
from uuid import uuid4
from app.models.interaction import InteractionType

# ---------------------------------------------------------
# TEST: Listar tipos de interacción
# ---------------------------------------------------------
def test_list_interaction_types(client, logged_in_user):
    response = client.get("/interactions/types")
    assert response.status_code == 200
    data = response.json()

    assert sorted(data) == sorted([t.value for t in InteractionType])


# ---------------------------------------------------------
# TEST: Crear una interacción correctamente
# ---------------------------------------------------------
def test_create_interaction(client, logged_in_user):
    response = client.post(
        "/interactions/",
        json={
            "user_id": logged_in_user["user_id"],
            "application_id": logged_in_user["application_id"],
            "int_type": "click"
        }
    )

    assert response.status_code == 201, response.text
    interaction = response.json()

    assert interaction["int_type"] == "click"
    assert interaction["user_id"] == logged_in_user["user_id"]
    assert interaction["application_id"] == logged_in_user["application_id"]
    assert "id" in interaction
    
# ---------------------------------------------------------
# TEST: Error al crear interacción con usuario inexistente
# ---------------------------------------------------------
def test_create_interaction_invalid_user(client, logged_in_user):
    response = client.post(
        "/interactions/",
        json={
            "user_id": str(uuid4()),
            "application_id": logged_in_user["application_id"],
            "int_type": "view"
        }
    )

    
    assert response.status_code == 404
    assert "no existe" in response.json()["detail"]
    
# ---------------------------------------------------------
# TEST: Error al crear interacción con app inexistente
# ---------------------------------------------------------
def test_create_interaction_invalid_app(client, logged_in_user):
    response = client.post(
        "/interactions/",
        json={
            "user_id": logged_in_user["user_id"],
            "application_id": str(uuid4()),
            "int_type": "favorite"
        }
    )

    assert response.status_code == 404
    assert "no existe" in response.json()["detail"]
    


# ---------------------------------------------------------
# TEST: Obtener lista de interacciones (debería devolver lista vacía inicialmente)
# ---------------------------------------------------------
def test_get_interactions_empty(client, logged_in_user):
    response = client.get("/interactions/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ---------------------------------------------------------
# TEST: Obtener interacción por ID
# ---------------------------------------------------------
def test_get_interaction_by_id(client, logged_in_user):
    # Crear interacción
    create_res = client.post(
        "/interactions/",
        json={
            "user_id": logged_in_user["user_id"],
            "application_id": logged_in_user["application_id"],
            "int_type": "view"
        }
    )

    interaction_id = create_res.json()["id"]

    # Obtener por ID
    response = client.get(f"/interactions/{interaction_id}")
    assert response.status_code == 200
    assert response.json()["id"] == interaction_id


# ---------------------------------------------------------
# TEST: Actualizar interacción
# ---------------------------------------------------------
def test_update_interaction(client, logged_in_user):
    # Crear interacción
    create_res = client.post(
        "/interactions/",
        json={
            "user_id": logged_in_user["user_id"],
            "application_id": logged_in_user["application_id"],
            "int_type": "view"
        }
    )

    interaction_id = create_res.json()["id"]

    # Actualizar
    response = client.put(
        f"/interactions/{interaction_id}",
        json={"int_type": "favorite"}
    )

    assert response.status_code == 200
    assert response.json()["int_type"] == "favorite"


# ---------------------------------------------------------
# TEST: Error al actualizar interacción inexistente
# ---------------------------------------------------------
def test_update_interaction_not_found(client, logged_in_user):
    response = client.put(
        f"/interactions/{uuid4()}",
        json={"int_type": "click"}
    )

    assert response.status_code == 404


# ---------------------------------------------------------
# TEST: Eliminar interacción
# ---------------------------------------------------------
def test_delete_interaction(client, logged_in_user):
    # Crear interacción
    create_res = client.post(
        "/interactions/",
        json={
            "user_id": logged_in_user["user_id"],
            "application_id": logged_in_user["application_id"],
            "int_type": "feedback"
        }
    )

    interaction_id = create_res.json()["id"]

    # Eliminar
    delete_res = client.delete(f"/interactions/{interaction_id}")

    assert delete_res.status_code == 200
    assert delete_res.json()["message"] == "Interacción eliminada correctamente"


# ---------------------------------------------------------
# TEST: No puede eliminar interacción ajena
# ---------------------------------------------------------
def test_delete_interaction_wrong_user(client, logged_in_user):
    # Crear otro usuario para simular acceso prohibido
    other_user = {
        "use_name": "Otro Usuario",
        "use_email": "other@example.com",
        "password": "Fakepassword123456",
        "role_id": logged_in_user["user_id"],  # no importa el rol aquí
        "use_career": "medicina",
        "use_academic_level": "pregrado",
    }

    response_cliente = client.post("/users/", json=other_user)
    
    user_data = {
        "use_email": other_user["use_email"],
        "password": other_user["password"]
    }

    # Loguear otro usuario
    login_res = client.post(
        "/auth/login",
        json=user_data
    )

    assert login_res.status_code == 200
    
    # Crear interacción con usuario real
    create_res = client.post(
        "/interactions/",
        json={
            "user_id": response_cliente.json()["id"],
            "application_id": logged_in_user["application_id"],
            "int_type": "click"
        }
    )

    interaction_id = create_res.json()["id"]
    assert create_res.status_code == 201

    # ESTE usuario intenta borrar interacción ajena
    delete_res = client.delete(f"/interactions/{interaction_id}")

    assert delete_res.status_code == 404
    assert "no encontrada" in delete_res.json()["detail"]
