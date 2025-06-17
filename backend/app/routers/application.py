from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas.application import (ApplicationCreate, ApplicationRead, ApplicationUpdate)
from app.services.app_service import (get_app, get_apps, create_app, update_app, delete_app)
from app.core.dependencies import get_db

router = APIRouter(
    prefix="/apps",
    tags=["applications"]
)

@router.get("/", response_model=list[ApplicationRead])
def read_apps(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return get_apps(db, skip, limit)

@router.get("/{app_id}", response_model=ApplicationRead)
def read_app(app_id: UUID, db: Session = Depends(get_db)):
    app = get_app(db, app_id)
    if not app:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Aplicación no encontrada")
    return app

@router.post(
    "/",
    response_model=ApplicationRead,
    status_code=status.HTTP_201_CREATED
)
def create_application(
    app_in: ApplicationCreate,
    db: Session = Depends(get_db)
):
    # Aquí podrías validar app_source en {"manual","ia"} si quieres
    return create_app(db, app_in)

@router.put("/{app_id}", response_model=ApplicationRead)
def update_application(
    app_id: UUID,
    app_in: ApplicationUpdate,
    db: Session = Depends(get_db)
):
    app = update_app(db, app_id, app_in)
    if not app:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Aplicación no encontrada")
    return app

@router.delete("/{app_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(app_id: UUID, db: Session = Depends(get_db)):
    success = delete_app(db, app_id)
    if not success:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Aplicación no encontrada")
