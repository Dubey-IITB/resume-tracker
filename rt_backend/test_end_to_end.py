import requests
import os
import sys
import json
import glob
import time

def test_end_to_end():
    """
    Test the entire application flow end-to-end using resumes from the downloads folder.
    This test simulates a frontend request to match candidates against a job description.
    """
    # Ensure server is running
    try:
        # Check if server is running
        response = requests.get("http://localhost:8000/api/test")
        if response.status_code != 200:
            print("❌ Server is not responding. Please start the server with 'python main.py'")
            return
        print("✅ Server is running")
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Please start the server with 'python main.py'")
        return

    # Step 1: Find resume files in downloads folder
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
    
    # Step 2: Create a mock job description
    job_description = """
    Senior Java Developer
    
    Requirements:
    - 5+ years of experience in Java development
    - Experience with Spring Framework
    - Strong understanding of REST APIs
    - Experience with cloud platforms (AWS, GCP, or Azure)
    - Good understanding of database systems
    - Experience with CI/CD pipelines
    
    Nice to have:
    - Experience with microservices architecture
    - Knowledge of JavaScript and modern frontend frameworks
    - Experience with containerization technologies (Docker, Kubernetes)
    
    Responsibilities:
    - Design and implement new features
    - Optimize application for performance and scalability
    - Collaborate with cross-functional teams
    - Participate in code reviews and architectural discussions
    """
    
    # Step 3: Set mock salary expectations
    # Using random values for demonstration
    current_ctcs = [80000] * len(resume_files)
    expected_ctcs = [95000] * len(resume_files)
    
    # Step 4: Test individual email extraction (simulate frontend preview)
    print("\n🔍 TESTING EMAIL EXTRACTION (Preview):")
    emails = []
    for file_path in resume_files:
        file_name = os.path.basename(file_path)
        print(f"\nProcessing: {file_name}")
        
        try:
            with open(file_path, "rb") as f:
                files = {"resume": (file_name, f, "application/pdf")}
                response = requests.post(
                    "http://localhost:8000/api/extract-email",
                    files=files
                )
            
            if response.status_code == 200:
                result = response.json()
                email = result.get("email")
                if email:
                    emails.append(email)
                print(f"✅ Email extracted: {email or 'Not found'}")
                
                if "details" in result and result["details"]:
                    details = result["details"]
                    if "fullName" in details and details["fullName"]:
                        print(f"👤 Name: {details['fullName']}")
                    if "skills" in details and details["skills"]:
                        skills = details["skills"]
                        if isinstance(skills, list):
                            print(f"🛠️ Skills: {', '.join(skills[:5])}{'...' if len(skills) > 5 else ''}")
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Error processing {file_name}: {e}")
    
    # Step 5: Test bulk candidate creation
    print("\n📋 TESTING CANDIDATE CREATION:")
    try:
        # Prepare files for upload
        files = []
        for i, file_path in enumerate(resume_files):
            with open(file_path, "rb") as f:
                files.append(("files", (os.path.basename(file_path), f.read(), "application/pdf")))
        
        # Convert CTC values to strings (as expected by the API)
        current_ctcs_str = [str(ctc) for ctc in current_ctcs]
        expected_ctcs_str = [str(ctc) for ctc in expected_ctcs]
        
        response = requests.post(
            "http://localhost:8000/api/create-candidates-from-pdfs",
            files=files,
            data={
                "current_ctcs": current_ctcs_str,
                "expected_ctcs": expected_ctcs_str,
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {result.get('message', 'Candidates created successfully')}")
            
            if "candidates" in result:
                print(f"✅ Created {len(result['candidates'])} candidates:")
                for candidate in result["candidates"]:
                    print(f"   👤 {candidate['name']} ({candidate['email']})")
                    # Make sure email is in our list for later use
                    if candidate['email'] not in emails:
                        emails.append(candidate['email'])
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error creating candidates: {e}")
    
    # Step 6: Test process-and-match endpoint (most comprehensive test)
    print("\n🔍 TESTING PROCESS AND MATCH:")
    try:
        # Prepare files for upload
        files = []
        for i, file_path in enumerate(resume_files):
            with open(file_path, "rb") as f:
                files.append(("files", (os.path.basename(file_path), f.read(), "application/pdf")))
        
        # Set up the form data
        data = {
            "job_description": job_description,
            "budget": "100000",  # Budget in string format
            "current_ctcs": current_ctcs_str,
            "expected_ctcs": expected_ctcs_str,
        }
        
        print("⏳ Sending request to process-and-match endpoint (this may take a while)...")
        response = requests.post(
            "http://localhost:8000/api/process-and-match",
            files=files,
            data=data
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Successfully processed and matched candidates")
            
            if "candidates" in result:
                print(f"✅ Processed {len(result['candidates'])} candidates:")
                for candidate in result["candidates"]:
                    print(f"   👤 {candidate['name']} ({candidate['email']})")
            
            if "analysis" in result:
                analysis = result["analysis"]
                if "comparative_analysis" in analysis:
                    comp_analysis = analysis["comparative_analysis"]
                    if "best_match" in comp_analysis:
                        # Best match could be an email or index
                        best_match = comp_analysis["best_match"]
                        print(f"✅ Best match: {best_match}")
                        
                        # If it's an index, convert to the appropriate candidate
                        try:
                            if isinstance(best_match, int) and "candidates" in result:
                                if 0 <= best_match - 1 < len(result["candidates"]):
                                    best_match_candidate = result["candidates"][best_match - 1]
                                    print(f"   👤 Candidate: {best_match_candidate['name']} ({best_match_candidate['email']})")
                        except Exception as e:
                            print(f"   ⚠️ Could not identify best match candidate: {e}")
                    
                    if "reasoning" in comp_analysis:
                        print(f"📝 Reasoning: {comp_analysis['reasoning'][:150]}...")
                
                # Print candidate details
                if "candidates" in analysis:
                    for i, candidate_analysis in enumerate(analysis["candidates"]):
                        print(f"\n📊 Candidate {i+1} Analysis:")
                        for key, value in candidate_analysis.items():
                            if key not in ["strengths", "weaknesses", "salary_analysis", "recommendation"]:
                                print(f"   {key}: {value}")
            
            if "ranking_analysis" in result:
                ranking = result["ranking_analysis"]
                if "winner" in ranking:
                    print(f"🏆 Winner according to ranking: {ranking['winner']}")
                
                if "overall_scores" in ranking:
                    scores = ranking["overall_scores"]
                    print("📊 Overall scores:")
                    for candidate, score in scores.items():
                        print(f"   {candidate}: {score}")
            
            if "synthetic_email_warnings" in result:
                print(f"⚠️ Warning: {len(result['synthetic_email_warnings'])} synthetic emails were generated")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error in process-and-match: {e}")
    
    print("\n✅ END-TO-END TEST COMPLETED")
    
    # If emails were successfully extracted, report them
    if emails:
        print("\n📧 Extracted Emails (Primary Keys):")
        for i, email in enumerate(emails):
            print(f"   {i+1}. {email}")

if __name__ == "__main__":
    try:
        test_end_to_end()
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        sys.exit(1) 