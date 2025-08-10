# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String, Float, Text
# from sqlalchemy.dialects.postgresql import ARRAY
# from db.db import engine

# Base = declarative_base()

# class Resume(Base):
#     __tablename__ = "resumes"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     email = Column(String)
#     phone = Column(String)
#     qualifications = Column(ARRAY(String))
#     skills = Column(ARRAY(String))
#     experience_years = Column(Float)
# class JobDescription(Base):
#     __tablename__ = "job_descriptions"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String)
#     company = Column(String)
#     description = Column(Text)
#     required_qualifications = Column(ARRAY(String))
#     required_skills = Column(ARRAY(String))
#     min_experience = Column(Float)
#     location = Column(String)
#     salary_range = Column(String)  # e.g., "$50,000 - $70,000"
# Base.metadata.create_all(bind=engine)
# print("✅ Table created in database.")
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Text, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from db.db import engine

Base = declarative_base()

class SelectionStatus(PyEnum):
    PENDING = "Pending"
    SHORTLISTED = "Shortlisted"
    REJECTED = "Rejected"
    HIRED = "Hired"

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    qualifications = Column(ARRAY(String))
    skills = Column(ARRAY(String))
    experience_years = Column(Float)
    
    applications = relationship("Application", back_populates="resume")

class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    company = Column(String)
    description = Column(Text)
    required_qualifications = Column(ARRAY(String))
    required_skills = Column(ARRAY(String))
    min_experience = Column(Float)
    location = Column(String)
    salary_range = Column(String)
    
    applications = relationship("Application", back_populates="job")

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    job_id = Column(Integer, ForeignKey("job_descriptions.id"))
    status = Column(Enum(SelectionStatus), default=SelectionStatus.PENDING)
    match_score = Column(Float)
    feedback = Column(Text)
    
    resume = relationship("Resume", back_populates="applications")
    job = relationship("JobDescription", back_populates="applications")

Base.metadata.create_all(bind=engine)
print("✅ Tables created in database.")
