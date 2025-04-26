from app.database import engine
from app.models import Base

def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ Base de datos y tablas creadas exitosamente.")

if __name__ == "__main__":
    init_db()
