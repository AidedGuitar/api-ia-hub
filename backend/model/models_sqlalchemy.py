
from sqlalchemy import Column, String, Integer, Text, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()

class Role(Base):
    __tablename__ = 'role'

    rol_id = Column(Integer, primary_key=True, autoincrement=True)
    rol_name = Column(String(50), nullable=False)


class User(Base):
    __tablename__ = 'user'

    use_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    use_name = Column(String(100), nullable=False)
    use_email = Column(String(100), unique=True, nullable=False)
    use_career = Column(String(100))
    use_academic_level = Column(String(50))
    use_rol_id = Column(Integer, ForeignKey('role.rol_id'), nullable=False)


class Application(Base):
    __tablename__ = 'application'

    app_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    app_name = Column(String(100), nullable=False)
    app_category = Column(String(100))
    app_link = Column(Text, nullable=False)
    app_description = Column(Text)
    app_source = Column(String(50))


class Interaction(Base):
    __tablename__ = 'interaction'

    int_id = Column(Integer, primary_key=True, autoincrement=True)
    int_use_id = Column(UUID(as_uuid=True), ForeignKey('user.use_id'), nullable=False)
    int_app_id = Column(UUID(as_uuid=True), ForeignKey('application.app_id'), nullable=False)
    int_type = Column(String(50))
    int_timestamp = Column(DateTime, default=datetime.utcnow)


class Feedback(Base):
    __tablename__ = 'feedback'

    fee_id = Column(Integer, primary_key=True, autoincrement=True)
    fee_use_id = Column(UUID(as_uuid=True), ForeignKey('user.use_id'), nullable=False)
    fee_app_id = Column(UUID(as_uuid=True), ForeignKey('application.app_id'), nullable=False)
    fee_rating = Column(Integer, CheckConstraint('fee_rating >= 1 AND fee_rating <= 5'))
    fee_comment = Column(Text)
    fee_date = Column(DateTime, default=datetime.utcnow)
