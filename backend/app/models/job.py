import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, JSON, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.connection import Base

def generate_uuid():
    return str(uuid.uuid4())

class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False, default="Untitled Position")
    company = Column(String(255), nullable=True, default="Target Company")
    raw_text = Column(Text, nullable=False)
    
    # Extracted metadata
    education_requirements = Column(JSON, default=list)
    experience_level = Column(String(100), nullable=True)
    keywords_json = Column(JSON, default=list)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="job_descriptions")
    job_skills = relationship("JobSkill", back_populates="job_description", cascade="all, delete-orphan")
    analyses = relationship("AnalysisResult", back_populates="job_description", cascade="all, delete-orphan")


class JobSkill(Base):
    __tablename__ = "job_skills"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    job_id = Column(String(36), ForeignKey("job_descriptions.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_name = Column(String(100), nullable=False, index=True)
    category = Column(String(50), nullable=True)
    is_required = Column(Boolean, default=True)
    importance_level = Column(String(50), default="high")  # high, medium, low

    job_description = relationship("JobDescription", back_populates="job_skills")
