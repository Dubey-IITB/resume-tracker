from typing import Optional, Dict, Any, List
from pydantic import BaseModel, EmailStr
from datetime import datetime

# Shared properties
class CandidateBase(BaseModel):
    name: str
    email: EmailStr
    current_ctc: float
    expected_ctc: float
    additional_info: Optional[Dict[str, Any]] = None

# Properties to receive on candidate creation
class CandidateCreate(CandidateBase):
    pass

# Properties to receive on candidate update
class CandidateUpdate(CandidateBase):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    current_ctc: Optional[float] = None
    expected_ctc: Optional[float] = None

# Properties to return to client
class CandidateInDBBase(CandidateBase):
    email: EmailStr
    resume_path: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Additional properties to return via API
class Candidate(CandidateInDBBase):
    pass

# Additional properties stored in DB
class CandidateInDB(CandidateInDBBase):
    resume_text: str

# Properties for candidate with match scores
class CandidateWithScores(Candidate):
    jd_match_score: Optional[float] = None
    comparative_score: Optional[float] = None 