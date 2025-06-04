from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

class UserBase(BaseModel):
    use_name: str
    use_email: EmailStr
    use_career: Optional[str] = None
    use_academic_level: Optional[str] = None
    use_rol_id: UUID

class UserCreate(UserBase):
    password: str
    use_rol_id: Optional[UUID] = None  # <- ahora es opcional
    
class UserRead(UserBase):
    id: UUID

    class Config:
        orm_mode = True

class User(BaseModel):
    id: int
    use_name: str
    use_email: str

    class Config:
        orm_mode = True
        
class SocialLoginRequest(BaseModel):
    use_name: str
    use_email: EmailStr       
        
class UserResponse(BaseModel):
    id: UUID
    use_name: str
    use_email: EmailStr
    use_rol_id: UUID

    class Config:
        orm_mode = True  # Esto permite que se pueda convertir el modelo ORM en JSON automáticamente

class UserLogin(BaseModel):
    use_email: EmailStr
    password: str
    
class UserOut(UserBase):
    id: UUID

    class Config:
        orm_mode = True