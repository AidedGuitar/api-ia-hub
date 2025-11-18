# tests/test_applications.py

from uuid import uuid4

# ===============================================
# TEST: Crear una aplicación
# ===============================================
def test_create_application(client):
    payload = {
        "app_name": "Khan Academy",
        "app_category": "Educación",
        "app_link": "https://khanacademy.org",
        "app_description": "Plataforma educativa gratuita",
        "app_source": "manual",
        "app_keywords": "math, science, physics",
        "app_academic_level": "Universitario"
    }

    response = client.post("/apps/", json=payload)

    assert response.status_code == 201
    data = response.json()

    assert data["app_name"] == "Khan Academy"
    assert data["app_link"] == "https://khanacademy.org"
    assert data["app_keywords"] == "math, science, physics"
    assert data["app_academic_level"] == "Universitario"
    assert "id" in data


# ===============================================
# TEST: Error por aplicación duplicada (409)
# ===============================================
def test_create_duplicate_application(client):
    payload = {
        "app_name": "Coursera",
        "app_category": "Educación",
        "app_link": "https://coursera.org",
        "app_description": "Cursos online",
        "app_source": "manual",
        "app_keywords": "math, science, physics",
        "app_academic_level": "Universitario"
    }

    # Primer insert OK
    client.post("/apps/", json=payload)

    # Segundo insert debe fallar
    response = client.post("/apps/", json=payload)

    assert response.status_code == 409
    assert response.json()["detail"] == "El nombre de la aplicación ya existe."


# ===============================================
# TEST: Listar aplicaciones
# ===============================================
def test_read_applications(client):
    response = client.get("/apps/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)


# ===============================================
# TEST: Obtener aplicación por ID
# ===============================================
def test_read_application_by_id(client):
    # Crear primero
    app = client.post("/apps/", json={
        "app_name": "Wikipedia",
        "app_category": "Referencia",
        "app_link": "https://wikipedia.org",
        "app_description": "Enciclopedia libre",
        "app_source": "manual",
        "app_keywords": "inteligencia artificial, chat, aprendizaje",
        "app_academic_level": "Profesional"
    }).json()

    response = client.get(f"/apps/{app['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == app["id"]


# ===============================================
# TEST: Obtener app con ID incorrecto → 404
# ===============================================
def test_read_application_not_found(client):
    random_id = uuid4()
    response = client.get(f"/apps/{random_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Aplicación no encontrada"


# ===============================================
# TEST: Actualizar aplicación
# ===============================================
def test_update_application(client):
    # Crear primero
    app = client.post("/apps/", json={
        "app_name": "Duolingo",
        "app_category": "Idiomas",
        "app_link": "https://duolingo.com",
        "app_description": "Aprende idiomas",
        "app_source": "manual",
        "app_keywords": "inteligencia artificial, chat, aprendizaje",
        "app_academic_level": "Profesional"
    }).json()

    update_payload = {
        "app_name": "Duolingo Updated",
        "app_category": "Idiomas",
        "app_link": "https://duolingo.com",
        "app_description": "Actualizado",
        "app_source": "ia",
        "app_keywords": "math, science, physics",
        "app_academic_level": "Universitario"
    }

    response = client.put(f"/apps/{app['id']}", json=update_payload)

    assert response.status_code == 200
    data = response.json()

    assert data["app_name"] == "Duolingo Updated"
    assert data["app_description"] == "Actualizado"
    assert data["app_source"] == "ia"
    assert data["app_keywords"] == "math, science, physics"
    assert data["app_academic_level"] == "Universitario"


# ===============================================
# TEST: UPDATE de aplicación inexistente → 404
# ===============================================
def test_update_application_not_found(client):
    random_id = uuid4()

    payload = {
        "app_name": "Nada",
        "app_category": "N/A",
        "app_link": "https://google.com",
        "app_description": "Desconocido",
        "app_source": "manual",
        "app_keywords": "math, science, physics",
        "app_academic_level": "Universitario"
    }

    response = client.put(f"/apps/{random_id}", json=payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Aplicación no encontrada"


# ===============================================
# TEST: Borrar aplicación
# ===============================================
def test_delete_application(client):
    # Crear una app para borrarla
    app = client.post("/apps/", json={
        "app_name": "GeoGebra",
        "app_category": "Matemáticas",
        "app_link": "https://geogebra.org",
        "app_description": "Herramientas matemáticas",
        "app_source": "manual",
        "app_keywords": "math, science, physics",
        "app_academic_level": "Universitario"
    }).json()

    response = client.delete(f"/apps/{app['id']}")
    assert response.status_code == 204

    # Verificar que ya no existe
    response2 = client.get(f"/apps/{app['id']}")
    assert response2.status_code == 404


# ===============================================
# TEST: DELETE de aplicación inexistente
# ===============================================
def test_delete_application_not_found(client):
    random_id = uuid4()

    response = client.delete(f"/apps/{random_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Aplicación no encontrada"
