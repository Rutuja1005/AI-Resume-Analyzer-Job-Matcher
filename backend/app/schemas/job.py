from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime

class JobAnalyzeRequest(BaseModel):
    title: Optional[str] = "Software Engineer"
    company: Optional[str] = "Target Company"
    job_description_text: str

class ExtractedJobData(BaseModel):
    title: str
    company: Optional[str] = None
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    skills_by_category: Dict[str, List[str]] = {}
    education_requirements: List[str] = []
    experience_level: Optional[str] = None
    important_keywords: List[str] = []
    raw_text: str

class JobResponse(BaseModel):
    id: str
    title: str
    company: Optional[str] = None
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    skills_by_category: Dict[str, List[str]] = {}
    education_requirements: List[str] = []
    experience_level: Optional[str] = None
    important_keywords: List[str] = []
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
