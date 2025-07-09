from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db import models
import json
from sqlalchemy import desc, func

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

def main():
    db = get_db()
    
    # Get unique candidates based on email
    unique_candidates = db.query(
        models.Candidate
    ).group_by(
        models.Candidate.email
    ).all()
    
    print("\n=== Unique Candidates in Database (by email) ===\n")
    
    for candidate in unique_candidates:
        # Get the latest match for this candidate
        latest_match = db.query(
            models.CandidateJobMatch,
            models.Job
        ).join(
            models.Job,
            models.Job.id == models.CandidateJobMatch.job_id
        ).filter(
            models.CandidateJobMatch.candidate_email == candidate.email
        ).order_by(
            desc(models.CandidateJobMatch.created_at)
        ).first()
        
        if latest_match:
            match, job = latest_match
            print(f"\nCandidate: {candidate.name} ({candidate.email})")
            print(f"Current CTC: {candidate.current_ctc}")
            print(f"Expected CTC: {candidate.expected_ctc}")
            print(f"\nJob Description: {job.description[:200]}...")
            print(f"\nMatch Scores:")
            print(f"- Overall Score: {match.overall_score}")
            print(f"- Technical Match: {match.technical_match_score}")
            print(f"- Experience Match: {match.experience_match_score}")
            print(f"- Salary Match: {match.salary_match_score}")
            
            if match.strengths:
                print("\nStrengths:")
                strengths = json.loads(match.strengths)
                for strength in strengths:
                    print(f"- {strength}")
            
            if match.weaknesses:
                print("\nWeaknesses:")
                weaknesses = json.loads(match.weaknesses)
                for weakness in weaknesses:
                    print(f"- {weakness}")
            
            if match.salary_analysis:
                print("\nSalary Analysis:")
                print(match.salary_analysis)
            
            if match.recommendation:
                print("\nRecommendation:")
                print(match.recommendation)
            
            print("\n" + "="*50)
        else:
            print(f"\nCandidate: {candidate.name} ({candidate.email})")
            print("No matches found for this candidate")
            print("\n" + "="*50)

if __name__ == "__main__":
    main() 