import os
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Cargar variables del archivo .env (por ejemplo, DATABASE_URL)
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Leer la URL de conexión desde el .env
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está definida en el archivo .env")

# Crear el motor y la sesión
engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función que inyecta la sesión en dependencias FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()