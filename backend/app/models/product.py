from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from sqlalchemy import func, Column, DateTime


class Product(SQLModel, table=True):
    """
    Represents a product being tracked.
    """
    __tablename__ = "products"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=500)
    variant: Optional[str] = Field(default=None, max_length=500)
    sku: Optional[str] = Field(index=True, unique=True, default=None, max_length=100)
    description: Optional[str] = Field(default=None)
    image_url: Optional[str] = Field(default=None, max_length=500)
    category_id: int = Field(index=True, foreign_key="categories.id")
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), 
            server_default=func.now(),
            nullable=False
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), 
            server_default=func.now(), 
            onupdate=func.now(),       
            nullable=False
        )
    )
    
    def __repr__(self) -> str:
        return f"Product(id={self.id}, name='{self.name}')"

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Milk",
                "variant": "1L",
                "sku": "205683475",
                "description": "Milk description and additional details",
                "image_url": "https://w7.pngwing.com/pngs/600/735/png-transparent-coffee-milk-milk-bottle-milk-thumbnail.png",
            }
        }