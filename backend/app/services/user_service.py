from uuid import UUID
from sqlalchemy.orm import Session
from app.models import user as user_model
from app.schemas import user as user_schema
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.auth.password_handler import hash_password, verify_password
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

STUDENT_ROLE_ID = UUID("d6d8d99a-e713-4d03-b2e2-6b66f05bdd6e")

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.use_email == email).first()

def get_user(db: Session, user_id: UUID):
     return db.query(user_model.User).filter(user_model.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(user_model.User).offset(skip).limit(limit).all()

def create_user(db: Session, user_in: UserCreate):
    new_user = User(
        use_name=user_in.use_name,
        use_email=user_in.use_email,
        use_career=user_in.use_career,
        use_academic_level=user_in.use_academic_level,
        use_rol_id=user_in.use_rol_id or STUDENT_ROLE_ID,
        auth_provider="local",
        hashed_password=hash_password(user_in.password),
    )
    db.add(new_user)

    try:
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError as e:
        db.rollback()
        raise  # 🚨 Propaga la excepción al caller (register)

def update_user(db: Session, user_id: UUID, user: user_schema.UserCreate):
    db_user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if db_user:
        db_user.use_name = user.use_name
        db_user.use_email = user.use_email
        db_user.use_rol_id = user.use_rol_id or STUDENT_ROLE_ID
        db_user.hashed_password = hash_password(user.password)
        db.commit()
        db.refresh(db_user)
    return db_user

def update_user_profile(db: Session, user_id: UUID, profile_data: user_schema.UserProfileUpdate):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("Usuario no encontrado")
    user.use_career = profile_data.use_career
    user.use_academic_level = profile_data.use_academic_level
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: UUID):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return {"ok": True}
    return {"ok": False}


def social_login(db: Session, email: str, name: str) -> User:
    user = db.query(User).filter(User.use_email == email).first()
    if user:
        return user

    new_user = User(
        use_name=name,
        use_email=email,
        use_rol_id=UUID("d6d8d99a-e713-4d03-b2e2-6b66f05bdd6e"),
        auth_provider="google"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(db: Session, credentials: UserLogin):
    user = db.query(User).filter(User.use_email == credentials.use_email).first()
    if not user:
        raise ValueError("Credenciales inválidas.")

    # ✅ Primero: verificar el proveedor de autenticación
    if user.auth_provider != "local":
        raise ValueError("Credenciales inválidas.")

    # ✅ Segundo: verificar que tenga una contraseña hasheada
    if not user.hashed_password:
        raise ValueError("Credenciales inválidas.")

    # ✅ Tercero: verificar la contraseña
    if not verify_password(credentials.password, user.hashed_password):
        raise ValueError("Credenciales inválidas.")
    
    return user