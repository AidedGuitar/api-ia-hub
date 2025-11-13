from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.models.user import User
from app.schemas.feedback import FeedbackCreate, FeedbackRead, FeedbackUpdate
from app.services.feedback_service import (
    get_feedback, get_feedbacks,
    create_feedback, update_feedback, delete_feedback,
    get_app_rating, get_feedback_by_user_app
)
from app.core.dependencies import get_current_user, get_db

router = APIRouter(
    prefix="/feedback",
    tags=["feedback"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/", response_model=list[FeedbackRead])
def read_all_feedbacks(
    skip: int = 0, limit: int = 20,
    db: Session = Depends(get_db)
):
    return get_feedbacks(db, skip=skip, limit=limit)

@router.get("/{feedback_id}", response_model=FeedbackRead)
def read_feedback(
    feedback_id: UUID,
    db: Session = Depends(get_db)
):
    fb = get_feedback(db, feedback_id)
    if not fb:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Feedback no encontrado")
    return fb

@router.post(
    "/",
    response_model=FeedbackRead,
    status_code=status.HTTP_201_CREATED
)
def create_feedback_endpoint(
    feedback_in: FeedbackCreate,
    db: Session = Depends(get_db)
):
     # Validar unicidad: un feedback por usuario-app
    existing = get_feedback_by_user_app(db, feedback_in.user_id, feedback_in.application_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El feedback para este usuario y aplicación ya existe"
        )
    
    return create_feedback(db, feedback_in)

@router.put("/{feedback_id}", response_model=FeedbackRead)
def update_feedback_endpoint(
    feedback_id: UUID,
    feedback_in: FeedbackUpdate,
    db: Session = Depends(get_db)
):
    fb = update_feedback(db, feedback_id, feedback_in)
    if not fb:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Feedback no encontrado")
    return fb

@router.delete("/{feedback_id}", status_code=status.HTTP_200_OK)
def delete_feedback_endpoint(
    feedback_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    success = delete_feedback(db, feedback_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback no encontrado"
        )
    return {"message": "Interacción eliminada correctamente"}

@router.get("/app/{app_id}/rating")
def read_app_rating(
    app_id: UUID,
    db: Session = Depends(get_db)
):
    return get_app_rating(db, app_id)