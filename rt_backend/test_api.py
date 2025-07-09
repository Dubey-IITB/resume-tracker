import requests
import os

def test_process_and_match():
    # Test data
    job_description = """
    Senior Software Engineer
    Requirements:
    - 5+ years of experience in Python development
    - Strong knowledge of FastAPI and SQLAlchemy
    - Experience with cloud platforms (AWS/GCP)
    - Bachelor's degree in Computer Science or related field
    """
    
    budget = 150000  # $150k budget
    
    # Get sample PDFs from Downloads folder
    downloads_dir = os.path.expanduser("~/Downloads")
    pdf_files = [f for f in os.listdir(downloads_dir) if f.endswith('.pdf')][:2]
    
    if len(pdf_files) < 2:
        print("Please ensure you have at least 2 PDF files in your Downloads folder")
        return
    
    # Prepare the files and form data
    files = [
        ('files', (pdf_files[0], open(os.path.join(downloads_dir, pdf_files[0]), 'rb'), 'application/pdf')),
        ('files', (pdf_files[1], open(os.path.join(downloads_dir, pdf_files[1]), 'rb'), 'application/pdf'))
    ]
    
    data = {
        'job_description': job_description,
        'budget': str(budget),
        'current_ctcs': ['100000', '120000'],  # Sample current CTCs
        'expected_ctcs': ['130000', '140000']  # Sample expected CTCs
    }
    
    # Make the request
    try:
        response = requests.post(
            'http://localhost:8000/api/process-and-match',
            files=files,
            data=data
        )
        
        print(f"Status Code: {response.status_code}")
        print("Response:")
        print(response.json())
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        # Close the files
        for file in files:
            file[1][1].close()

if __name__ == "__main__":
    test_process_and_match() 