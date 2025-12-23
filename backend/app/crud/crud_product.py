from sqlmodel import Session, select
from typing import List, Optional

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def create_product(session: Session, product_in: ProductCreate) -> Product:
    product = Product.model_validate(product_in)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


def get_product(session: Session, product_id: int) -> Optional[Product]:
    return session.get(Product, product_id)


def get_products(session: Session, skip: int = 0, limit: int = 100) -> List[Product]:
    statement = select(Product).offset(skip).limit(limit)
    return session.exec(statement).all()


def get_products_by_category(session: Session, category_id: int, skip: int = 0, limit: int = 100) -> List[Product]:
    statement = (
        select(Product)
        .where(Product.category_id == category_id)
        .offset(skip)
        .limit(limit)
    )
    return session.exec(statement).all()


def update_product(session: Session, db_product: Product, product_in: ProductUpdate) -> Product:
    product_data = product_in.model_dump(exclude_unset=True)
    for key, value in product_data.items():
        setattr(db_product, key, value)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


def delete_product(session: Session, product_id: int) -> Optional[Product]:
    product = session.get(Product, product_id)
    if product:
        session.delete(product)
        session.commit()
    return product