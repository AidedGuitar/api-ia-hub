from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
        
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

class UserLogin(BaseModel):
    email: EmailStr
    password: str