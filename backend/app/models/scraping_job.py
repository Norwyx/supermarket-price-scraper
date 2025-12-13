from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional
from enum import Enum


class ScrapingJobStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class ScrapingJob(SQLModel, table=True):
    """
    Represents a scraping job.
    """
    __tablename__ = "scraping_jobs"

    id: Optional[int] = Field(default=None, primary_key=True)
    supermarket_id: Optional[int] = Field(index=True, default=None, foreign_key="supermarkets.id")
    status: ScrapingJobStatus = Field(index=True, default=ScrapingJobStatus.PENDING)
    started_at: datetime = Field(index=True,default_factory=datetime.utcnow)
    completed_at: datetime = Field(default_factory=datetime.utcnow)
    products_scraped: Optional[int] = Field(default=0)
    errors_count: Optional[int] = Field(default=0)
    error_message: Optional[str] = Field(default=None)
    
    def __repr__(self) -> str:
        return f"ScrapingJob(id={self.id}, supermarket_id={self.supermarket_id}, products_scraped={self.products_scraped}, errors_count={self.errors_count}, error_message={self.error_message})"

    class Config:
        json_schema_extra = {
            "example": {
                "supermarket_id": 1,
                "products_scraped": 1,
                "errors_count": 0,
                "error_message": "No errors",
            }
        }