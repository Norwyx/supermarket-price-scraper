from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from pydantic import field_validator


class ProductBase(SQLModel):
    name: str = Field(max_length=500)
    variant: Optional[str] = None
    sku: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = None
    image_url: Optional[str] = Field(default=None, max_length=500)
    category_id: int = Field(gt=0)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v_clean = v.strip()
        if len(v_clean) < 2:
            raise ValueError("Name must be at least 2 characters long")
        return v_clean
    

    @field_validator("sku")
    @classmethod
    def validate_sku(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v_clean = v.upper().strip()
        if not v_clean:
            raise ValueError("SKU cannot be an empty string")
        return v_clean

class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductUpdate(SQLModel):
    name: Optional[str] = Field(default=None, max_length=500)
    variant: Optional[str] = None
    sku: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = None
    image_url: Optional[str] = Field(default=None, max_length=500)
    supermarket_id: Optional[int] = Field(default=None, gt=0)
    category_id: Optional[int] = Field(default=None, gt=0)