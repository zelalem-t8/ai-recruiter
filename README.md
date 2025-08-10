# AI Recruiter

AI Recruiter is an intelligent recruitment automation platform built with Python and FastAPI. It leverages generative AI (Google Gemini) to parse resumes, match candidates to job descriptions, and streamline the application process for hiring teams.

## Features

- **Resume Parsing**: Upload a PDF resume and automatically extract key candidate information (name, email, phone, skills, qualifications, experience).
- **AI-Powered Matching**: Uses Google Gemini to analyze and score candidate-job fit based on skills, experience, and qualifications.
- **Automated Applications**: Creates job applications and assigns selection statuses (Shortlisted, Pending, Rejected) with detailed feedback.
- **Job Description Management**: Create, view, and manage job descriptions via API endpoints.
- **Database Integration**: Stores resumes, job descriptions, and applications with relationships for efficient querying.
- **API-first Design**: All functionality exposed as FastAPI endpoints for easy integration.

## Technologies Used

- **Python**
- **FastAPI** (web framework)
- **SQLAlchemy** (ORM)
- **PostgreSQL** (default, but configurable)
- **Google Gemini API** (AI resume parsing and matching)
- **Pydantic** (data validation)
- **Shutil, Tempfile, OS** (file handling utilities)

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL
- Google Gemini API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/zelalem-t8/ai-recruiter.git
   cd ai-recruiter
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   - Configure your PostgreSQL connection settings.
   - Add your `GEMINI_API_KEY` in a `.env` or your config file.

4. **Run database migrations**
   - Tables auto-create on first run via SQLAlchemy.

5. **Start the FastAPI server**
   ```bash
   uvicorn main:app --reload
   ```

### Usage

#### Upload Resume & Apply to Job

- **Endpoint:** `POST /upload-resume/`
- **Form Data:**
  - `file`: Resume PDF file
  - `job_id`: Target job description ID

Returns:
```json
{
  "resume": {
    "id": 1,
    "name": "Jane Doe",
    "email": "jane@example.com"
  },
  "application": {
    "id": 1,
    "job_id": 2,
    "job_title": "Software Engineer"
  },
  "message": "Resume processed and application created successfully"
}
```

#### Job Description Management

- **Create Job:** `POST /job-descriptions/`
- **List Jobs:** `GET /job-descriptions/`
- **Get Job:** `GET /job-descriptions/{job_id}`

#### AI Matching

- Resumes are analyzed and scored against job descriptions. Feedback includes match score, strengths, areas for improvement, and missing requirements.

## Database Models

- **Resume:** Candidate info, skills, qualifications, experience.
- **JobDescription:** Title, company, requirements, location, salary.
- **Application:** Links resume and job, stores status, match score, feedback.

## Example Flow

1. **Create a job description** via API.
2. **Upload a candidate’s resume** with the job ID.
3. **Resume is parsed and matched** using AI.
4. **Application is created** with feedback and status.

## License

*Currently not specified.*

## Contact

For questions or support, please contact [zelalem-t8](https://github.com/zelalem-t8).