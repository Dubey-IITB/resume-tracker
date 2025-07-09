from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

from app.schemas.candidate import Candidate, CandidateWithScores

# Shared properties
class JobBase(BaseModel):
    title: str
    description: Optional[str] = None
    min_budget: Optional[float] = None
    max_budget: Optional[float] = None
    status: str = "active"

# Properties to receive on job creation
class JobCreate(JobBase):
    pass

# Properties to receive on job update
class JobUpdate(JobBase):
    title: Optional[str] = None

# Properties to return to client
class JobInDBBase(JobBase):
    id: int
    recruiter_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# Additional properties to return via API
class Job(JobInDBBase):
    pass

# Additional properties stored in DB
class JobInDB(JobInDBBase):
    jd_text: str

# Properties for job with candidates
class JobWithCandidates(Job):
    candidates: Optional[List[CandidateWithScores]] = None

# Properties for matched candidate results
class CandidateMatchResults(BaseModel):
    job_id: int
    jd_matches: List[CandidateWithScores]
    comparative_matches: List[CandidateWithScores]