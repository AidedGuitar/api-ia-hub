from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import SocialLoginRequest, UserResponse, UserCreate, UserLogin
from app.core.dependencies import get_db
from app.services.user_service import social_login, create_user, login_user
from app.auth.jwt_handler import create_access_token
from app.auth.google_oauth import verify_google_token
from pydantic import EmailStr, TypeAdapter
from app.config import settings
import re

router = APIRouter(prefix="/auth", tags=["Auth"])

# ---------------------------
# Helpers
# ---------------------------
def validate_email(use_email: str):
    try:
        TypeAdapter(EmailStr).validate_python(use_email)
    except Exception:
        raise HTTPException(status_code=400, detail="Formato de correo inválido.")

def validate_password(password: str):
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="La contraseña debe tener al menos 8 caracteres.")
    if not re.search(r"[A-Z]", password):
        raise HTTPException(status_code=400, detail="La contraseña debe contener al menos una letra mayúscula.")
    if not re.search(r"[a-z]", password):
        raise HTTPException(status_code=400, detail="La contraseña debe contener al menos una letra minúscula.")
    if not re.search(r"\d", password):
        raise HTTPException(status_code=400, detail="La contraseña debe contener al menos un número.")

# ---------------------------
# Endpoints
# ---------------------------
@router.post("/login", response_model=UserResponse)
def login_user_endpoint(credentials: UserLogin, response: Response, db: Session = Depends(get_db)):
    validate_email(credentials.use_email)

    try:
        user = login_user(db, credentials)

        if not user:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Credenciales inválidas.")

        token = create_access_token({"sub": user.use_email})
        if not token:
            raise HTTPException(status_code=500, detail="No se pudo generar el token de acceso.")

        response.set_cookie(
            key=settings.COOKIE_NAME,
            value=token,
            httponly=True,
            secure=settings.COOKIE_SECURE,
            samesite=settings.COOKIE_SAMESITE,
            domain=settings.COOKIE_DOMAIN,
        )

        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno en el inicio de sesión.")
    
@router.post("/social-login", response_model=UserResponse)
def google_social_login(payload: SocialLoginRequest, response: Response, db: Session = Depends(get_db)):
    if not payload.id_token:
        raise HTTPException(status_code=400, detail="Token de Google requerido.")

    try:
        info = verify_google_token(payload.id_token)
        if not info or "email" not in info:
            raise HTTPException(status_code=400, detail="Token de Google inválido o sin email.")

        email = info["email"]
        name = info.get("name", email.split("@")[0])
        validate_email(email)

        user = social_login(db, email, name)

        token = create_access_token({"sub": user.use_email})
        if not token:
            raise HTTPException(status_code=500, detail="No se pudo generar el token de acceso.")

        response.set_cookie(
            key=settings.COOKIE_NAME,
            value=token,
            httponly=True,
            secure=settings.COOKIE_SECURE,
            samesite=settings.COOKIE_SAMESITE,
            domain=settings.COOKIE_DOMAIN,
        )

        return user
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Error al procesar el login social.")


@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    print(user_in)
    validate_email(user_in.use_email)
    validate_password(user_in.password)

    try:
        user = create_user(db, user_in)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al registrar el usuario.")


@router.post("/logout")
def logout(response: Response):
    try:
        response.delete_cookie(key=settings.COOKIE_NAME, domain=settings.COOKIE_DOMAIN)
        return {"msg": "Desconectado"}
    except Exception:
        raise HTTPException(status_code=500, detail="Error al cerrar sesión.")