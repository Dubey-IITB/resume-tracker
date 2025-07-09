import requests
import os
import sys
import json
import glob

def test_candidate_creation():
    """Test candidate creation with Ollama email extraction."""
    print("⚙️ Testing candidate creation with Ollama email extraction")
    
    # Find resume files in downloads folder
    downloads_dir = os.path.expanduser("~/Downloads")
    resume_files = glob.glob(os.path.join(downloads_dir, "*.pdf"))
    
    if not resume_files:
        print(f"❌ No PDF files found in {downloads_dir}")
        return
    
    # Use at most 2 resumes for the test
    resume_files = resume_files[:2]
    print(f"📄 Found {len(resume_files)} resume files for testing:")
    for i, file_path in enumerate(resume_files):
        print(f"   {i+1}. {os.path.basename(file_path)}")
    
    # Sample salary expectations
    current_ctcs = [float(80000)] * len(resume_files)
    expected_ctcs = [float(95000)] * len(resume_files)
    
    # Prepare files for upload
    files = []
    for file_path in resume_files:
        file_name = os.path.basename(file_path)
        with open(file_path, "rb") as f:
            file_content = f.read()
            files.append(("files", (file_name, file_content, "application/pdf")))
    
    # Convert CTC values to the correct format
    data = {
        "current_ctcs": current_ctcs,
        "expected_ctcs": expected_ctcs
    }
    
    print("⏳ Sending request to create-candidates-from-pdfs endpoint...")
    
    try:
        response = requests.post(
            "http://localhost:8000/api/create-candidates-from-pdfs", 
            files=files,
            data={
                "current_ctcs": current_ctcs,
                "expected_ctcs": expected_ctcs,
            }
        )
        
        print(f"🔄 Response status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success: {result.get('message', 'Candidates created successfully')}")
            
            if "candidates" in result:
                print(f"✅ Created/updated {len(result['candidates'])} candidates:")
                for candidate in result["candidates"]:
                    print(f"   👤 {candidate['name']} ({candidate['email']})")
                    
                    # Check if the email was properly extracted (not a synthetic email)
                    email = candidate['email']
                    if "@example.com" in email:
                        print(f"   ⚠️ Warning: Synthetic email detected ({email})")
                    else:
                        print(f"   ✓ Valid email detected: {email}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Error details: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    print("\n✅ TEST COMPLETED")

if __name__ == "__main__":
    try:
        # Check if server is running
        try:
            response = requests.get("http://localhost:8000/api/test")
            if response.status_code != 200:
                print("❌ Server is not responding. Please start the server with 'python main.py'")
                sys.exit(1)
        except requests.exceptions.ConnectionError:
            print("❌ Server is not running. Please start the server with 'python main.py'")
            sys.exit(1)
            
        test_candidate_creation()
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        sys.exit(1) 