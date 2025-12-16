from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import field_validator


class CategoryBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    slug: str = Field(max_length=255)
    image_url: Optional[str] = Field(default=None, max_length=500)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v_clean = v.strip()
        if len(v_clean) < 3:
            raise ValueError("Name must be at least 3 characters long")
        return v_clean
    
    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: str) -> str:
        v_clean = v.strip().lower() 
        if not re.match(r'^[a-z0-9-]+$', v_clean):
            raise ValueError("Slug must only contain lowercase letters, numbers, and hyphens")
        return v_clean


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int
    created_at: datetime


    class Config:
        from_attributes = True


class CategoryUpdate(SQLModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    slug: Optional[str] = Field(default=None, max_length=255)
    image_url: Optional[str] = Field(default=None, max_length=500)