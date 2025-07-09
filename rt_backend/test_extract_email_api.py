import requests
import sys
import os
import json

def test_extract_email_api():
    """Test the extract-email API endpoint."""
    # Create a simple text file with resume content
    resume_content = """
    John Doe
    Software Developer
    john.doe@example.com
    (123) 456-7890
    
    Experience:
    - Senior Developer at XYZ Corp (2018-present)
    - Junior Developer at ABC Inc (2015-2018)
    
    Skills:
    - Python, JavaScript, SQL
    - AWS, Docker, Kubernetes
    """
    
    # Create a temporary text file
    test_file_path = "test_resume.txt"
    with open(test_file_path, "w") as f:
        f.write(resume_content)
    
    try:
        # Prepare the file for upload
        with open(test_file_path, "rb") as f:
            files = {"resume": ("test_resume.txt", f, "text/plain")}
            
            # Make the request
            response = requests.post(
                "http://localhost:8000/api/extract-email",
                files=files
            )
        
        # Print the response
        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            print("Response JSON:")
            print(json.dumps(response.json(), indent=2))
            
            # Check if email was extracted correctly
            if response.json().get("email") == "john.doe@example.com":
                print("\nSUCCESS: Email extracted correctly!")
            else:
                print(f"\nERROR: Email was not extracted correctly. Got: {response.json().get('email')}")
        else:
            print(f"Error response: {response.text}")
    
    finally:
        # Clean up the test file
        if os.path.exists(test_file_path):
            os.remove(test_file_path)

if __name__ == "__main__":
    try:
        test_extract_email_api()
    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1) 