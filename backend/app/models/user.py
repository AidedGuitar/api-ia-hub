import uuid
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

class User(Base):
    __tablename__ = 'user'

    use_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    use_name = Column(String(100), nullable=False)
    use_email = Column(String(100), unique=True, nullable=False)
    use_career = Column(String(100))
    use_academic_level = Column(String(50))
    use_rol_id = Column(Integer, ForeignKey('role.rol_id'), nullable=False)
    auth_provider = Column(String, default="local")  # 'local' o 'google'
    hashed_password = Column(String, nullable=True)  # <= AGREGAR ESTA LINEA
