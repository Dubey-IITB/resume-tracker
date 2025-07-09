import json
import os
from typing import Any, Dict, List, Optional, Union

from fastapi import UploadFile
from sqlalchemy.orm import Session
import PyPDF2

from app.db.models import Job
from app.schemas.job import JobCreate, JobUpdate

def get_by_id(db: Session, *, id: int) -> Optional[Job]:
    return db.query(Job).filter(Job.id == id).first()

def get_multi(
    db: Session, *, skip: int = 0, limit: int = 100, recruiter_id: Optional[int] = None
) -> List[Job]:
    query = db.query(Job)
    if recruiter_id:
        query = query.filter(Job.recruiter_id == recruiter_id)
    return query.offset(skip).limit(limit).all()

def create(
    db: Session, *, obj_in: JobCreate, recruiter_id: int, jd_file: UploadFile = None
) -> Job:
    # Extract text from the JD if provided
    jd_text = ""
    
    if jd_file:
        # Create directory for JDs if it doesn't exist
        os.makedirs("uploads/jds", exist_ok=True)
        
        # Save the JD file
        jd_path = f"uploads/jds/{jd_file.filename}"
        with open(jd_path, "wb") as f:
            f.write(jd_file.file.read())
        
        # Extract text from PDF
        if jd_path.lower().endswith('.pdf'):
            with open(jd_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    jd_text += page.extract_text()
    
    # Create job object
    data = obj_in.dict()
    db_obj = Job(
        **data,
        recruiter_id=recruiter_id,
        jd_text=jd_text,
    )
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(
    db: Session, *, db_obj: Job, obj_in: Union[JobUpdate, Dict[str, Any]]
) -> Job:
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def remove(db: Session, *, id: int) -> Job:
    obj = db.query(Job).get(id)
    db.delete(obj)
    db.commit()
    return obj 