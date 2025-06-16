from app.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import HTTPException, Cookie, status
from app.auth.jwt_handler import verify_access_token
from app.services.user_service import get_user_by_email
from app.config import settings
from typing import Iterator


# Dependency para obtener la sesión de la base de datos
def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    token: str = Cookie(None, alias=settings.COOKIE_NAME)
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autenticado")
    email = verify_access_token(token)
    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no existe")
    return user