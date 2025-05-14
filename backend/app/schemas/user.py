from pydantic import BaseModel, EmailStr
from uuid import UUID

class SocialLoginRequest(BaseModel):
    name: str
    email: EmailStr

class UserResponse(BaseModel):
    use_id: UUID
    use_name: str
    use_email: EmailStr
    use_rol_id: int

    class Config:
        orm_mode = True  # Esto permite que se pueda convertir el modelo ORM en JSON automáticamente

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str