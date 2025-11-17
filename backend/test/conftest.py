# tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.models.models_sqlalchemy import Base
from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.models_sqlalchemy import Role
from app.models.models_sqlalchemy import User

from uuid import uuid4


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
    return User(
        id=uuid4(),
        use_name="Test User",
        use_email="test@example.com",
        use_career="Ingeniería",
        use_academic_level="Pregrado",
        use_rol_id="d6d8d99a-e713-4d03-b2e2-6b66f05bdd6e",
        auth_provider="local",
        hashed_password="fakepass123"
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
