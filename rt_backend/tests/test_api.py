import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import requests
import PyPDF2

from app.db.base import Base
from app.db.session import get_db
from main import app

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

BASE_URL = "http://localhost:8000"

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def test_root():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    print("Root Response:", response.json())

def test_api_test():
    response = requests.get(BASE_URL + "/api/test")
    assert response.status_code == 200
    print("API Test Response:", response.json())

def test_candidates():
    response = requests.get(BASE_URL + "/api/candidates")
    assert response.status_code == 200
    print("Candidates Response:", response.json())

def test_resume_ranking():
    pdf_path_1 = "/Users/kirtivatsalmishra/Downloads/resume.pdf"  # Replace with the path to your first PDF file
    pdf_path_2 = "/Users/kirtivatsalmishra/Downloads/Kirti_Mishra_Resume.pdf"
    resume_text_1 = extract_text_from_pdf(pdf_path_1)
    resume_text_2 = extract_text_from_pdf(pdf_path_2)
    resume_data = {
        "resume1": resume_text_1,
        "resume2": resume_text_2,
        "job_description": "Looking for a Python developer with FastAPI experience."
    }
    response = requests.post(BASE_URL + "/api/rank", json=resume_data)
    assert response.status_code == 200
    print("Resume Ranking Response:", response.json())

def test_auth_test_endpoint():
    response = client.get("/api/test")
    assert response.status_code == 200
    assert response.json() == {"message": "Authentication route is working"}

def test_candidates_test_endpoint():
    response = client.get("/api/test")
    assert response.status_code == 200
    assert response.json() == {"message": "Candidates route is working"}

def test_jobs_test_endpoint():
    response = client.get("/api/test")
    assert response.status_code == 200
    assert response.json() == {"message": "Jobs route is working"}

def test_create_candidate():
    candidate_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "current_ctc": 100000,
        "expected_ctc": 120000,
        "resume_path": "/path/to/resume.pdf"
    }
    response = client.post("/api/candidates", json=candidate_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == candidate_data["name"]
    assert data["email"] == candidate_data["email"]
    assert data["current_ctc"] == candidate_data["current_ctc"]
    assert data["expected_ctc"] == candidate_data["expected_ctc"]

def test_create_job():
    job_data = {
        "title": "Senior Software Engineer",
        "description": "Looking for an experienced software engineer",
        "budget_min": 120000,
        "budget_max": 150000,
        "recruiter_id": 1
    }
    response = client.post("/api/jobs", json=job_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == job_data["title"]
    assert data["description"] == job_data["description"]
    assert data["budget_min"] == job_data["budget_min"]
    assert data["budget_max"] == job_data["budget_max"]

def test_get_candidates():
    response = client.get("/api/candidates")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_jobs():
    response = client.get("/api/jobs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_candidate_by_id():
    # First create a candidate
    candidate_data = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "current_ctc": 90000,
        "expected_ctc": 110000,
        "resume_path": "/path/to/resume.pdf"
    }
    create_response = client.post("/api/candidates", json=candidate_data)
    candidate_id = create_response.json()["id"]
    
    # Then get the candidate by ID
    response = client.get(f"/api/candidates/{candidate_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == candidate_data["name"]
    assert data["email"] == candidate_data["email"]

def test_get_job_by_id():
    # First create a job
    job_data = {
        "title": "Junior Developer",
        "description": "Entry level position",
        "budget_min": 60000,
        "budget_max": 80000,
        "recruiter_id": 1
    }
    create_response = client.post("/api/jobs", json=job_data)
    job_id = create_response.json()["id"]
    
    # Then get the job by ID
    response = client.get(f"/api/jobs/{job_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == job_data["title"]
    assert data["description"] == job_data["description"]

if __name__ == "__main__":
    test_root()
    test_api_test()
    test_candidates()
    test_resume_ranking()
    print("All tests passed!") 