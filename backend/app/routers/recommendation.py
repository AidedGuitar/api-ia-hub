from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user
from app.database import get_db
from app.recommender.predictor import ContentBasedRecommender

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.get("/")
def get_recommendations(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    recommender = ContentBasedRecommender(db)
    recommendations = recommender.recommend(user_id=current_user.id, top_n=5)
    return {
        "user_id": current_user.id,
        "recommendations": recommendations
    }