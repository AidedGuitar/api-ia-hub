from sqlalchemy.orm import Session
from uuid import UUID
from app.models.application import Application
from app.schemas.application import ApplicationCreate, ApplicationUpdate

def get_app(db: Session, app_id: UUID) -> Application | None:
    return db.query(Application).filter(Application.id == app_id).first()

def get_apps(db: Session, skip: int = 0, limit: int = 100) -> list[Application]:
    return db.query(Application).offset(skip).limit(limit).all()

def create_app(db: Session, app_in: ApplicationCreate) -> Application:
    app = Application(**app_in.dict())
    db.add(app)
    db.commit()
    db.refresh(app)
    return app

def update_app(db: Session, app_id: UUID, app_in: ApplicationUpdate) -> Application | None:
    app = get_app(db, app_id)
    if not app:
        return None
    for field, value in app_in.dict(exclude_unset=True).items():
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
