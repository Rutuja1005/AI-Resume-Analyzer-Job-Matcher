import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Text, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base

def generate_uuid():
    return str(uuid.uuid4())

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    resume_id = Column(String(36), ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, index=True)
    job_description_id = Column(String(36), ForeignKey("job_descriptions.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Quantitative Scores (0 - 100)
    overall_match_score = Column(Float, nullable=False, default=0.0)
    skill_match_score = Column(Float, nullable=False, default=0.0)
    keyword_match_score = Column(Float, nullable=False, default=0.0)
    education_match_score = Column(Float, nullable=False, default=0.0)
    experience_match_score = Column(Float, nullable=False, default=0.0)
    ats_score = Column(Float, nullable=False, default=0.0)
    
    # Qualitative & Breakdown Details
    ats_breakdown_json = Column(JSON, default=dict)
    matching_skills_json = Column(JSON, default=list)
    match_explanation = Column(Text, nullable=True)
    recommendations_json = Column(JSON, default=list)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="analyses")
    resume = relationship("Resume", back_populates="analyses")
    job_description = relationship("JobDescription", back_populates="analyses")
    missing_skills = relationship("MissingSkill", back_populates="analysis", cascade="all, delete-orphan")


class MissingSkill(Base):
    __tablename__ = "missing_skills"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    analysis_id = Column(String(36), ForeignKey("analysis_results.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_name = Column(String(100), nullable=False)
    importance = Column(String(50), default="High")       # High, Medium, Low
    reason = Column(Text, nullable=True)
    suggested_learning_topic = Column(String(255), nullable=True)
    learning_resource_url = Column(String(500), nullable=True)

    analysis = relationship("AnalysisResult", back_populates="missing_skills")
