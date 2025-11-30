"""
Script para generar datos de prueba en la base de datos.
Ejecutar desde la raíz del backend: `python seed_data.py`
"""

import uuid
from datetime import datetime, timedelta
from random import choice, randint, sample
from database import SessionLocal, engine
from models.models_sqlalchemy import Base, User, Application, Interaction, Feedback, Role
from auth.password_handler import hash_password

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
            "app_name": "Khan Academy",
            "app_description": "Plataforma educativa gratuita con cursos en matemáticas, ciencias y más.",
            "app_link": "https://www.khanacademy.org",
            "app_academic_level": "Universitario",
            "app_keywords": "matemáticas, ciencias, fundamentos, autodidacta",
            "app_category": "STEM"
        },
        {
            "app_name": "Coursera",
            "app_description": "Cursos online dictados por universidades y empresas líderes en el mundo.",
            "app_link": "https://www.coursera.org",
            "app_academic_level": "Universitario",
            "app_keywords": "cursos online, certificaciones, profesional",
            "app_category": "Cursos"
        },
        {
            "app_name": "Duolingo",
            "app_description": "Aplicación gamificada para aprender idiomas de forma divertida.",
            "app_link": "https://www.duolingo.com",
            "app_academic_level": "Todos",
            "app_keywords": "idiomas, gamificación, aprendizaje rápido",
            "app_category": "Idiomas"
        },
        {
            "app_name": "Notion",
            "app_description": "Herramienta de organización, apuntes y productividad para estudiantes.",
            "app_link": "https://www.notion.so",
            "app_academic_level": "Universitario",
            "app_keywords": "productividad, notas, organización",
            "app_category": "Productividad"
        },
        {
            "app_name": "Brilliant",
            "app_description": "Cursos interactivos para aprender matemáticas, lógica y ciencias.",
            "app_link": "https://www.brilliant.org",
            "app_academic_level": "Pregrado",
            "app_keywords": "lógica, matemáticas, ciencias, interactivo",
            "app_category": "STEM"
        },
        {
            "app_name": "Wolfram Alpha",
            "app_description": "Motor de conocimiento computacional para resolver problemas complejos.",
            "app_link": "https://www.wolframalpha.com",
            "app_academic_level": "Universitario",
            "app_keywords": "cálculo, ecuaciones, álgebra, ingeniería",
            "app_category": "Ciencia y Tecnología"
        },
        {
            "app_name": "Google Classroom",
            "app_description": "Plataforma para gestionar cursos, tareas y comunicación académica.",
            "app_link": "https://classroom.google.com",
            "app_academic_level": "Escolar",
            "app_keywords": "tareas, clases, gestión educativa",
            "app_category": "Educación"
        },
        {
            "app_name": "Blinkist",
            "app_description": "Resúmenes de libros de no ficción en formato audio y texto.",
            "app_link": "https://www.blinkist.com",
            "app_academic_level": "Universitario",
            "app_keywords": "resúmenes, lectura rápida, aprendizaje continuo",
            "app_category": "Lectura"
        }
    ]



    for app_data in applications_data:
        app = Application(
            id=uuid.uuid4(),
            app_name=app_data["app_name"],
            app_category=app_data["app_category"],
            app_link=app_data["app_link"],
            app_description=app_data["app_description"],
            app_source="manual",
            app_keywords=app_data["app_keywords"],
            app_academic_level=app_data["app_academic_level"]
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
        hashed_password=hash_password("Admin123456")
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
            hashed_password=hash_password("Student1234858")
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
    except Exception as e:
        print(f"❌ Error al generar datos: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()