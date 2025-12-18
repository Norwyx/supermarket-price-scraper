from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from sqlalchemy import func, Column, DateTime


class Category(SQLModel, table=True):
    """
    Represents a category of products being tracked.
    """
    __tablename__ = "categories"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=255)
    slug: str = Field(index=True, unique=True, max_length=255)
    image_url: Optional[str] = Field(default=None, max_length=500)
    parent_id: Optional[int] = Field(default=None, foreign_key="categories.id", index=True)
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), 
            server_default=func.now(),
            nullable=False
        )
    )
    
    def __repr__(self) -> str:
        return f"Category(id={self.id}, name='{self.name}')"

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Fruits",
                "slug": "fruits",
                "image_url": "https://image.similarpng.com/file/similarpng/original-picture/2020/08/Group-of-fresh-fruits-on-transparent-background-PNG.png",
            }
        }