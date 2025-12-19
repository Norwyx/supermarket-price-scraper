from sqlmodel import SQLModel, Field, Session, select
from typing import Optional, List
from datetime import datetime, timezone

from app.models.scraping_job import ScrapingJob, ScrapingJobStatus
from app.schemas.scraping_job import ScrapingJobCreate, ScrapingJobUpdate


def create_scraping_job(session: Session, job_in: ScrapingJobCreate) -> ScrapingJob:
    job = ScrapingJob.model_validate(job_in)
    session.add(job)
    session.commit()
    session.refresh(job)
    return job


def get_job(session: Session, job_id: int) -> Optional[ScrapingJob]:
    return session.get(ScrapingJob, job_id)


def get_jobs(session: Session, skip: int = 0, limit: int = 100) -> List[ScrapingJob]:
    statement = (
        select(ScrapingJob)
        .order_by(ScrapingJob.started_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return session.exec(statement).all()


def get_jobs_by_supermarket(session: Session, supermarket_id: int, skip: int = 0, limit: int = 10) -> List[ScrapingJob]:
    statement = (
        select(ScrapingJob)
        .where(ScrapingJob.supermarket_id == supermarket_id)
        .order_by(ScrapingJob.started_at.desc())
        .offset(skip) 
        .limit(limit)
    )
    return session.exec(statement).all()

def get_running_jobs(session: Session) -> List[ScrapingJob]:
    statement = select(ScrapingJob).where(
        ScrapingJob.status == ScrapingJobStatus.RUNNING
    )
    return session.exec(statement).all()


def update_job(session: Session, db_job: ScrapingJob, job_in: ScrapingJobUpdate) -> ScrapingJob:
    job_data = job_in.model_dump(exclude_unset=True)

    if job_in.status in [ScrapingJobStatus.COMPLETED, ScrapingJobStatus.FAILED]:
        if not db_job.completed_at:
            job_data["completed_at"] = datetime.now(timezone.utc)
    
    for key, value in job_data.items():
        setattr(db_job, key, value)
        
    session.add(db_job)
    session.commit()
    session.refresh(db_job)
    return db_job