from google import genai
from models.resume import Resume, JobDescription, Application, SelectionStatus
from db.db import SessionLocal
import json
from typing import Dict, Any
from utils.send_email import send_status_email
from config import GEMINI_API_KEY
client = genai.Client(api_key=GEMINI_API_KEY)  # Replace with your actual API key

def analyze_match(resume: Dict[str, Any], job: Dict[str, Any]) -> Dict[str, Any]:
    prompt = f"""
You are an expert hiring assistant analyzing a job application. Perform a detailed analysis and provide:

1. MATCH SCORE (0-100): Calculate based on:
   - Skills match (weight: 40%)
   - Experience relevance (weight: 30%)
   - Qualifications alignment (weight: 20%)
   - Other factors (e.g., certifications, projects) (weight: 10%)

2. SELECTION STATUS:
   - "Shortlisted" (score ≥ 75)
   - "Pending" (score 50-74)
   - "Rejected" (score < 50)

3. DETAILED FEEDBACK:
   - Top 3 strengths
   - Top 3 areas for improvement
   - Any critical missing requirements

RESUME DATA:
{json.dumps(resume, indent=2)}

JOB DESCRIPTION:
{json.dumps(job, indent=2)}

IMPORTANT:
- Return ONLY valid JSON format
- Don't include any explanatory text
- Use this exact structure:
{{
  "match_score": number,
  "status": "Shortlisted|Pending|Rejected",
  "feedback": string,
  "strengths": [string, string, string],
  "improvement_areas": [string, string, string],
  "missing_requirements": [string]
}}
"""
    
    try:
        # Correct API call syntax
        response =client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        # Parse response
        if response.candidates and response.candidates[0].content.parts:
            response_text = response.candidates[0].content.parts[0].text
            clean_response = response_text.replace('```json', '').replace('```', '').strip()
            
            try:
                result = json.loads(clean_response)
                return {
                    "match_score": result.get("match_score", 0),
                    "status": result.get("status", "Pending"),
                    "feedback": result.get("feedback", "Analysis in progress")
                   }
            except json.JSONDecodeError:
                print(f"Failed to parse response: {clean_response}")
                return fallback_response()
                
        return fallback_response()
    
    except Exception as e:
        print(f"Error analyzing match: {e}")
        return fallback_response()

def fallback_response() -> Dict[str, Any]:
    return {
        "match_score": 0,
        "status": "Pending",
        "feedback": "System is currently analyzing this application",
    }
def create_application(resume_id: int, job_id: int) -> Application:
    db = SessionLocal()
    try:
        # Get resume and job with database relationship
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        job = db.query(JobDescription).filter(JobDescription.id == job_id).first()
        
        if not resume or not job:
            raise ValueError("Resume or Job not found")
        
        # Prepare data for AI analysis
        resume_data = {
            "skills": resume.skills,
            "experience": resume.experience_years
        }
        
        job_data = {
            "required_skills": job.required_skills,
            "min_experience": job.min_experience
        }
        
        # Get AI analysis (your existing Gemini integration)
        analysis = analyze_match(resume_data, job_data)
        
        # Create application
        application = Application(
            resume_id=resume_id,
            job_id=job_id,
            match_score=analysis["match_score"],
            status=SelectionStatus[analysis["status"].upper()],
            feedback=analysis["feedback"]
        )
        
        db.add(application)
        db.commit()
        db.refresh(application)
        status= send_status_email(
            applicant_email=str(resume.email),
            applicant_name=str(resume.name),
            status_data={
                "match_score": analysis["match_score"],
                "status": analysis["status"],
                "feedback": analysis["feedback"]
            },
            job_title=str(job.title)
        )
        print(f"Email sent successfully: {status}")
        return application
        
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()