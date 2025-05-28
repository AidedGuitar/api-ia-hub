from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import user as user_schema
from app.services import user_service
from app.core.dependencies import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=user_schema.User)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user)

@router.get("/", response_model=list[user_schema.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return user_service.get_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=user_schema.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_service.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=user_schema.User)
def update_user(user_id: int, user: user_schema.UserCreate, db: Session = Depends(get_db)):
    return user_service.update_user(db, user_id, user)

@router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.delete_user(db, user_id)