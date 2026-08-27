from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from app.models.user import User
from app.models.resume import Resume, ResumeSkill
from app.models.job import JobDescription, JobSkill
from app.models.analysis import AnalysisResult, MissingSkill
from app.schemas.analysis import MatchRequest
from app.ml.jd_analyzer import jd_analyzer
from app.ml.matcher import resume_matcher
from app.ml.ats_scorer import ats_scorer
from app.ml.roadmap_generator import roadmap_generator
from app.ml.skill_ontology import get_skill_category

class AnalysisService:
    def analyze_and_save_job(
        self,
        db: Session,
        text: str,
        title: Optional[str],
        company: Optional[str],
        user: User
    ) -> JobDescription:
        if not text or len(text.strip()) < 30:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Job description text is too short. Please provide a detailed job posting."
            )

        extracted = jd_analyzer.analyze(text, title=title, company=company)
        
        job = JobDescription(
            user_id=user.id,
            title=extracted["title"],
            company=extracted["company"],
            raw_text=text,
            education_requirements=extracted["education_requirements"],
            experience_level=extracted["experience_level"],
            keywords_json=extracted["important_keywords"]
        )
        db.add(job)
        db.commit()
        db.refresh(job)

        # Add job skills
        for skill_name in extracted["all_skills"]:
            is_req = skill_name in extracted["required_skills"]
            cat = get_skill_category(skill_name)
            js = JobSkill(
                job_id=job.id,
                skill_name=skill_name,
                category=cat,
                is_required=is_req,
                importance_level="high" if is_req else "medium"
            )
            db.add(js)

        db.commit()
        db.refresh(job)
        return job

    def run_match_analysis(
        self,
        db: Session,
        request: MatchRequest,
        user: User
    ) -> Dict[str, Any]:
        # 1. Fetch Resume
        resume = db.query(Resume).filter(Resume.id == request.resume_id, Resume.user_id == user.id).first()
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found or unauthorized access."
            )

        # 2. Get or create Job Description
        job = None
        if request.job_description_id:
            job = db.query(JobDescription).filter(JobDescription.id == request.job_description_id, JobDescription.user_id == user.id).first()
        
        if not job and request.job_description_text:
            job = self.analyze_and_save_job(
                db=db,
                text=request.job_description_text,
                title=request.job_title,
                company=request.company,
                user=user
            )
        
        if not job:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A valid Job Description ID or Job Description text is required for matching."
            )

        # Prepare payloads for ML matching
        resume_skills = [s.skill_name for s in resume.skills]
        job_skills = [s.skill_name for s in job.job_skills]

        resume_payload = {
            "raw_text": resume.raw_text,
            "skills": resume_skills,
            "education": resume.education_json or [],
            "experience": resume.experience_json or [],
            "projects": resume.projects_json or [],
            "certifications": resume.certifications_json or [],
            "summary": resume.summary_text,
            "name": resume.candidate_name,
            "email": resume.candidate_email,
            "phone": resume.candidate_phone
        }

        job_payload = {
            "raw_text": job.raw_text,
            "all_skills": job_skills,
            "required_skills": [s.skill_name for s in job.job_skills if s.is_required],
            "education_requirements": job.education_requirements or [],
            "experience_level": job.experience_level or "",
            "important_keywords": job.keywords_json or []
        }

        # 3. Execute Match Engine
        match_data = resume_matcher.match(resume_payload, job_payload)

        # 4. Execute ATS Scorer
        ats_data = ats_scorer.evaluate(
            resume_data=resume_payload,
            job_data=job_payload,
            matching_skills_count=len(match_data["matching_skills"])
        )

        # 5. Generate Skill Gap Roadmap
        missing_roadmap = roadmap_generator.generate_missing_skills_roadmap(match_data["missing_skills_raw"])

        # 6. Synthesize Top Actionable Recommendations
        recommendations = ats_data.get("critical_improvements", [])
        if missing_roadmap:
            top_3_missing = [m["skill_name"] for m in missing_roadmap[:3]]
            recommendations.insert(0, f"Prioritize acquiring target skills: {', '.join(top_3_missing)}.")

        # 7. Save AnalysisResult to DB
        analysis_record = AnalysisResult(
            user_id=user.id,
            resume_id=resume.id,
            job_description_id=job.id,
            overall_match_score=match_data["overall_match_score"],
            skill_match_score=match_data["skill_match_score"],
            keyword_match_score=match_data["keyword_match_score"],
            education_match_score=match_data["education_match_score"],
            experience_match_score=match_data["experience_match_score"],
            ats_score=ats_data["total_ats_score"],
            ats_breakdown_json=ats_data,
            matching_skills_json=match_data["matching_skills"],
            match_explanation=match_data["match_explanation"],
            recommendations_json=recommendations
        )
        db.add(analysis_record)
        db.commit()
        db.refresh(analysis_record)

        # 8. Save Missing Skills entries
        for m in missing_roadmap:
            ms = MissingSkill(
                analysis_id=analysis_record.id,
                skill_name=m["skill_name"],
                importance=m["importance"],
                reason=m["reason"],
                suggested_learning_topic=m["suggested_learning_topic"],
                learning_resource_url=m["learning_resource_url"]
            )
            db.add(ms)

        db.commit()
        db.refresh(analysis_record)

        return {
            "analysis_id": analysis_record.id,
            "resume_id": resume.id,
            "job_description_id": job.id,
            "job_title": job.title,
            "company": job.company,
            "candidate_name": resume.candidate_name,
            "overall_match_score": analysis_record.overall_match_score,
            "skill_match_score": analysis_record.skill_match_score,
            "keyword_match_score": analysis_record.keyword_match_score,
            "education_match_score": analysis_record.education_match_score,
            "experience_match_score": analysis_record.experience_match_score,
            "ats_score": analysis_record.ats_score,
            "matching_skills": match_data["matching_skills"],
            "missing_skills": missing_roadmap,
            "all_job_skills": job_skills,
            "important_keywords": job.keywords_json or [],
            "ats_breakdown": ats_data,
            "match_explanation": analysis_record.match_explanation,
            "recommendations": recommendations,
            "created_at": analysis_record.created_at
        }

    def get_analysis_by_id(self, db: Session, analysis_id: str, user: User) -> Dict[str, Any]:
        analysis = db.query(AnalysisResult).filter(AnalysisResult.id == analysis_id, AnalysisResult.user_id == user.id).first()
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Analysis record not found or unauthorized access."
            )

        resume = analysis.resume
        job = analysis.job_description
        missing_skills = db.query(MissingSkill).filter(MissingSkill.analysis_id == analysis.id).all()

        missing_list = [
            {
                "skill_name": ms.skill_name,
                "importance": ms.importance,
                "reason": ms.reason,
                "suggested_learning_topic": ms.suggested_learning_topic,
                "learning_resource_url": ms.learning_resource_url
            }
            for ms in missing_skills
        ]

        return {
            "analysis_id": analysis.id,
            "resume_id": resume.id if resume else None,
            "job_description_id": job.id if job else None,
            "job_title": job.title if job else "Target Position",
            "company": job.company if job else "Target Organization",
            "candidate_name": resume.candidate_name if resume else "Candidate",
            "overall_match_score": analysis.overall_match_score,
            "skill_match_score": analysis.skill_match_score,
            "keyword_match_score": analysis.keyword_match_score,
            "education_match_score": analysis.education_match_score,
            "experience_match_score": analysis.experience_match_score,
            "ats_score": analysis.ats_score,
            "matching_skills": analysis.matching_skills_json or [],
            "missing_skills": missing_list,
            "all_job_skills": [s.skill_name for s in job.job_skills] if job else [],
            "important_keywords": job.keywords_json if job else [],
            "ats_breakdown": analysis.ats_breakdown_json or {},
            "match_explanation": analysis.match_explanation,
            "recommendations": analysis.recommendations_json or [],
            "created_at": analysis.created_at
        }

    def get_analysis_history(self, db: Session, user: User) -> List[Dict[str, Any]]:
        analyses = db.query(AnalysisResult).filter(AnalysisResult.user_id == user.id).order_by(AnalysisResult.created_at.desc()).all()
        history = []
        for a in analyses:
            missing_cnt = len(a.missing_skills)
            matching_cnt = len(a.matching_skills_json) if a.matching_skills_json else 0
            history.append({
                "id": a.id,
                "job_title": a.job_description.title if a.job_description else "Untitled Role",
                "company": a.job_description.company if a.job_description else "Company",
                "candidate_name": a.resume.candidate_name if a.resume else "Candidate",
                "overall_match_score": a.overall_match_score,
                "skill_match_score": a.skill_match_score,
                "ats_score": a.ats_score,
                "matching_skills_count": matching_cnt,
                "missing_skills_count": missing_cnt,
                "created_at": a.created_at
            })
        return history

    def get_dashboard_stats(self, db: Session, user: User) -> Dict[str, Any]:
        total_resumes = db.query(Resume).filter(Resume.user_id == user.id).count()
        total_jobs = db.query(JobDescription).filter(JobDescription.user_id == user.id).count()
        total_analyses = db.query(AnalysisResult).filter(AnalysisResult.user_id == user.id).count()

        avg_match = db.query(func.avg(AnalysisResult.overall_match_score)).filter(AnalysisResult.user_id == user.id).scalar() or 0.0
        avg_ats = db.query(func.avg(AnalysisResult.ats_score)).filter(AnalysisResult.user_id == user.id).scalar() or 0.0

        recent_history = self.get_analysis_history(db, user)[:6]

        # Score trends (ordered chronologically)
        trend_records = db.query(AnalysisResult).filter(AnalysisResult.user_id == user.id).order_by(AnalysisResult.created_at.asc()).limit(10).all()
        score_trends = [
            {
                "date": a.created_at.strftime("%b %d"),
                "match_score": a.overall_match_score,
                "ats_score": a.ats_score,
                "job": a.job_description.title if a.job_description else "Role"
            }
            for a in trend_records
        ]

        # Top missing skills across analyses
        missing_query = (
            db.query(MissingSkill.skill_name, func.count(MissingSkill.id).label("freq"))
            .join(AnalysisResult)
            .filter(AnalysisResult.user_id == user.id)
            .group_by(MissingSkill.skill_name)
            .order_by(func.count(MissingSkill.id).desc())
            .limit(6)
            .all()
        )
        top_missing = [{"skill": m[0], "count": m[1]} for m in missing_query]

        # Skill category distribution in uploaded resumes
        cat_query = (
            db.query(ResumeSkill.category, func.count(ResumeSkill.id).label("freq"))
            .join(Resume)
            .filter(Resume.user_id == user.id)
            .group_by(ResumeSkill.category)
            .all()
        )
        cat_dist = [{"category": c[0] or "General", "count": c[1]} for c in cat_query]

        return {
            "total_resumes": total_resumes,
            "total_jobs": total_jobs,
            "total_analyses": total_analyses,
            "avg_match_score": round(float(avg_match), 1),
            "avg_ats_score": round(float(avg_ats), 1),
            "recent_analyses": recent_history,
            "score_trends": score_trends,
            "top_missing_skills": top_missing,
            "skill_category_distribution": cat_dist
        }

analysis_service = AnalysisService()
