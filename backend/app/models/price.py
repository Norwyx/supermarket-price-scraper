from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import UniqueConstraint, Index


class Price(SQLModel, table=True):
    """
    Represents a price of a product.
    """
    __tablename__ = "prices"
    __table_args__ = (
        UniqueConstraint("product_id", "supermarket_id", "scraped_at", name="uix_price_composite"),
        Index("idx_price_composite", "product_id", "supermarket_id", "scraped_at"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: Optional[int] = Field(index=True, default=None, foreign_key="products.id")
    supermarket_id: Optional[int] = Field(index=True, default=None, foreign_key="supermarkets.id")
    price: float = Field(index=True)
    url: Optional[str] = Field(default=None)
    original_price: Optional[float] = Field(default=None)
    scraped_at: datetime = Field(index=True, default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"Price(id={self.id}, product_id={self.product_id}, supermarket_id={self.supermarket_id}, price={self.price}, original_price={self.original_price}, url={self.url}, scraped_at={self.scraped_at})"

    class Config:
        json_schema_extra = {
            "example": {
                "product_id": 1,
                "supermarket_id": 1,
                "price": 1.99,
                "original_price": 2.99,
                "url": "https://supermarket.com/product/1",
                "scraped_at": "2022-01-01T00:00:00Z",
            }
        } 