from fastapi import APIRouter, HTTPException
from models.resume import JobDescription
from utils.job_service import (
    create_job_description,
    get_all_job_descriptions,
    get_job_description_by_id
)
from pydantic import BaseModel
from typing import List

router = APIRouter(
    prefix="/job-descriptions",
    tags=["job_descriptions"]
)

class JobDescriptionCreate(BaseModel):
    title: str
    company: str
    description: str
    required_skills: List[str]
    required_qualifications: List[str]
    min_experience: float
    location: str
    salary_range: str

class JobDescriptionResponse(JobDescriptionCreate):
    id: int

    class Config:
        orm_mode = True

@router.post("/", response_model=JobDescriptionResponse)
def create_job(job: JobDescriptionCreate):
    try:
        return create_job_description(**job.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[JobDescriptionResponse])
def read_jobs():
    return get_all_job_descriptions()

@router.get("/{job_id}", response_model=JobDescriptionResponse)
def read_job(job_id: int):
    job = get_job_description_by_id(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job