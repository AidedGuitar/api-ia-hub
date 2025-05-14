from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import SocialLoginRequest, UserResponse, UserCreate, UserLogin
from app.core.dependencies import get_db
from app.services.user_service import social_login, create_user, login_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login_user_endpoint(credentials: UserLogin, db: Session = Depends(get_db)):
    try:
        user = login_user(db, credentials)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/social-login", response_model=UserResponse)
def google_social_login(social_data: SocialLoginRequest, db: Session = Depends(get_db)):    
    user = social_login(db, social_data)
    return user

@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    try:
        user = create_user(db, user_in)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))