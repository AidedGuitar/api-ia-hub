from sqlalchemy.orm import Session
from uuid import UUID
from app.models.interaction import Interaction
from app.schemas.interaction import InteractionCreate, InteractionUpdate


def get_interaction(db: Session, interaction_id: UUID) -> Interaction | None:
    return db.query(Interaction).filter(Interaction.id == interaction_id).first()


def get_interactions(db: Session, skip: int = 0, limit: int = 100) -> list[Interaction]:
    return db.query(Interaction).offset(skip).limit(limit).all()


def create_interaction(db: Session, interaction_in: InteractionCreate) -> Interaction:
    interaction = Interaction(**interaction_in.dict())
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return interaction


def update_interaction(db: Session, interaction_id: UUID, interaction_in: InteractionUpdate) -> Interaction | None:
    interaction = get_interaction(db, interaction_id)
    if not interaction:
        return None
    for field, value in interaction_in.dict(exclude_unset=True).items():
        setattr(interaction, field, value)
    db.commit()
    db.refresh(interaction)
    return interaction


def delete_interaction(db: Session, interaction_id: UUID) -> bool:
    interaction = get_interaction(db, interaction_id)
    if not interaction:
        return False
    db.delete(interaction)
    db.commit()
    return True