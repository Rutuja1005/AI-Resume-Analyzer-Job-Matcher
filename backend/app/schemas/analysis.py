from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime

class MatchRequest(BaseModel):
    resume_id: str
    job_description_id: Optional[str] = None
    job_description_text: Optional[str] = None
    job_title: Optional[str] = "Target Role"
    company: Optional[str] = "Target Company"

class MissingSkillDetail(BaseModel):
    skill_name: str
    importance: str  # High, Medium, Low
    reason: str
    suggested_learning_topic: str
    learning_resource_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ATSFactorScore(BaseModel):
    score: float
    max_score: float
    status: str  # passed, warning, failed
    feedback: str

class ATSBreakdown(BaseModel):
    keyword_coverage: ATSFactorScore
    section_completeness: ATSFactorScore
    contact_information: ATSFactorScore
    quantifiable_achievements: ATSFactorScore
    formatting_and_length: ATSFactorScore
    action_verbs_density: ATSFactorScore
    skill_relevance: ATSFactorScore
    total_ats_score: float
    strengths: List[str] = []
    critical_improvements: List[str] = []

class MatchResponse(BaseModel):
    analysis_id: str
    resume_id: str
    job_description_id: str
    job_title: str
    company: Optional[str] = None
    candidate_name: Optional[str] = None
    
    # Core Match Scores (0-100)
    overall_match_score: float
    skill_match_score: float
    keyword_match_score: float
    education_match_score: float
    experience_match_score: float
    ats_score: float
    
    # Skills Breakdown
    matching_skills: List[str] = []
    missing_skills: List[MissingSkillDetail] = []
    all_job_skills: List[str] = []
    important_keywords: List[str] = []
    
    # Detailed Assessments
    ats_breakdown: Dict[str, Any]
    match_explanation: str
    recommendations: List[str] = []
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AnalysisHistoryItem(BaseModel):
    id: str
    job_title: str
    company: Optional[str] = None
    candidate_name: Optional[str] = None
    overall_match_score: float
    skill_match_score: float
    ats_score: float
    matching_skills_count: int
    missing_skills_count: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class DashboardStatsResponse(BaseModel):
    total_resumes: int
    total_jobs: int
    total_analyses: int
    avg_match_score: float
    avg_ats_score: float
    recent_analyses: List[AnalysisHistoryItem]
    score_trends: List[Dict[str, Any]]
    top_missing_skills: List[Dict[str, Any]]
    skill_category_distribution: List[Dict[str, Any]]
