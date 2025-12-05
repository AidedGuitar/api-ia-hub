from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Dict
from app.core.dependencies import get_db, get_current_user
from app.recommender.predictor import ContentBasedRecommender

router = APIRouter(prefix="/recommendations", tags=["recommender"])

@router.get("/", response_model=List[Dict])
def get_recommendations(limit: int = Query(4, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    rec = ContentBasedRecommender(db)  # en prod -> cachear la instancia
    results = rec.recommend(str(current_user.id), top_n=limit)
    return results
