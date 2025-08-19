import pytest
from fastapi import HTTPException
from app.routers.auth import validate_email, validate_password

def test_validate_email_valido():
    # No debe lanzar excepción
    validate_email("test@example.com")

def test_validate_email_invalido():
    with pytest.raises(HTTPException) as exc:
        validate_email("correo-invalido")
    assert exc.value.status_code == 400
    assert "Formato de correo inválido" in exc.value.detail

def test_validate_password_valida():
    # No debe lanzar excepción
    validate_password("Password1")

@pytest.mark.parametrize("password, mensaje", [
    ("short", "al menos 8 caracteres"),
    ("nouppercase1", "mayúscula"),
    ("NOLOWERCASE1", "minúscula"),
    ("NoNumber", "número"),
])
def test_validate_password_invalida(password, mensaje):
    with pytest.raises(HTTPException) as exc:
        validate_password(password)
    assert mensaje in exc.value.detail
