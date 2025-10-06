"""
Script para generar datos de prueba en la base de datos.
Ejecutar desde la raíz del backend: `python seed_data.py`
"""

import uuid
from datetime import datetime, timedelta
from random import choice, randint, sample

from app.database import SessionLocal, engine
from app.models.models_sqlalchemy import Base, User, Application, Interaction, Feedback, Role
from app.auth.password_handler import hash_password

# Crear todas las tablas si no existen
Base.metadata.create_all(bind=engine)

# UUIDs fijos para roles (deben coincidir con create_db.py)
ADMIN_ROLE_ID = uuid.UUID("fbfa60c1-2888-44b5-9eea-de384cc92a95")
STUDENT_ROLE_ID = uuid.UUID("d6d8d99a-e713-4d03-b2e2-6b66f05bdd6e")

def create_roles(db):
    """Asegura que los roles existan."""
    if not db.query(Role).filter(Role.id == ADMIN_ROLE_ID).first():
        admin_role = Role(id=ADMIN_ROLE_ID, rol_name="Administrador")
        db.add(admin_role)
    if not db.query(Role).filter(Role.id == STUDENT_ROLE_ID).first():
        student_role = Role(id=STUDENT_ROLE_ID, rol_name="Estudiante")
        db.add(student_role)
    db.commit()

def create_applications(db):
    """Crea un catálogo de materias/aplicaciones realistas."""
    applications_data = [
        {
            "name": "Cálculo Diferencial",
            "category": "Matemáticas",
            "description": "Fundamentos del cálculo: límites, derivadas e integrales.",
            "keywords": "matemáticas, cálculo, derivadas, límites, funciones",
            "academic_level": "Primer semestre",
            "credits": 4
        },
        {
            "name": "Programación I",
            "category": "Ingeniería de Sistemas",
            "description": "Introducción a la programación con Python.",
            "keywords": "programación, python, algoritmos, lógica, desarrollo",
            "academic_level": "Primer semestre",
            "credits": 3
        },
        {
            "name": "Álgebra Lineal",
            "category": "Matemáticas",
            "description": "Vectores, matrices, sistemas de ecuaciones y espacios vectoriales.",
            "keywords": "matemáticas, matrices, vectores, álgebra, ecuaciones",
            "academic_level": "Segundo semestre",
            "credits": 3
        },
        {
            "name": "Estructuras de Datos",
            "category": "Ingeniería de Sistemas",
            "description": "Listas, pilas, colas, árboles y grafos.",
            "keywords": "programación, estructuras, árboles, grafos, algoritmos",
            "academic_level": "Tercer semestre",
            "credits": 4
        },
        {
            "name": "Física Mecánica",
            "category": "Física",
            "description": "Cinemática, dinámica y energía.",
            "keywords": "física, mecánica, movimiento, fuerza, energía",
            "academic_level": "Primer semestre",
            "credits": 4
        },
        {
            "name": "Bases de Datos",
            "category": "Ingeniería de Sistemas",
            "description": "Modelado, SQL y administración de bases de datos relacionales.",
            "keywords": "bases de datos, SQL, modelado, PostgreSQL, MySQL",
            "academic_level": "Cuarto semestre",
            "credits": 3
        },
        {
            "name": "Inteligencia Artificial",
            "category": "Ingeniería de Sistemas",
            "description": "Fundamentos de IA: algoritmos de búsqueda, redes neuronales y aprendizaje automático.",
            "keywords": "IA, machine learning, redes neuronales, algoritmos, inteligencia",
            "academic_level": "Sexto semestre",
            "credits": 4
        },
        {
            "name": "Redes de Computadores",
            "category": "Ingeniería de Sistemas",
            "description": "Protocolos, arquitectura TCP/IP y seguridad en redes.",
            "keywords": "redes, TCP/IP, protocolos, internet, seguridad",
            "academic_level": "Quinto semestre",
            "credits": 3
        }
    ]

    for app_data in applications_data:
        app = Application(
            id=uuid.uuid4(),
            app_name=app_data["name"],
            app_category=app_data["category"],
            app_link="https://universidad.edu/materias",
            app_description=app_data["description"],
            app_source="manual",
            app_keywords=app_data["keywords"],
            app_academic_level=app_data["academic_level"],
            app_credits=app_data["credits"]
        )
        db.add(app)
    db.commit()
    print(f"✅ {len(applications_data)} materias creadas.")

def create_users(db):
    """Crea usuarios de prueba (1 admin, 5 estudiantes)."""
    # Usuario administrador
    admin = User(
        id=uuid.uuid4(),
        use_name="Admin User",
        use_email="admin@universidad.edu.co",
        use_career="Administración",
        use_academic_level="Profesional",
        use_rol_id=ADMIN_ROLE_ID,
        auth_provider="local",
        hashed_password=hash_password("admin123")
    )
    db.add(admin)

    # Usuarios estudiantes
    careers = ["Ingeniería de Sistemas", "Matemáticas", "Física", "Ingeniería Electrónica"]
    academic_levels = ["Primer semestre", "Segundo semestre", "Tercer semestre"]

    for i in range(1, 6):
        student = User(
            id=uuid.uuid4(),
            use_name=f"Estudiante {i}",
            use_email=f"estudiante{i}@universidad.edu.co",
            use_career=choice(careers),
            use_academic_level=choice(academic_levels),
            use_rol_id=STUDENT_ROLE_ID,
            auth_provider="local",
            hashed_password=hash_password("student123")
        )
        db.add(student)
    db.commit()
    print("✅ 1 administrador y 5 estudiantes creados.")

def create_interactions_and_feedback(db):
    """Genera interacciones y retroalimentación simuladas."""
    users = db.query(User).filter(User.use_rol_id == STUDENT_ROLE_ID).all()
    applications = db.query(Application).all()

    interaction_types = ["view", "click", "favorite"]

    for user in users:
        # Seleccionar 3-5 materias aleatorias para interactuar
        selected_apps = sample(applications, k=randint(3, 5))
        for app in selected_apps:
            # Registrar una interacción
            interaction = Interaction(
                id=uuid.uuid4(),
                user_id=user.id,
                application_id=app.id,
                int_type=choice(interaction_types),
                int_timestamp=datetime.utcnow() - timedelta(days=randint(0, 30))
            )
            db.add(interaction)

            # Registrar retroalimentación (rating 4 o 5 para simular interés)
            if choice([True, False]):  # 50% de probabilidad
                feedback = Feedback(
                    id=uuid.uuid4(),
                    user_id=user.id,
                    application_id=app.id,
                    fee_rating=randint(4, 5),
                    fee_comment="Muy útil para mi carrera."
                )
                db.add(feedback)
    db.commit()
    print(f"✅ Interacciones y retroalimentación generadas para {len(users)} estudiantes.")

def main():
    db = SessionLocal()
    try:
        print("🌱 Iniciando la generación de datos de prueba...")
        create_roles(db)
        create_applications(db)
        create_users(db)
        create_interactions_and_feedback(db)
        print("🎉 Datos de prueba generados exitosamente.")
    except Exception as e:
        print(f"❌ Error al generar datos: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()