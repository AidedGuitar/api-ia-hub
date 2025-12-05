from sqlalchemy.orm import Session
from uuid import UUID
from app.models.application import Application
from app.schemas.application import ApplicationCreate, ApplicationUpdate
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from app.models.models_sqlalchemy import Feedback

def get_app(db: Session, app_id: UUID) -> Application | None:
    app = db.query(Application).filter(Application.id == app_id).first()
    if not app:
        return None

    avg_rating = get_app_avg_rating(db, app_id)

    print("resultados pochos: ",avg_rating)
    # Adjuntar dinámicamente el valor
    app.avg_rating = avg_rating

    return app

def get_apps(db: Session, skip: int = 0, limit: int = 100) -> list[Application]:
    apps = db.query(Application).offset(skip).limit(limit).all()

    for app in apps:
        avg_rating = get_app_avg_rating(db, app.id)
        app.avg_rating = avg_rating
        print("resultados pochos: ",avg_rating)  

    return apps

def create_app(db: Session, app_in: ApplicationCreate) -> Application:
    app = Application(**app_in.model_dump())
    db.add(app)
    try:
        db.commit()
        db.refresh(app)
        return app
    except IntegrityError as e:
        db.rollback()
        raise e  # 🚨 Solo propaga el error, no lo convierte en HTTPException

def update_app(db: Session, app_id: UUID, app_in: ApplicationUpdate) -> Application | None:
    app = get_app(db, app_id)
    if not app:
        return None
    for field, value in app_in.model_dump(exclude_unset=True).items():
        setattr(app, field, value)
    db.commit()
    db.refresh(app)
    return app

def delete_app(db: Session, app_id: UUID) -> bool:
    app = get_app(db, app_id)
    if not app:
        return False
    db.delete(app)
    db.commit()
    return True

def get_app_avg_rating(db: Session, app_id: UUID) -> float:
    result = db.query(
        func.avg(Feedback.fee_rating),
        func.count(Feedback.fee_rating)
    ).filter(Feedback.application_id == app_id).one()

    avg = result[0]  # EL PROMEDIO
    return float(avg) if avg is not None else 0.0


