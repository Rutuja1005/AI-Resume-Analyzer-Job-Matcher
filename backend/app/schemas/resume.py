from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime

class ResumeSkillSchema(BaseModel):
    skill_name: str
    category: Optional[str] = "General"
    experience_years_estimated: Optional[int] = 0

    model_config = ConfigDict(from_attributes=True)

class ExtractedResumeData(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: List[str] = []
    skills_by_category: Dict[str, List[str]] = {}
    education: List[Dict[str, Any]] = []
    experience: List[Dict[str, Any]] = []
    projects: List[Dict[str, Any]] = []
    certifications: List[Dict[str, Any]] = []
    summary: Optional[str] = None
    raw_text: Optional[str] = None

class ResumeResponse(BaseModel):
    id: str
    filename: str
    file_size: int
    candidate_name: Optional[str] = None
    candidate_email: Optional[str] = None
    candidate_phone: Optional[str] = None
    skills: List[str] = []
    education: List[Dict[str, Any]] = []
    experience: List[Dict[str, Any]] = []
    projects: List[Dict[str, Any]] = []
    certifications: List[Dict[str, Any]] = []
    summary_text: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ResumeListResponse(BaseModel):
    total: int
    items: List[ResumeResponse]
