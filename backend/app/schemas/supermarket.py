from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import field_validator


class SupermarketBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    website_url: str = Field(max_length=500)
    logo_url: Optional[str] = Field(default=None, max_length=500)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v_clean = v.strip()
        if len(v_clean) < 2:
            raise ValueError("Name must be at least 2 characters long")
        return v_clean

    @field_validator("website_url")
    @classmethod
    def validate_website_url(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("URL cannot be empty")
        if not (v.startswith("http://") or v.startswith("https://")):
            raise ValueError("URL must start with http:// or https://")
        return v


class SupermarketCreate(SupermarketBase):
    pass


class SupermarketRead(SupermarketBase):
    id: int
    created_at: datetime


    class Config:
        from_attributes = True


class SupermarketUpdate(SQLModel):
    name: Optional[str] = Field(default=None, min_length=1)
    website_url: Optional[str] = None
    logo_url: Optional[str] = None
