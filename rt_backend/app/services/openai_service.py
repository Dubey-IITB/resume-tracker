import openai
from app.core.config import settings
import json
import logging
from typing import Optional, Dict
import re
import extract_emails

logger = logging.getLogger(__name__)

def get_openai_client():
    """Initializes and returns an OpenAI client."""
    return openai.OpenAI(api_key=settings.OPENAI_API_KEY)

def extract_candidate_details_from_text(client: openai.OpenAI, resume_text: str) -> Optional[Dict[str, str]]:
    """Extracts candidate details (like name and email) from resume text using OpenAI."""
    if not resume_text or not resume_text.strip():
        return None

    simple_prompt = (
        "Extract the candidate\'s full name and email address from the following text. "
        "Return JSON with keys \"name\" and \"email\". "
        "If email or name is not found, return null for that field. Text: " + resume_text[:2000]
    )

    try:
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are an assistant that extracts structured information.",},
                {"role": "user", "content": simple_prompt}
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        if content:
            data = json.loads(content)
            return {"name": data.get("name"), "email": data.get("email")}
        return None
    except Exception as e:
        logger.error(f"Error in OpenAI call for details: {e}")
        return None

def extract_email_from_text(text: str) -> Optional[str]:
    """Extracts the first valid email from text using the extract_emails library."""
    if not text or not text.strip():
        logger.info("Email extraction skipped: input text is empty or whitespace.")
        return None
    
    try:
        # extract_emails returns an iterator of EmailMatch objects
        # We'll take the first one if it exists.
        email_iterator = extract_emails.extract_emails(text, first_only=True, resolve_gxh_obfuscation=True)
        first_match = next(email_iterator, None)
        
        if first_match:
            extracted_email = first_match.email
            logger.info(f"Successfully extracted email using extract_emails library: {extracted_email}")
            return extracted_email
        else:
            logger.info(f"No email found by extract_emails library in the provided text.")
            return None
    except Exception as e:
        logger.error(f"Error using extract_emails library: {e}", exc_info=True)
        return None

def generate_candidate_job_match_summary(client, job_description, candidate_resume):
    logger.warning("generate_candidate_job_match_summary is STUBBED.")
    return None

def analyze_resume_for_skills_and_experience(client, resume_text):
    logger.warning("analyze_resume_for_skills_and_experience is STUBBED.")
    return None 