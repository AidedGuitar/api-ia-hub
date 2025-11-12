from pydantic import BaseModel, field_validator
from typing import Optional
from uuid import UUID
import re

class UserBase(BaseModel):
    use_name: str
    use_email: str
    use_career: Optional[str] = None
    use_academic_level: Optional[str] = None
    use_rol_id: Optional[UUID] = None

class UserCreate(UserBase):
    password: str
    use_career: str
    use_academic_level: str
    use_rol_id: Optional[UUID] = None  # <- ahora es opcional
    
    @field_validator('use_email')
    @classmethod
    def validate_email(cls, v):
        if "@" not in v:
            raise ValueError("Formato de correo inválido.")
        return v

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8 or not re.search(r"[A-Z]", v) or not re.search(r"[a-z]", v) or not re.search(r"\d", v):
            raise ValueError("La contraseña no cumple con los requisitos. Debe tener al menos 8 caracteres, una letra mayúscula, una letra minúscula y un número.")
        return v
    
class UserRead(UserBase):
    id: UUID
    use_rol_id: UUID

    class Config:
        from_attributes  = True
        
class SocialLoginRequest(BaseModel):
    id_token: str      
        
class UserResponse(BaseModel):
    id: UUID
    use_name: str
    use_email: str
    use_career: str
    use_academic_level: str
    use_rol_id: UUID

    class Config:
        from_attributes  = True  # Esto permite que se pueda convertir el modelo ORM en JSON automáticamente

class UserLogin(BaseModel):
    use_email: str
    password: str
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class UserProfileUpdate(BaseModel):
    use_career: str
    use_academic_level: str