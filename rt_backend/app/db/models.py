from sqlalchemy import Boolean, Column, Integer, String, Float, ForeignKey, Table, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base

# Association table for candidate and job matches
class CandidateJobMatch(Base):
    __tablename__ = "candidate_job_match"
    candidate_email = Column(String, ForeignKey("candidates.email"), primary_key=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), primary_key=True)
    jd_match_score = Column(Float)
    comparative_score = Column(Float)
    overall_score = Column(Float)
    salary_match_score = Column(Float)
    technical_match_score = Column(Float)
    experience_match_score = Column(Float)
    strengths = Column(Text)
    weaknesses = Column(Text)
    salary_analysis = Column(Text)
    recommendation = Column(Text)
    comparative_analysis = Column(Text)
    status = Column(String, default="active")  # active, saved, rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    candidate = relationship("Candidate", back_populates="job_matches")
    job = relationship("Job", back_populates="candidates")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # Relationships
    jobs = relationship("Job", back_populates="recruiter")

class Candidate(Base):
    __tablename__ = "candidates"

    email = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    resume_path = Column(String)
    resume_text = Column(Text)
    current_ctc = Column(Float)
    expected_ctc = Column(Float)
    additional_info = Column(Text)  # JSON string for additional Q&A
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    job_matches = relationship(
        "CandidateJobMatch",
        back_populates="candidate"
    )

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    jd_text = Column(Text)  # Extracted text from JD document
    min_budget = Column(Float)
    max_budget = Column(Float)
    status = Column(String, default="active")  # active, closed, draft
    
    # Foreign keys
    recruiter_id = Column(Integer, ForeignKey("users.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    recruiter = relationship("User", back_populates="jobs")
    candidates = relationship(
        "CandidateJobMatch",
        back_populates="job"
    ) 