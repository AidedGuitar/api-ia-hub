from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.models.interaction import InteractionType
from app.schemas.interaction import (InteractionCreate, InteractionRead, InteractionUpdate)
from app.services.interaction_service import (get_interaction, get_interactions, create_interaction, update_interaction, delete_interaction)
from app.core.dependencies import get_current_user, get_db
from app.models.user import User

router = APIRouter(
    prefix="/interactions",
    tags=["interactions"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/types", response_model=list[str])
def read_interaction_types():
    """
    Devuelve todos los valores posibles para el tipo de interacción.
    """
    return [member.value for member in InteractionType]

@router.get("/", response_model=list[InteractionRead])
def read_interactions(
    skip: int = 0, limit: int = 20,
    db: Session = Depends(get_db)
):
    return get_interactions(db, skip=skip, limit=limit)

@router.get("/{interaction_id}", response_model=InteractionRead)
def read_interaction(
    interaction_id: UUID,
    db: Session = Depends(get_db)
):
    interaction = get_interaction(db, interaction_id)
    if not interaction:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Interacción no encontrada")
    return interaction

@router.post(
    "/",
    response_model=InteractionRead,
    status_code=status.HTTP_201_CREATED
)
def create_interaction_endpoint(
    interaction_in: InteractionCreate,
    db: Session = Depends(get_db)
):
    return create_interaction(db, interaction_in)

@router.put("/{interaction_id}", response_model=InteractionRead)
def update_interaction_endpoint(
    interaction_id: UUID,
    interaction_in: InteractionUpdate,
    db: Session = Depends(get_db)
):
    interaction = update_interaction(db, interaction_id, interaction_in)
    if not interaction:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Interacción no encontrada")
    return interaction

@router.delete("/{interaction_id}", status_code=status.HTTP_200_OK)
def delete_interaction_endpoint(
    interaction_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    success = delete_interaction(db, interaction_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interacción no encontrada"
        )
    return {"message": "Interacción eliminada correctamente"}