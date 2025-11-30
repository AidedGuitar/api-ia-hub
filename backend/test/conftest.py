# tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.models.models_sqlalchemy import Base
from app.core.dependencies import get_current_user
from app.models.models_sqlalchemy import Role, User, Feedback
from app.models.models_sqlalchemy import User
from app.database import get_db
from uuid import uuid4
import random

# ============================================================
# 1. Base de datos PostgreSQL: SOLO PARA TESTS
# ============================================================

TEST_DATABASE_URL = "postgresql+psycopg://postgres:123456789@localhost:5432/test_db"

# engine especial para testing (NO USA el engine original)
engine = create_engine(TEST_DATABASE_URL, future=True)

# Session para tests
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ============================================================
# 2. Crear y eliminar todas las tablas antes y después de tests
# ============================================================

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    # Crear tablas
    Base.metadata.create_all(bind=engine)

    # Crear roles iniciales si tus endpoints los necesitan
    db = TestingSessionLocal()
    try:
        if db.query(Role).count() == 0:
            ADMIN_ID = uuid4()
            STUDENT_ID = uuid4()
            db.add(Role(id=ADMIN_ID, rol_name="Administrador"))
            db.add(Role(id=STUDENT_ID, rol_name="Estudiante"))
            db.commit()
    finally:
        db.close()

    yield

    # Destruir tablas después de todos los tests
    Base.metadata.drop_all(bind=engine)


# ============================================================
# 3. Override de get_db → usar BD de prueba
# ============================================================

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================
# 4. Override de usuario autenticado
# ============================================================

def override_current_user():
    clienttest = next(get_db()).query(User).filter(User.use_email == "login@example.com").first()
    
    return User(
        id=str(clienttest.id) if clienttest else uuid4(),
        use_name="Test User",
        use_email="login@example.com",
        use_career="Ingeniería",
        use_academic_level="Pregrado",
        use_rol_id="d6d8d99a-e713-4d03-b2e2-6b66f05bdd6e",
        auth_provider="local",
        hashed_password="Password123"
    )


# ============================================================
# 5. Cliente TestClient usando overrides
# ============================================================

@pytest.fixture
def client():
    # Aplicar overrides
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_current_user

    with TestClient(app) as c:
        yield c

    # Limpiar los overrides después de cada test
    app.dependency_overrides.clear()

# ======================================================
# FIXTURE: CREAR USUARIO Y LOGUEAR AUTOMÁTICAMENTE
# ======================================================

@pytest.fixture()
def logged_in_user(client):
    """
    Crea un usuario válido y obtiene su token de login vía cookies.
    """

    user_data = {
        "use_email": "login@example.com",
        "password": "Password123"
    }

    # Hacer login (crea la cookie)
    response = client.post(
        "/auth/login",
        json=user_data
    )

    assert response.status_code == 200    
    
    db_client = next(get_db())
    clienttest = db_client.query(User).filter(User.use_email == user_data['use_email']).first()
    
    responseUser = client.get("/users/"+str(clienttest.id))  # para crear la cookie de sesión
    assert responseUser.status_code == 200
    user = responseUser.json()
    
    responseApps = client.get("/apps/")  # para crear la cookie de sesión
    assert responseApps.status_code == 200
    apps_list = responseApps.json() 
    first_app_id = apps_list[0]["id"] if len(apps_list) > 0 else None

    # 3) Retornar el cliente autenticado
    return {
        "user_id": user["id"],
        "application_id": first_app_id,
    }
    
# ======================================================
# 6. LECTOR DE APLICACIONES PARA TESTS DE FEEDBACK
# ======================================================

@pytest.fixture()
def logged_in_user_with_apps(client):
    """
    Usuario logueado + lista de apps, seleccionando automáticamente una app
    sin feedback previo para evitar errores 409.
    """

    # ---- LOGIN ----
    user_data = {
        "use_email": "login@example.com",
        "password": "Password123"
    }

    response = client.post("/auth/login", json=user_data)
    assert response.status_code == 200

    # ---- OBTENER USER ID ----
    db = next(get_db())
    db_user = db.query(User).filter(User.use_email == user_data["use_email"]).first()

    response_user = client.get(f"/users/{db_user.id}")
    assert response_user.status_code == 200
    user = response_user.json()

    # ---- LISTAR APPS ----
    response_apps = client.get("/apps/")
    assert response_apps.status_code == 200
    apps_list = response_apps.json()

    if not apps_list:
        raise Exception("❌ No hay aplicaciones en la BD para ejecutar los test")

    # ---- SELECCIONAR APP SIN FEEDBACK PREVIO ----
    db = next(get_db())
    selected_app_id = None

    for app in apps_list:
        # Revisar si ya existe feedback de este user para esta app
        exists = db.query(Feedback).filter(
            Feedback.user_id == user["id"],
            Feedback.application_id == app["id"]
        ).first()

        if not exists:
            selected_app_id = app["id"]
            break

    if selected_app_id is None:
        raise Exception("❌ Todas las apps ya tienen feedback del usuario. No hay app disponible.")

    return {
        "user_id": user["id"],
        "application_id": selected_app_id,
    }