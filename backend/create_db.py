from app.database import SessionLocal, engine
from app.models.models_sqlalchemy import Base, Role
import uuid

def init_db():
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Definir UUIDs fijos
        ADMIN_ID = uuid.UUID("fbfa60c1-288b-44b5-9eea-de384cc92a95")
        STUDENT_ID = uuid.UUID("d6d8d99a-e713-4d03-b2e2-6b66f05bdd6e")

        # Verificar si ya existen roles
        existing_roles = db.query(Role).count()
        if existing_roles == 0:
            admin_role = Role(id=ADMIN_ID, rol_name="Administrador")
            student_role = Role(id=STUDENT_ID, rol_name="Estudiante")
            db.add_all([admin_role, student_role])
            db.commit()
            print("✅ Roles con UUIDs fijos creados exitosamente.")
        else:
            print(f"ℹ️ Ya existen {existing_roles} roles. No se insertaron duplicados.")
    except Exception as e:
        print("❌ Error al insertar roles:", e)
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()