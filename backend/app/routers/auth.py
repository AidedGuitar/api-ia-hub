from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import SocialLoginRequest, UserResponse, UserCreate, UserLogin
from app.core.dependencies import get_db
from app.services.user_service import social_login, create_user, login_user
from app.auth.jwt_handler import create_access_token
from app.auth.google_oauth import verify_google_token
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=UserResponse)
def login_user_endpoint(credentials: UserLogin, response: Response, db: Session = Depends(get_db)):
    try:
        user = login_user(db, credentials)
        
        if not user:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Credenciales inválidas.")
    
        token = create_access_token(user.use_email)
        
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

@router.post("/social-login", response_model=UserResponse)
def google_social_login(
    payload: SocialLoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    # 1. Verificamos el token con Google y extraemos el payload
    info = verify_google_token(payload.id_token)
    email = info["email"]
    name = info.get("name", email.split("@")[0])

    # 2. Creamos o buscamos el usuario
    user = social_login(db, email, name)

    # 3. Generamos un JWT de acceso
    token = create_access_token(user.use_email)
    response.set_cookie(
        key=settings.COOKIE_NAME,
        value=token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        domain=settings.COOKIE_DOMAIN,
    )
    return user

@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    try:
        user = create_user(db, user_in)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key=settings.COOKIE_NAME, domain=settings.COOKIE_DOMAIN)
    return {"msg": "Desconectado"}