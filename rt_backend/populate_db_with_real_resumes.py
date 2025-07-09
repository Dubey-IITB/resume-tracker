import json
import os
import pdfplumber
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.session import Base
from app.db.models import Candidate
from app.services.ollama_service import OllamaClient

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file using pdfplumber."""
    try:
        print(f"Extracting text from {file_path}")
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
            return text
    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
        return None

def populate_db_with_real_resumes():
    # Initialize database connection
    engine = create_engine('sqlite:///./app.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Initialize Ollama client for email extraction
    ollama_client = OllamaClient()
    
    # Get resumes from Downloads folder
    downloads_dir = os.path.expanduser("~/Downloads")
    resume_files = ["resume1.pdf", "resume2.pdf"]
    
    for resume_file in resume_files:
        file_path = os.path.join(downloads_dir, resume_file)
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue
        
        # Extract text from PDF
        resume_text = extract_text_from_pdf(file_path)
        if not resume_text:
            print(f"Could not extract text from {resume_file}")
            continue
        
        # Extract email using Ollama
        email = ollama_client.extract_email_from_resume(resume_text)
        print(f"Extracted email from {resume_file}: {email}")
        
        # Extract candidate details
        details = ollama_client.extract_candidate_details(resume_text)
        
        # Get name from details or use filename
        name = details.get("fullName") if details and "fullName" in details else resume_file.replace(".pdf", "")
        
        # Check if candidate already exists
        existing_candidate = session.query(Candidate).filter_by(email=email).first()
        if existing_candidate:
            print(f"Candidate with email {email} already exists, updating")
            existing_candidate.name = name
            existing_candidate.resume_text = resume_text
            existing_candidate.current_ctc = 80000 if resume_file == "resume1.pdf" else 70000  # Sample values
            existing_candidate.expected_ctc = 95000 if resume_file == "resume1.pdf" else 85000  # Sample values
        else:
            print(f"Creating new candidate: {name}, {email}")
            candidate = Candidate(
                email=email,
                name=name,
                resume_text=resume_text,
                current_ctc=80000 if resume_file == "resume1.pdf" else 70000,  # Sample values
                expected_ctc=95000 if resume_file == "resume1.pdf" else 85000  # Sample values
            )
            session.add(candidate)
    
    # Commit changes
    session.commit()
    
    # Print all candidates
    candidates = session.query(Candidate).all()
    print("\nCandidates in database:")
    for c in candidates:
        print(f"- {c.name} ({c.email})")
    
    session.close()
    print("\nDatabase populated successfully!")

if __name__ == "__main__":
    populate_db_with_real_resumes() 