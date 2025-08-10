from fastapi import APIRouter, HTTPException
from models.resume import Application, SelectionStatus
from utils.matching_service import create_application
from pydantic import BaseModel
from typing import Optional
from db.db import SessionLocal
router = APIRouter(
    prefix="/applications",
    tags=["applications"]
)

class ApplicationCreate(BaseModel):
    resume_id: int
    job_id: int

class ApplicationResponse(BaseModel):
    id: int
    resume_id: int
    job_id: int
    match_score: float
    status: str
    feedback: Optional[str] = None

    class Config:
        orm_mode = True

@router.post("/", response_model=ApplicationResponse)
def apply_to_job(application: ApplicationCreate):
    try:
        return create_application(
            resume_id=application.resume_id,
            job_id=application.job_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application(application_id: int):
    db = SessionLocal()
    try:
        application = db.query(Application).filter(Application.id == application_id).first()
        if not application:
            raise HTTPException(status_code=404, detail="Application not found")
        return application
    finally:
        db.close()