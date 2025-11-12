from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.models.user import CareerType


router = APIRouter(prefix="/career", tags=["career"], dependencies=[Depends(get_current_user)])

@router.get("/types", response_model=list[str])
def read_interaction_types():
    """
    Devuelve todos los valores posibles para el tipo de carrera.
    """
    return [career.value for career in CareerType]