from app.database import SessionLocal
from sqlalchemy.orm import Session

# Dependency para obtener la sesión de la base de datos
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
