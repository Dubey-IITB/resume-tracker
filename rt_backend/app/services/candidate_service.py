import json
import os
from typing import Any, Dict, List, Optional, Union
import logging

from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
import PyPDF2

from app.db.models import Candidate
from app.schemas.candidate import CandidateCreate, CandidateUpdate
from app.services.ollama_service import OllamaClient
from app.services.openai_service import extract_email_from_text

logger = logging.getLogger(__name__)

def get_by_email(db: Session, *, email: str) -> Optional[Candidate]:
    return db.query(Candidate).filter(Candidate.email == email).first()

def get_multi(
    db: Session, *, skip: int = 0, limit: int = 100
) -> List[Candidate]:
    return db.query(Candidate).offset(skip).limit(limit).all()

def create(
    db: Session, *, obj_in: CandidateCreate, resume_file: UploadFile = None
) -> Candidate:
    # Parse the additional_info as JSON if it's a string
    additional_info = obj_in.additional_info
    if isinstance(additional_info, str):
        additional_info = json.loads(additional_info)
    
    # Extract text from the resume if provided
    resume_path = ""
    resume_text = ""
    
    if resume_file:
        # Create directory for resumes if it doesn't exist
        os.makedirs("uploads/resumes", exist_ok=True)
        
        # Save the resume file
        resume_path = f"uploads/resumes/{resume_file.filename}"
        with open(resume_path, "wb") as f:
            f.write(resume_file.file.read())
        
        # Extract text from PDF
        if resume_path.lower().endswith('.pdf'):
            with open(resume_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    resume_text += page.extract_text()
                    
        # Always try to extract email using Ollama, even if email is provided
        # This ensures we have a valid email as the primary key
        try:
            # Initialize Ollama client
            ollama_client = OllamaClient()
            
            # Extract email from resume text
            extracted_email = ollama_client.extract_email_from_resume(resume_text)
            
            # If email is found by Ollama, use it
            if extracted_email:
                logger.info(f"Email extracted by Ollama: {extracted_email}")
                obj_in.email = extracted_email
            # Only if Ollama fails, try the fallback method
            elif not obj_in.email:
                fallback_email = extract_email_from_text(resume_text)
                if fallback_email:
                    logger.info(f"Email extracted by fallback method: {fallback_email}")
                    obj_in.email = fallback_email
                else:
                    # If no email could be extracted, raise an exception
                    raise HTTPException(
                        status_code=400,
                        detail="Could not extract email from resume and no email was provided. Email is required as the primary key."
                    )
        except Exception as e:
            logger.error(f"Error extracting email with Ollama: {e}", exc_info=True)
            # If exception occurred and no email is provided, raise an exception
            if not obj_in.email:
                raise HTTPException(
                    status_code=400,
                    detail=f"Error extracting email and no email was provided: {str(e)}"
                )
    elif not obj_in.email:
        # If no resume file and no email provided, raise an exception
        raise HTTPException(
            status_code=400,
            detail="Either a resume file or an email address must be provided."
        )
    
    # Check if candidate with this email already exists
    existing_candidate = get_by_email(db, email=obj_in.email)
    if existing_candidate:
        logger.info(f"Candidate with email {obj_in.email} already exists, updating instead of creating new")
        # Update existing candidate
        for field in ["name", "current_ctc", "expected_ctc"]:
            if hasattr(obj_in, field) and getattr(obj_in, field) is not None:
                setattr(existing_candidate, field, getattr(obj_in, field))
        
        # Update resume info if provided
        if resume_text:
            existing_candidate.resume_text = resume_text
            existing_candidate.resume_path = resume_path
        
        # Update additional info if provided
        if additional_info:
            existing_candidate.additional_info = json.dumps(additional_info)
        
        db.add(existing_candidate)
        db.commit()
        db.refresh(existing_candidate)
        return existing_candidate
    
    # Create new candidate object
    db_obj = Candidate(
        name=obj_in.name,
        email=obj_in.email,  # Using the extracted or provided email as primary key
        resume_path=resume_path,
        resume_text=resume_text,
        current_ctc=obj_in.current_ctc,
        expected_ctc=obj_in.expected_ctc,
        additional_info=json.dumps(additional_info) if additional_info else None,
    )
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(
    db: Session, *, db_obj: Candidate, obj_in: Union[CandidateUpdate, Dict[str, Any]]
) -> Candidate:
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    
    # Handle additional_info specially if it exists
    if "additional_info" in update_data and update_data["additional_info"]:
        if isinstance(update_data["additional_info"], dict):
            update_data["additional_info"] = json.dumps(update_data["additional_info"])
        elif isinstance(update_data["additional_info"], str):
            # Ensure it's valid JSON
            try:
                json.loads(update_data["additional_info"])
            except:
                # If not valid JSON, store as a JSON string
                update_data["additional_info"] = json.dumps(update_data["additional_info"])
    
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def remove(db: Session, *, email: str) -> Candidate:
    obj = db.query(Candidate).get(email)
    db.delete(obj)
    db.commit()
    return obj 