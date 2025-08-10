from models.resume import JobDescription
from db.db import SessionLocal
from typing import List

def create_job_description(
    title: str,
    company: str,
    description: str,
    required_skills: List[str],
    required_qualifications: List[str],
    min_experience: float,
    location: str,
    salary_range: str
) -> JobDescription:
    db = SessionLocal()
    try:
        job = JobDescription(
            title=title,
            company=company,
            description=description,
            required_skills=required_skills,
            required_qualifications=required_qualifications,
            min_experience=min_experience,
            location=location,
            salary_range=salary_range
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        return job
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def get_all_job_descriptions() -> List[JobDescription]:
    db = SessionLocal()
    try:
        return db.query(JobDescription).all()
    finally:
        db.close()

def get_job_description_by_id(job_id: int) -> JobDescription:
    db = SessionLocal()
    try:
        return db.query(JobDescription).filter(JobDescription.id == job_id).first()
    finally:
        db.close()