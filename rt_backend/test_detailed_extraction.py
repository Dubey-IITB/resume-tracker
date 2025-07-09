import requests
import sys
import os
import json
import argparse

def test_detailed_extraction(file_path=None):
    """
    Test detailed resume extraction for a single file.
    
    Args:
        file_path: Path to the resume file. If None, will prompt user to select from Downloads.
    """
    if not file_path:
        # Path to Downloads folder
        downloads_dir = os.path.expanduser("~/Downloads")
        
        # List PDF files
        pdf_files = [f for f in os.listdir(downloads_dir) if f.lower().endswith('.pdf')]
        
        if not pdf_files:
            print(f"No PDF files found in {downloads_dir}")
            return
        
        # Present choices to user
        print("Available PDF files in Downloads:")
        for i, filename in enumerate(pdf_files):
            print(f"{i+1}. {filename}")
        
        choice = input("\nEnter the number of the file to process (or 'q' to quit): ")
        if choice.lower() == 'q':
            return
        
        try:
            index = int(choice) - 1
            if 0 <= index < len(pdf_files):
                file_path = os.path.join(downloads_dir, pdf_files[index])
            else:
                print("Invalid selection")
                return
        except ValueError:
            print("Invalid input")
            return
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    print(f"\nProcessing: {os.path.basename(file_path)}")
    
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
            
            files = {"resume": (os.path.basename(file_path), f, content_type)}
            
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
            
            # Print email
            print("\n" + "="*50)
            print("EMAIL EXTRACTION RESULT:")
            print("="*50)
            print(f"Email: {result.get('email') or 'No email found'}")
            
            # Print detailed candidate information
            if 'details' in result and result['details']:
                print("\n" + "="*50)
                print("DETAILED CANDIDATE INFORMATION:")
                print("="*50)
                
                details = result['details']
                print(json.dumps(details, indent=2))
                
                # Create a readable summary
                print("\n" + "="*50)
                print("CANDIDATE SUMMARY:")
                print("="*50)
                
                # Name
                name = None
                if 'fullName' in details:
                    name = details['fullName']
                elif 'name' in details:
                    name = details['name']
                print(f"Name: {name or 'Not found'}")
                
                # Email
                email = None
                if 'emailAddress' in details:
                    email = details['emailAddress']
                elif 'email' in details:
                    email = details['email']
                print(f"Email: {email or result.get('email') or 'Not found'}")
                
                # Phone
                phone = None
                if 'phoneNumber' in details:
                    phone = details['phoneNumber']
                elif 'phone' in details:
                    phone = details['phone']
                print(f"Phone: {phone or 'Not found'}")
                
                # Skills
                skills = []
                if 'skills' in details and details['skills']:
                    if isinstance(details['skills'], list):
                        skills = details['skills']
                    elif isinstance(details['skills'], str):
                        skills = [details['skills']]
                print(f"Skills: {', '.join(skills) if skills else 'Not found'}")
                
                # Experience
                experience = None
                if 'yearsOfExperience' in details:
                    experience = details['yearsOfExperience']
                print(f"Years of Experience: {experience or 'Not found'}")
                
                # Education
                education = None
                if 'education' in details:
                    if isinstance(details['education'], dict):
                        if 'highestDegree' in details['education']:
                            education = details['education']['highestDegree']
                    else:
                        education = details['education']
                print(f"Education: {education or 'Not found'}")
            
            # Print extracted text
            if 'text_sample' in result:
                print("\n" + "="*50)
                print("EXTRACTED TEXT SAMPLE:")
                print("="*50)
                print(result['text_sample'])
        else:
            print(f"Error response: {response.text}")
    
    except Exception as e:
        print(f"Error processing file: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test detailed resume extraction.')
    parser.add_argument('--file', '-f', help='Path to the resume file to process')
    args = parser.parse_args()
    
    try:
        test_detailed_extraction(args.file)
    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1) 