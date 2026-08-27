from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.schemas.job import JobAnalyzeRequest, JobResponse
from app.services.analysis_service import analysis_service
from app.utils.security import get_current_user
from app.models.user import User
from app.models.job import JobDescription

router = APIRouter(prefix="/jobs", tags=["Job Descriptions"])

@router.post("/analyze", response_model=JobResponse, status_code=status.HTTP_201_CREATED, summary="Analyze & Save Job Description")
def analyze_job(
    request: JobAnalyzeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Parses job posting text, extracts required and preferred skill entities,
    categorizes tech domains, infers seniority level, and saves to database.
    """
    job = analysis_service.analyze_and_save_job(
        db=db,
        text=request.job_description_text,
        title=request.title,
        company=request.company,
        user=current_user
    )
    
    # Categorize skills
    by_category = {}
    for s in job.job_skills:
        cat = s.category or "General"
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(s.skill_name)

    return {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "required_skills": [s.skill_name for s in job.job_skills if s.is_required],
        "preferred_skills": [s.skill_name for s in job.job_skills if not s.is_required],
        "skills_by_category": by_category,
        "education_requirements": job.education_requirements or [],
        "experience_level": job.experience_level,
        "important_keywords": job.keywords_json or [],
        "created_at": job.created_at
    }

@router.get("", response_model=List[JobResponse], summary="List saved job descriptions")
def list_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieves all job descriptions analyzed by the authenticated user."""
    jobs = db.query(JobDescription).filter(JobDescription.user_id == current_user.id).order_by(JobDescription.created_at.desc()).all()
    results = []
    for job in jobs:
        by_category = {}
        for s in job.job_skills:
            cat = s.category or "General"
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(s.skill_name)

        results.append({
            "id": job.id,
            "title": job.title,
            "company": job.company,
            "required_skills": [s.skill_name for s in job.job_skills if s.is_required],
            "preferred_skills": [s.skill_name for s in job.job_skills if not s.is_required],
            "skills_by_category": by_category,
            "education_requirements": job.education_requirements or [],
            "experience_level": job.experience_level,
            "important_keywords": job.keywords_json or [],
            "created_at": job.created_at
        })
    return results

@router.get("/{id}", response_model=JobResponse, summary="Get single job description")
def get_job(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieves single job description by ID."""
    job = db.query(JobDescription).filter(JobDescription.id == id, JobDescription.user_id == current_user.id).first()
    if not job:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Job description not found")

    by_category = {}
    for s in job.job_skills:
        cat = s.category or "General"
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(s.skill_name)

    return {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "required_skills": [s.skill_name for s in job.job_skills if s.is_required],
        "preferred_skills": [s.skill_name for s in job.job_skills if not s.is_required],
        "skills_by_category": by_category,
        "education_requirements": job.education_requirements or [],
        "experience_level": job.experience_level,
        "important_keywords": job.keywords_json or [],
        "created_at": job.created_at
    }
