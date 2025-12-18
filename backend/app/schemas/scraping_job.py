from enum import Enum
from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel
from pydantic import field_validator


class JobStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class ScrapingJobBase(SQLModel):
    supermarket_id: int = Field(gt=0)
    status: JobStatus = JobStatus.PENDING
    products_scraped: int = 0
    errors_count: int = 0
    error_message: Optional[str] = None

    @field_validator("products_scraped", "errors_count")
    @classmethod
    def validate_counts(cls, v: int) -> int:
        if v < 0:
            raise ValueError("Counters cannot be negative")
        return v

    @field_validator("error_message")
    @classmethod
    def clean_error_message(cls, v: Optional[str]) -> Optional[str]:
        if v:
            return v.strip()
        return v


class ScrapingJobCreate(ScrapingJobBase):
    pass   


class ScrapingJobRead(ScrapingJobBase):
    id: int
    started_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ScrapingJobUpdate(SQLModel):
    status: Optional[JobStatus] = None
    products_scraped: Optional[int] = None
    errors_count: Optional[int] = None
    error_message: Optional[str] = None
    completed_at: Optional[datetime] = None