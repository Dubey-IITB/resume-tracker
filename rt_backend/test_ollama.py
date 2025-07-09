import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.ollama_service import OllamaClient
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_email_extraction():
    """Test the email extraction functionality."""
    # Sample resume text with an email
    sample_resume = """
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
    
    # Initialize the Ollama client
    ollama_client = OllamaClient()
    
    # Test email extraction
    logger.info("Testing email extraction...")
    email = ollama_client.extract_email_from_resume(sample_resume)
    logger.info(f"Extracted email: {email}")
    
    # Test detailed extraction
    logger.info("Testing detailed candidate extraction...")
    details = ollama_client.extract_candidate_details(sample_resume)
    logger.info(f"Extracted details: {details}")
    
    return email, details

if __name__ == "__main__":
    try:
        email, details = test_email_extraction()
        print("\nTest Results:")
        print(f"Email: {email}")
        print(f"Candidate Details: {details}")
        print("\nTest completed successfully!")
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)
        print(f"\nTest failed: {e}")
        sys.exit(1) 