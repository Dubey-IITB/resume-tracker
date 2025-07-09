import requests
import json
import logging
from typing import Optional, Dict, List, Any
from app.core.config import settings

logger = logging.getLogger(__name__)

class OllamaClient:
    """Client for interacting with a local Ollama instance."""
    
    def __init__(self, base_url: str = None, model: str = None):
        self.base_url = base_url or settings.OLLAMA_BASE_URL
        self.model = model or settings.OLLAMA_MODEL
        self.completions_endpoint = f"{self.base_url}/v1/chat/completions"
        
        logger.info(f"Initialized Ollama client with base_url: {self.base_url}, model: {self.model}")
    
    def extract_email_from_resume(self, resume_text: str) -> Optional[str]:
        """
        Extract email address from resume text using Ollama LLM.
        
        Args:
            resume_text: The text content of the resume
            
        Returns:
            Extracted email address or None if not found
        """
        if not resume_text or not resume_text.strip():
            logger.info("Email extraction skipped: input text is empty or whitespace.")
            return None
        
        # Truncate text if it's too long to avoid token limits
        truncated_text = resume_text[:4000]  # Using a conservative limit
        
        prompt = f"""
        Extract the email address from the following resume text. Return ONLY the email address.
        If no email is found, respond with "No email found".
        
        Resume text:
        {truncated_text}
        """
        
        try:
            response = self._call_ollama(prompt)
            
            # Extract the content from the response
            if response and "choices" in response:
                content = response["choices"][0]["message"]["content"].strip()
                
                # Check if the response indicates no email was found
                if content.lower() == "no email found":
                    return None
                
                # Basic email validation - not comprehensive but helps filter obvious non-emails
                if "@" in content and "." in content:
                    # Extract just the email if there's additional text
                    import re
                    email_match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', content)
                    if email_match:
                        return email_match.group(0)
                    return content
                
                return None
            
            return None
        
        except Exception as e:
            logger.error(f"Error extracting email with Ollama: {e}", exc_info=True)
            return None
    
    def extract_candidate_details(self, resume_text: str) -> Dict[str, Any]:
        """
        Extract comprehensive candidate details from resume text.
        
        Args:
            resume_text: The text content of the resume
            
        Returns:
            Dictionary containing extracted details like name, email, skills, experience, etc.
        """
        if not resume_text or not resume_text.strip():
            logger.info("Candidate extraction skipped: input text is empty or whitespace.")
            return {}
        
        # Truncate text if it's too long
        truncated_text = resume_text[:4000]
        
        prompt = f"""
        Extract the following information from this resume and return as JSON:
        1. Full name
        2. Email address
        3. Phone number
        4. Skills (as an array)
        5. Years of experience (as a number)
        6. Education (highest degree)
        
        For any field where information isn't found, use null.
        
        Resume text:
        {truncated_text}
        """
        
        try:
            response = self._call_ollama(prompt)
            
            if response and "choices" in response:
                content = response["choices"][0]["message"]["content"].strip()
                
                # Try to parse the JSON response
                try:
                    # Find JSON in the response (handles cases where the model outputs extra text)
                    import re
                    json_match = re.search(r'({[\s\S]*})', content)
                    if json_match:
                        parsed_json = json.loads(json_match.group(1))
                        return parsed_json
                    
                    # If no JSON pattern found, try parsing the whole content
                    return json.loads(content)
                except json.JSONDecodeError:
                    logger.error("Failed to parse JSON from Ollama response")
                    return {"error": "Failed to parse candidate details"}
            
            return {}
        
        except Exception as e:
            logger.error(f"Error extracting candidate details with Ollama: {e}", exc_info=True)
            return {}
    
    def compare_candidate_with_jd(self, candidate_info: Dict[str, Any], job_info: Dict[str, Any]) -> float:
        """
        Compare a candidate with a job description and return a match score.
        
        Args:
            candidate_info: Dictionary containing candidate details
            job_info: Dictionary containing job details
            
        Returns:
            Match score between 0 and 1
        """
        # Prepare additional info for prompt
        additional_info = candidate_info.get("additional_info", {})
        if isinstance(additional_info, str):
            try:
                additional_info = json.loads(additional_info)
            except:
                additional_info = {"data": additional_info}
        
        # Prepare prompt for Ollama
        prompt = f"""
        You are a skilled HR talent matcher. I'm going to give you information about a job and a candidate.
        
        JOB DESCRIPTION:
        {job_info.get('jd_text', '')}
        
        JOB TITLE: {job_info.get('title', '')}
        BUDGET RANGE: {job_info.get('min_budget', '')} - {job_info.get('max_budget', '')}
        
        CANDIDATE INFORMATION:
        Name: {candidate_info.get('name', '')}
        Resume: {candidate_info.get('resume_text', '')}
        Current CTC: {candidate_info.get('current_ctc', '')}
        Expected CTC: {candidate_info.get('expected_ctc', '')}
        Additional Information: {json.dumps(additional_info, indent=2)}
        
        Based on this information, evaluate how well the candidate matches the job requirements on a scale of 0 to 1.0.
        Consider skills, experience, salary expectations vs. budget, and all other relevant factors.
        
        Return just the numerical score between 0 and 1.0 without any explanation.
        """
        
        try:
            response = self._call_ollama(prompt)
            
            # Extract score from response
            if response and "choices" in response:
                score_text = response["choices"][0]["message"]["content"].strip()
                try:
                    score = float(score_text)
                    # Ensure score is between 0 and 1
                    score = max(0.0, min(1.0, score))
                    return score
                except ValueError:
                    logger.error(f"Failed to parse score from Ollama response: {score_text}")
                    return 0.5
            
            return 0.5
        
        except Exception as e:
            logger.error(f"Error comparing candidate with JD using Ollama: {e}", exc_info=True)
            return 0.5
    
    def compare_candidates(self, candidates_info: List[Dict[str, Any]], job_info: Dict[str, Any]) -> Dict[int, float]:
        """
        Compare candidates with each other in context of a job and return comparative scores.
        
        Args:
            candidates_info: List of dictionaries containing candidate details
            job_info: Dictionary containing job details
            
        Returns:
            Dictionary with candidate IDs as keys and comparative scores as values
        """
        # If no candidates or only one candidate, return early
        if not candidates_info or len(candidates_info) <= 1:
            return {c.get('id', i): 0.5 for i, c in enumerate(candidates_info)}
        
        # Prepare candidate information for the prompt
        prompt_candidates = []
        for c in candidates_info:
            # Process additional info
            additional_info = c.get('additional_info', {})
            if isinstance(additional_info, str):
                try:
                    additional_info = json.loads(additional_info)
                except:
                    additional_info = {"data": additional_info}
            
            # Get resume text and truncate if too long
            resume_text = c.get('resume_text', '')
            truncated_resume = resume_text[:1000] + "..." if len(resume_text) > 1000 else resume_text
            
            prompt_candidates.append({
                "id": c.get('id'),
                "name": c.get('name', ''),
                "resume": truncated_resume,
                "current_ctc": c.get('current_ctc', ''),
                "expected_ctc": c.get('expected_ctc', ''),
                "additional_info": additional_info
            })
        
        # Prepare prompt for Ollama
        prompt = f"""
        You are a skilled HR talent matcher. I'm going to give you information about a job and multiple candidates.
        
        JOB DESCRIPTION:
        {job_info.get('jd_text', '')}
        
        JOB TITLE: {job_info.get('title', '')}
        BUDGET RANGE: {job_info.get('min_budget', '')} - {job_info.get('max_budget', '')}
        
        CANDIDATES:
        {json.dumps(prompt_candidates, indent=2)}
        
        Compare the candidates with each other in the context of this job. Rank them based on their qualifications, 
        experience, skills, and salary expectations.
        
        Return a JSON object with candidate IDs as keys and scores between 0 and 1.0 as values, representing their 
        comparative ranking. Higher scores indicate better candidates.
        
        Example output format:
        {{"1": 0.9, "2": 0.7, "3": 0.85}}
        
        Return only the JSON object without any explanation.
        """
        
        try:
            response = self._call_ollama(prompt)
            
            # Extract scores from response
            if response and "choices" in response:
                score_text = response["choices"][0]["message"]["content"].strip()
                try:
                    # Find JSON in the response (handles cases where the model outputs extra text)
                    import re
                    json_match = re.search(r'({[\s\S]*})', score_text)
                    if json_match:
                        scores = json.loads(json_match.group(1))
                    else:
                        # If no JSON pattern found, try parsing the whole content
                        scores = json.loads(score_text)
                    
                    # Convert string keys to integers and ensure scores are between 0 and 1
                    return {int(k): max(0.0, min(1.0, float(v))) for k, v in scores.items()}
                except (ValueError, json.JSONDecodeError) as e:
                    logger.error(f"Failed to parse scores from Ollama response: {e}")
                    return {c.get('id', i): 0.5 for i, c in enumerate(candidates_info)}
            
            # Default scores if API call failed
            return {c.get('id', i): 0.5 for i, c in enumerate(candidates_info)}
        
        except Exception as e:
            logger.error(f"Error comparing candidates using Ollama: {e}", exc_info=True)
            return {c.get('id', i): 0.5 for i, c in enumerate(candidates_info)}
    
    def rank_resumes(self, job_description: str, resumes: List[str]) -> Dict[str, Any]:
        """
        Rank multiple resumes against a job description.
        
        Args:
            job_description: The job description text
            resumes: List of resume texts
            
        Returns:
            Dictionary with detailed analysis of each resume
        """
        if not job_description or not resumes:
            return {}
        
        # Truncate texts to avoid token limits
        truncated_jd = job_description[:2000]
        truncated_resumes = [r[:2000] + "..." if len(r) > 2000 else r for r in resumes]
        
        # Prepare the prompt
        prompt = f"""
        You are a skilled HR talent matcher. I'm going to give you a job description and {len(resumes)} resumes.
        
        JOB DESCRIPTION:
        {truncated_jd}
        
        """
        
        # Add each resume to the prompt
        for i, resume in enumerate(truncated_resumes):
            prompt += f"""
            RESUME {i+1}:
            {resume}
            
            """
        
        prompt += f"""
        Analyze each resume against the job description and provide a detailed analysis in JSON format with the following structure:
        {{
            "rankings": [
                {{
                    "resume_id": 1,
                    "overall_score": 0.85,
                    "skills_match": 0.80,
                    "experience_match": 0.90,
                    "strengths": ["strength1", "strength2"],
                    "weaknesses": ["weakness1", "weakness2"],
                    "recommendation": "Brief hiring recommendation"
                }},
                ...
            ],
            "comparative_analysis": {{
                "best_match": 1,
                "reasoning": "Brief explanation for best match"
            }}
        }}
        
        Provide only the JSON response, no additional text.
        """
        
        try:
            response = self._call_ollama(prompt)
            
            if response and "choices" in response:
                content = response["choices"][0]["message"]["content"].strip()
                
                # Try to parse the JSON response
                try:
                    # Find JSON in the response (handles cases where the model outputs extra text)
                    import re
                    json_match = re.search(r'({[\s\S]*})', content)
                    if json_match:
                        parsed_json = json.loads(json_match.group(1))
                        return parsed_json
                    
                    # If no JSON pattern found, try parsing the whole content
                    return json.loads(content)
                except json.JSONDecodeError:
                    logger.error("Failed to parse JSON from Ollama response for resume ranking")
                    return {"error": "Failed to parse ranking analysis"}
            
            return {}
        
        except Exception as e:
            logger.error(f"Error ranking resumes with Ollama: {e}", exc_info=True)
            return {"error": f"Failed to rank resumes: {str(e)}"}
    
    def _call_ollama(self, prompt: str) -> Dict[str, Any]:
        """
        Make a call to the Ollama API.
        
        Args:
            prompt: The user prompt to send to the model
            
        Returns:
            API response as a dictionary
        """
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        try:
            response = requests.post(
                self.completions_endpoint,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30  # Add timeout to prevent hanging
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                return {}
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Request to Ollama failed: {e}", exc_info=True)
            return {} 