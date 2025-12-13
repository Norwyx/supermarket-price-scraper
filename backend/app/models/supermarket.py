from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional


class Supermarket(SQLModel, table=True):
    """
    Represents a competitor supermarket being tracked.
    """
    __tablename__ = "supermarkets"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, max_length=255)
    website_url: str = Field(max_length=500)
    logo_url: Optional[str] = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"Supermarket(id={self.id}, name='{self.name}')"

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Supermarket",
                "website_url": "https://supermarket.com",
            }
        }