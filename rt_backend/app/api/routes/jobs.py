from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.db import models

router = APIRouter()


# --- Pydantic schemas ---

class JobCreate(BaseModel):
    title: str
    description: Optional[str] = None
    min_budget: Optional[float] = None
    max_budget: Optional[float] = None
    status: Optional[str] = "active"


class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    min_budget: Optional[float] = None
    max_budget: Optional[float] = None
    status: Optional[str] = None


# --- Helper ---

def _job_to_dict(job: models.Job) -> dict:
    return {
        "id": job.id,
        "title": job.title,
        "description": job.description,
        "min_budget": job.min_budget,
        "max_budget": job.max_budget,
        "status": job.status,
        "recruiter_id": job.recruiter_id,
        "created_at": job.created_at.isoformat() if job.created_at else None,
        "updated_at": job.updated_at.isoformat() if job.updated_at else None,
    }


# --- Routes ---

@router.get("/test")
def test_jobs():
    return {"message": "Jobs route is working"}


@router.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):
    """List all jobs."""
    jobs = db.query(models.Job).order_by(models.Job.created_at.desc()).all()
    return [_job_to_dict(j) for j in jobs]


@router.post("/jobs")
def create_job(job_in: JobCreate, db: Session = Depends(get_db)):
    """Create a new job."""
    job = models.Job(
        title=job_in.title,
        description=job_in.description,
        min_budget=job_in.min_budget,
        max_budget=job_in.max_budget,
        status=job_in.status or "active",
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return _job_to_dict(job)


@router.get("/jobs/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):
    """Get a single job by ID."""
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return _job_to_dict(job)


@router.put("/jobs/{job_id}")
def update_job(job_id: int, job_in: JobUpdate, db: Session = Depends(get_db)):
    """Update an existing job."""
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    update_data = job_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(job, field, value)

    db.commit()
    db.refresh(job)
    return _job_to_dict(job)


@router.delete("/jobs/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    """Delete a job."""
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    db.delete(job)
    db.commit()
    return {"message": "Job deleted successfully"}