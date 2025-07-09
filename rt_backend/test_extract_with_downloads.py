import requests
import sys
import os
import json
import glob

def test_extract_email_from_downloads():
    """Test the extract-email API endpoint with files from the Downloads folder."""
    
    # Path to Downloads folder
    downloads_dir = os.path.expanduser("~/Downloads")
    
    # Look for PDFs and common resume file formats
    resume_files = []
    for ext in ['*.pdf', '*.docx', '*.doc', '*.txt']:
        resume_files.extend(glob.glob(os.path.join(downloads_dir, ext)))
    
    if not resume_files:
        print(f"No resume files found in {downloads_dir}")
        return

    print(f"Found {len(resume_files)} potential resume files:")
    for i, file_path in enumerate(resume_files):
        print(f"{i+1}. {os.path.basename(file_path)}")
    
    # Process each file
    for file_path in resume_files:
        file_name = os.path.basename(file_path)
        print(f"\nProcessing: {file_name}")
        
        try:
            # Prepare the file for upload
            with open(file_path, "rb") as f:
                # Determine content type based on extension
                content_type = "application/pdf"
                if file_path.lower().endswith('.docx'):
                    content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                elif file_path.lower().endswith('.doc'):
                    content_type = "application/msword"
                elif file_path.lower().endswith('.txt'):
                    content_type = "text/plain"
                
                files = {"resume": (file_name, f, content_type)}
                
                # Make the request
                print("Sending to API...")
                response = requests.post(
                    "http://localhost:8000/api/extract-email",
                    files=files
                )
            
            # Print the response
            print(f"Status code: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print("\nEmail extraction result:")
                print(f"Email: {result.get('email') or 'No email found'}")
                
                if 'details' in result and result['details']:
                    print("\nExtracted details:")
                    details = result['details']
                    
                    # Print name if available
                    if 'fullName' in details:
                        print(f"Name: {details['fullName']}")
                    elif 'name' in details:
                        print(f"Name: {details['name']}")
                    
                    # Print phone if available
                    if 'phoneNumber' in details:
                        print(f"Phone: {details['phoneNumber']}")
                    elif 'phone' in details:
                        print(f"Phone: {details['phone']}")
                    
                    # Print skills if available
                    if 'skills' in details and details['skills']:
                        print(f"Skills: {', '.join(details['skills'])}")
                    
                    # Print experience if available
                    if 'yearsOfExperience' in details:
                        print(f"Experience: {details['yearsOfExperience']} years")
                    
                # Print sample of extracted text
                if 'text_sample' in result:
                    print("\nSample of extracted text:")
                    print(result['text_sample'][:200] + "..." if len(result['text_sample']) > 200 else result['text_sample'])
            else:
                print(f"Error response: {response.text}")
        
        except Exception as e:
            print(f"Error processing {file_name}: {str(e)}")

if __name__ == "__main__":
    try:
        test_extract_email_from_downloads()
    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1) 