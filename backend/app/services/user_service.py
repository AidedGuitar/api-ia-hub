from sqlalchemy.orm import Session
from app.models import user as user_model
from app.schemas import user as user_schema

def get_user(db: Session, user_id: int):
    return db.query(user_model.User).filter(user_model.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(user_model.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: user_schema.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = user_model.User(username=user.username, email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: user_schema.UserCreate):
    db_user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if db_user:
        db_user.username = user.username
        db_user.email = user.email
        db_user.hashed_password = user.password + "notreallyhashed"
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return {"ok": True}
    return {"ok": False}