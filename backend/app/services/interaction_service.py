from sqlalchemy.orm import Session
from uuid import UUID
from app.models.interaction import Interaction
from app.schemas.interaction import InteractionCreate, InteractionUpdate
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from fastapi import HTTPException, status
from app.models.application import Application



def get_interaction(db: Session, interaction_id: UUID) -> Interaction | None:
    return db.query(Interaction).filter(Interaction.id == interaction_id).first()


def get_interactions(db: Session, skip: int = 0, limit: int = 100) -> list[Interaction]:
    return db.query(Interaction).offset(skip).limit(limit).all()


def create_interaction(db: Session, interaction_in: InteractionCreate) -> Interaction:
    # Validar existencia del usuario
    user = db.query(User).filter(User.id == interaction_in.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El usuario con ID {interaction_in.user_id} no existe"
        )

    # Validar existencia de la aplicación
    app = db.query(Application).filter(Application.id == interaction_in.application_id).first()
    if not app:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La aplicación con ID {interaction_in.application_id} no existe"
        )
        
    # Crear la interacción
    interaction = Interaction(**interaction_in.dict())    
    db.add(interaction)
    try:
        db.commit()
        db.refresh(interaction)
        return interaction
    except IntegrityError:
        db.rollback()
        raise  # dejamos que el router maneje este error


def update_interaction(db: Session, interaction_id: UUID, interaction_in: InteractionUpdate) -> Interaction | None:
    interaction = get_interaction(db, interaction_id)
    if not interaction:
        return None
    for field, value in interaction_in.dict(exclude_unset=True).items():
        setattr(interaction, field, value)
    db.commit()
    db.refresh(interaction)
    return interaction


def delete_interaction(db: Session, interaction_id: UUID, current_user_id: UUID) -> bool:
    interaction = db.query(Interaction).filter(
        Interaction.id == interaction_id,
        Interaction.user_id == current_user_id  # Solo suyas
    ).first()
    if not interaction:
        return False
    db.delete(interaction)
    db.commit()
    return True