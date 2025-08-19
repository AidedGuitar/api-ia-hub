from sqlalchemy.orm import Session
from uuid import UUID
from sqlalchemy import func
from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate, FeedbackUpdate

def get_feedback_by_user_app(db: Session, user_id: UUID, app_id: UUID) -> Feedback | None:
    return db.query(Feedback).filter(
        Feedback.fee_use_id == user_id,
        Feedback.fee_app_id == app_id
    ).first()

def get_feedback(db: Session, feedback_id: UUID) -> Feedback | None:
    return db.query(Feedback).filter(Feedback.id == feedback_id).first()


def get_feedbacks(db: Session, skip: int = 0, limit: int = 100) -> list[Feedback]:
    return db.query(Feedback).offset(skip).limit(limit).all()


def create_feedback(db: Session, feedback_in: FeedbackCreate) -> Feedback:
    feedback = Feedback(**feedback_in.dict())
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback


def update_feedback(db: Session, feedback_id: UUID, feedback_in: FeedbackUpdate) -> Feedback | None:
    feedback = get_feedback(db, feedback_id)
    if not feedback:
        return None
    for field, value in feedback_in.dict(exclude_unset=True).items():
        setattr(feedback, field, value)
    db.commit()
    db.refresh(feedback)
    return feedback


def delete_feedback(db: Session, feedback_id: UUID) -> bool:
    feedback = get_feedback(db, feedback_id)
    if not feedback:
        return False
    db.delete(feedback)
    db.commit()
    return True


def get_app_rating(db: Session, app_id: UUID) -> dict:
    result = db.query(
        func.avg(Feedback.fee_rating).label('average'),
        func.count(Feedback.fee_rating).label('count')
    ).filter(Feedback.fee_app_id == app_id).one()
    return {
        'average': float(result.average or 0),
        'count': int(result.count)
    }