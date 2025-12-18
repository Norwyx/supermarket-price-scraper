from sqlmodel import Session, select
from typing import List, Optional

from app.models.supermarket import Supermarket
from app.schemas.supermarket import SupermarketCreate, SupermarketUpdate


def create_supermarket(session: Session, supermarket_in: SupermarketCreate) -> Supermarket:
    supermarket = Supermarket.model_validate(supermarket_in)
    session.add(supermarket)
    session.commit()
    session.refresh(supermarket)
    return supermarket


def get_supermarket(session: Session, supermarket_id: int) -> Optional[Supermarket]:
    return session.get(Supermarket, supermarket_id)


def get_supermarkets(session: Session, skip: int = 0, limit: int = 100) -> List[Supermarket]:
    statement = select(Supermarket).offset(skip).limit(limit)
    return session.exec(statement).all()


def update_supermarket(session: Session, db_supermarket: Supermarket, supermarket_in: SupermarketUpdate) -> Supermarket:
    supermarket_data = supermarket_in.model_dump(exclude_unset=True)
    for key, value in supermarket_data.items():
        setattr(db_supermarket, key, value)
    session.add(db_supermarket)
    session.commit()
    session.refresh(db_supermarket)
    return db_supermarket


def delete_supermarket(session: Session, supermarket_id: int) -> Optional[Supermarket]:
    supermarket = session.get(Supermarket, supermarket_id)
    if supermarket:
        session.delete(supermarket)
        session.commit()
    return supermarket