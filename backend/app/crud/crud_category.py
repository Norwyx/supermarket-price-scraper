from sqlmodel import Session, select
from typing import List, Optional

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


def create_category(session: Session, category_in: CategoryCreate) -> Category:
    category = Category.model_validate(category_in)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


def get_category(session: Session, category_id: int) -> Optional[Category]:
    return session.get(Category, category_id)


def get_categories(session: Session, skip: int = 0, limit: int = 100) -> List[Category]:
    statement = select(Category).offset(skip).limit(limit)
    return session.exec(statement).all()


def update_category(session: Session, db_category: Category, category_in: CategoryUpdate) -> Category:
    category_data = category_in.model_dump(exclude_unset=True)
    for key, value in category_data.items():
        setattr(db_category, key, value)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


def delete_category(session: Session, category_id: int) -> Optional[Category]:
    category = session.get(Category, category_id)
    if category:
        session.delete(category)
        session.commit()
    return category