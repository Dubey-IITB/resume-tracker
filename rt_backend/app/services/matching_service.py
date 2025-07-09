import json
import os
from typing import Dict, List, Tuple

from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models import Candidate, Job, CandidateJobMatch
from app.schemas.candidate import CandidateWithScores
from app.services.ollama_service import OllamaClient

# Initialize Ollama client
ollama_client = OllamaClient()

def compare_candidate_with_jd(candidate: Candidate, job: Job) -> float:
    """
    Compare a candidate with a job description using LLM and return a match score.
    """
    # Parse candidate's additional info
    additional_info = {}
    if candidate.additional_info:
        try:
            additional_info = json.loads(candidate.additional_info)
        except:
            additional_info = {"data": candidate.additional_info}
    
    # Prepare candidate info as dictionary
    candidate_info = {
        "id": candidate.id,
        "name": candidate.name,
        "resume_text": candidate.resume_text,
        "current_ctc": candidate.current_ctc,
        "expected_ctc": candidate.expected_ctc,
        "additional_info": additional_info
    }
    
    # Prepare job info as dictionary
    job_info = {
        "id": job.id,
        "title": job.title,
        "jd_text": job.jd_text,
        "min_budget": job.min_budget,
        "max_budget": job.max_budget
    }
    
    # Use Ollama client to get match score
    score = ollama_client.compare_candidate_with_jd(candidate_info, job_info)
    
    return score

def compare_candidates(candidates: List[Candidate], job: Job) -> Dict[int, float]:
    """
    Compare candidates with each other in context of a job and return comparative scores.
    """
    # If no candidates or only one candidate, return early
    if not candidates or len(candidates) <= 1:
        return {c.id: 0.5 for c in candidates}
    
    # Prepare candidate information
    candidates_info = []
    for c in candidates:
        additional_info = {}
        if c.additional_info:
            try:
                additional_info = json.loads(c.additional_info)
            except:
                additional_info = {"data": c.additional_info}
        
        candidates_info.append({
            "id": c.id,
            "name": c.name,
            "resume_text": c.resume_text,
            "current_ctc": c.current_ctc,
            "expected_ctc": c.expected_ctc,
            "additional_info": additional_info
        })
    
    # Prepare job info as dictionary
    job_info = {
        "id": job.id,
        "title": job.title,
        "jd_text": job.jd_text,
        "min_budget": job.min_budget,
        "max_budget": job.max_budget
    }
    
    # Use Ollama client to get comparative scores
    scores = ollama_client.compare_candidates(candidates_info, job_info)
    
    return scores

def match_candidates_with_job(db: Session, job_id: int) -> Tuple[List[CandidateWithScores], List[CandidateWithScores]]:
    """
    Match candidates with a job and return two sorted lists:
    1. Candidates sorted by match with JD
    2. Candidates sorted by comparative ranking
    """
    # Get job
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        return [], []
    
    # Get all candidates
    candidates = db.query(Candidate).all()
    if not candidates:
        return [], []
    
    # For each candidate, compare with JD
    jd_scores = {}
    for candidate in candidates:
        score = compare_candidate_with_jd(candidate, job)
        jd_scores[candidate.id] = score
    
    # Compare candidates with each other
    comparative_scores = compare_candidates(candidates, job)
    
    # Save scores to database
    for candidate in candidates:
        # Check if match record already exists
        match_record = db.query(CandidateJobMatch).filter_by(
            candidate_email=candidate.email, 
            job_id=job.id
        ).first()
        
        if match_record:
            # Update existing record
            match_record.jd_match_score = jd_scores.get(candidate.id, 0)
            match_record.comparative_score = comparative_scores.get(candidate.id, 0)
            db.add(match_record)
        else:
            # Insert new record
            match_record = CandidateJobMatch(
                candidate_email=candidate.email,
                job_id=job.id,
                jd_match_score=jd_scores.get(candidate.id, 0),
                comparative_score=comparative_scores.get(candidate.id, 0)
            )
            db.add(match_record)
    
    db.commit()
    
    # Create CandidateWithScores objects
    jd_matches = []
    comparative_matches = []
    
    for candidate in candidates:
        candidate_with_jd_score = CandidateWithScores(
            **{c.name: getattr(candidate, c.name) for c in candidate.__table__.columns},
            jd_match_score=jd_scores.get(candidate.id, 0)
        )
        
        candidate_with_comparative_score = CandidateWithScores(
            **{c.name: getattr(candidate, c.name) for c in candidate.__table__.columns},
            comparative_score=comparative_scores.get(candidate.id, 0)
        )
        
        jd_matches.append(candidate_with_jd_score)
        comparative_matches.append(candidate_with_comparative_score)
    
    # Sort both lists (descending order)
    jd_matches.sort(key=lambda x: x.jd_match_score, reverse=True)
    comparative_matches.sort(key=lambda x: x.comparative_score, reverse=True)
    
    return jd_matches, comparative_matches 