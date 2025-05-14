from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, SocialLoginRequest, UserLogin
from app.auth.password_handler import hash_password, verify_password

def social_login(db: Session, social_data: SocialLoginRequest):
    # Buscar si el usuario ya existe
    user = db.query(User).filter(User.use_email == social_data.email).first()
    if user:
        return user

    # Si no existe, lo creamos
    new_user = User(
        use_name=social_data.name,
        use_email=social_data.email,
        use_rol_id=2,  # Asignar un rol numérico, por ejemplo 2 = "usuario normal"
        auth_provider="google"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def create_user(db: Session, user_in: UserCreate):
    user = db.query(User).filter(User.use_email == user_in.email).first()
    if user:
        raise ValueError("El usuario ya está registrado.")

    new_user = User(
        use_name=user_in.name,
        use_email=user_in.email,
        hashed_password=hash_password(user_in.password),
        auth_provider="local",
        use_rol_id=2  # Asignar un rol numérico para usuarios locales también
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def login_user(db: Session, credentials: UserLogin):
    user = db.query(User).filter(User.use_email == credentials.email).first()
    if not user:
        raise ValueError("Usuario no encontrado.")

    if user.auth_provider != "local":
        raise ValueError("Este usuario debe iniciar sesión con Google.")

    if not verify_password(credentials.password, user.hashed_password):
        raise ValueError("Contraseña incorrecta.")

    return user
