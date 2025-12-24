from typing import Optional, List
from sqlmodel import SQLModel, Field
from datetime import datetime
from pydantic import field_validator, BaseModel


class PriceBase(SQLModel):
    product_id: int = Field(gt=0)
    supermarket_id: int = Field(gt=0)
    price: float = Field(ge=0)
    url: Optional[str] = Field(default=None, max_length=500)
    original_price: Optional[float] = Field(default=None, ge=0)
    scraped_at: Optional[datetime] = None

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("URL cannot be empty")
        if not (v.startswith("http://") or v.startswith("https://")):
            raise ValueError("URL must start with http:// or https://")
        return v


class PriceCreate(PriceBase):
    pass


class PriceRead(PriceBase):
    id: int
    scraped_at: datetime

    class Config:
        from_attributes = True


class PriceUpdate(SQLModel):
    product_id: Optional[int] = None
    supermarket_id: Optional[int] = None
    price: Optional[float] = None
    url: Optional[str] = None
    original_price: Optional[float] = None
    scraped_at: Optional[datetime] = None


class PriceComparisonItem(BaseModel):
    supermarket_id: int
    supermarket_name: str
    price: float
    url: Optional[str]
    is_cheapest: bool
    scraped_at: datetime


class PriceComparison(BaseModel):
    product_id: int
    product_name: str
    prices: List[PriceComparisonItem]
    cheapest_price: float
    most_expensive_price: float
    price_difference: float
    savings_percentage: float


class CompareBulkRequest(BaseModel):
    product_ids: List[int]