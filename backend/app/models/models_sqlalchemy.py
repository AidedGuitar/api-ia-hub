import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, Text, ForeignKey, DateTime,
    CheckConstraint, create_engine
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError

# 1. Conexión a PostgreSQL (ajusta tu usuario y contraseña si es necesario)
DATABASE_URL = "postgresql+psycopg://postgres:123456789@localhost:5432/db_api_ia"

Base = declarative_base()

class Role(Base):
    __tablename__ = 'role'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rol_name = Column(String(50), nullable=False)


class User(Base):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    use_name = Column(String(100), nullable=False)
    use_email = Column(String(100), unique=True, nullable=False)
    use_career = Column(String(100))
    use_academic_level = Column(String(50))
    use_rol_id = Column(Integer, ForeignKey('role.id'), nullable=False)


class Application(Base):
    __tablename__ = 'application'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    app_name = Column(String(100), nullable=False)
    app_category = Column(String(100))
    app_link = Column(Text, nullable=False)
    app_description = Column(Text)
    app_source = Column(String(50))


class Interaction(Base):
    __tablename__ = 'interaction'

    id = Column(UUID(as_uuid=True), primary_key=True)
    int_use_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    int_app_id = Column(UUID(as_uuid=True), ForeignKey('application.id'), nullable=False)
    int_type = Column(String(50))
    int_timestamp = Column(DateTime, default=datetime.utcnow)


class Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(UUID(as_uuid=True), primary_key=True)
    fee_use_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    fee_app_id = Column(UUID(as_uuid=True), ForeignKey('application.id'), nullable=False)
    fee_rating = Column(Integer, CheckConstraint('fee_rating >= 1 AND fee_rating <= 5'))
    fee_comment = Column(Text)
    fee_date = Column(DateTime, default=datetime.utcnow)

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