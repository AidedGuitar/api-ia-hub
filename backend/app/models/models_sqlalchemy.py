import uuid
from datetime import datetime, timezone
from sqlalchemy import create_engine, Column, String, Integer, Text, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.types import Enum as SAEnum
import enum

# 1. Conexión a PostgreSQL (ajusta tu usuario y contraseña si es necesario)
DATABASE_URL = "postgresql+psycopg://postgres:123456789@localhost:5432/db_api_ia"

Base = declarative_base()

class InteractionType(str, enum.Enum):
    view = "view"
    click = "click"
    favorite = "favorite"
    feedback = "feedback"

class Role(Base):
    __tablename__ = 'role'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rol_name = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(Base):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    use_name = Column(String(100), nullable=False)
    use_email = Column(String(100), unique=True, nullable=False)
    use_career = Column(String(100))
    use_academic_level = Column(String(50))
    use_rol_id = Column(Integer, ForeignKey('role.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Application(Base):
    __tablename__ = 'application'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    app_name = Column(String(100), nullable=False, unique=True)   # evita duplicados
    app_category = Column(String(100), nullable=True)
    app_link = Column(Text, nullable=False)
    app_description = Column(Text, nullable=True)
    app_source = Column(String(50), nullable=True)  # p.ej. "manual" o "ia"
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Interaction(Base):
    __tablename__ = 'interaction'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    int_use_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    int_app_id = Column(UUID(as_uuid=True), ForeignKey('application.id'), nullable=False)
    int_type = Column(SAEnum(InteractionType, name="interaction_type"), nullable=False)
    int_timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(UUID(as_uuid=True), primary_key=True)
    fee_use_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    fee_app_id = Column(UUID(as_uuid=True), ForeignKey('application.id'), nullable=False)
    fee_rating = Column(Integer, CheckConstraint('fee_rating >= 1 AND fee_rating <= 5'))
    fee_comment = Column(Text)
    fee_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
# 3. Crear las tablas si no existen
def init_db():
    try:
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(engine)
        print("✅ Tablas creadas exitosamente (o ya existen)")
    except SQLAlchemyError as e:
        print("❌ Error al crear las tablas:", e)

if __name__ == "__main__":
    init_db()