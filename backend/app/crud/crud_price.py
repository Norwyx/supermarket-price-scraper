from sqlmodel import Session, select
from typing import List, Optional

from app.models.price import Price
from app.schemas.price import PriceCreate


def create_price(session: Session, price_in: PriceCreate) -> Price:
    price = Price.model_validate(price_in)
    session.add(price)
    session.commit()
    session.refresh(price)
    return price


def get_prices_by_product(session: Session, product_id: int) -> List[Price]:
    statement = (
        select(Price)
        .where(Price.product_id == product_id)
        .order_by(Price.created_at.desc())
    )
    return session.exec(statement).all()