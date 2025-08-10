from fastapi import FastAPI, UploadFile, File, HTTPException,Form
from db.db import SessionLocal, engine
from models.resume import Base, Resume, JobDescription
from utils.pdf_utils import extract_text_from_pdf
from utils.resume_parser import parse_resume_with_gemini
from utils.matching_service import create_application
import shutil
import tempfile
import os
from api.applications import router as applications_router
from api.jobs import router as jobs_router 

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(applications_router)
app.include_router(jobs_router)
class JobApplicationRequest:
    def __init__(self, file: UploadFile = File(...), job_id: int = Form(...)):
        self.file = file
        self.job_id = job_id

@app.post("/upload-resume/")
async def upload_resume_and_apply(
    file: UploadFile = File(..., description="PDF resume file"),
    job_id: int = Form(..., description="ID of job to apply for")
):
    """
    Upload a resume PDF and create a job application.
    
    - **file**: PDF resume file (required)
    - **job_id**: ID of job to apply for (required)
    """
    # Verify job exists first
    db = SessionLocal()
    job = db.query(JobDescription).filter(JobDescription.id == job_id).first()
    db.close()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Save file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        # Extract text from PDF
        text = extract_text_from_pdf(tmp_path)
        if not text:
            raise HTTPException(status_code=400, detail="Failed to extract text from PDF")

        # Parse resume with AI
        parsed_data = parse_resume_with_gemini(text)
        
        # Save resume to database
        db = SessionLocal()
        try:
            resume = Resume(**parsed_data)
            db.add(resume)
            db.commit()
            db.refresh(resume)
            
            # Create application
            application = create_application(resume.id, job_id)
            
            return {
                "resume": {
                    "id": resume.id,
                    "name": resume.name,
                    "email": resume.email
                },
                "application": {
                    "id": application.id,
                    "job_id": job_id,
                    "job_title": job.title
                    
                },
                "message": "Resume processed and application created successfully"
            }
            
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        finally:
            db.close()
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up temporary file
        try:
            os.unlink(tmp_path)
        except:
            pass