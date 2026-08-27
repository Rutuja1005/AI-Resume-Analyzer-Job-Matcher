from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.schemas.resume import ResumeResponse, ResumeListResponse
from app.services.resume_service import resume_service
from app.utils.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/resumes", tags=["Resumes"])

@router.post("/upload", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED, summary="Upload & Parse PDF Resume")
def upload_resume(
    file: UploadFile = File(..., description="PDF format resume file"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Accepts PDF resume upload, extracts raw text, candidate entities,
    categorized skills, education history, and saves to database.
    """
    resume = resume_service.save_and_parse_resume(db, file, current_user)
    return {
        "id": resume.id,
        "filename": resume.filename,
        "file_size": resume.file_size,
        "candidate_name": resume.candidate_name,
        "candidate_email": resume.candidate_email,
        "candidate_phone": resume.candidate_phone,
        "skills": [s.skill_name for s in resume.skills],
        "education": resume.education_json or [],
        "experience": resume.experience_json or [],
        "projects": resume.projects_json or [],
        "certifications": resume.certifications_json or [],
        "summary_text": resume.summary_text,
        "created_at": resume.created_at
    }

@router.get("", response_model=ResumeListResponse, summary="List all resumes for user")
def list_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieves all resumes associated with authenticated user."""
    resumes = resume_service.get_user_resumes(db, current_user)
    items = [
        {
            "id": r.id,
            "filename": r.filename,
            "file_size": r.file_size,
            "candidate_name": r.candidate_name,
            "candidate_email": r.candidate_email,
            "candidate_phone": r.candidate_phone,
            "skills": [s.skill_name for s in r.skills],
            "education": r.education_json or [],
            "experience": r.experience_json or [],
            "projects": r.projects_json or [],
            "certifications": r.certifications_json or [],
            "summary_text": r.summary_text,
            "created_at": r.created_at
        }
        for r in resumes
    ]
    return {"total": len(items), "items": items}

@router.get("/{id}", response_model=ResumeResponse, summary="Get single resume details")
def get_resume(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieves a single resume by its ID."""
    resume = resume_service.get_resume_by_id(db, id, current_user)
    return {
        "id": resume.id,
        "filename": resume.filename,
        "file_size": resume.file_size,
        "candidate_name": resume.candidate_name,
        "candidate_email": resume.candidate_email,
        "candidate_phone": resume.candidate_phone,
        "skills": [s.skill_name for s in resume.skills],
        "education": resume.education_json or [],
        "experience": resume.experience_json or [],
        "projects": resume.projects_json or [],
        "certifications": resume.certifications_json or [],
        "summary_text": resume.summary_text,
        "created_at": resume.created_at
    }

@router.delete("/{id}", summary="Delete resume")
def delete_resume(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Deletes uploaded resume file and database record."""
    return resume_service.delete_resume(db, id, current_user)
