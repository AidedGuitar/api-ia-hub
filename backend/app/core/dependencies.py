from app.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import HTTPException, Cookie, status, Depends
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
    token: str   = Cookie(None, alias=settings.COOKIE_NAME),
    db:    Session = Depends(get_db),             # <<— inyectamos db
):
    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "No autenticado")

    # 1) Validamos el token y extraemos el email
    email = verify_access_token(token)

    # 2) Buscamos al usuario en la BD
    user = get_user_by_email(db, email)           # <<— pasamos db + email
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Usuario no existe")

    return user