import os
import uuid
import shutil
from typing import List, Optional
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from app.config import settings
from app.models.user import User
from app.models.resume import Resume, ResumeSkill
from app.ml.resume_parser import resume_parser
from app.ml.skill_ontology import get_skill_category

class ResumeService:
    def save_and_parse_resume(
        self,
        db: Session,
        file: UploadFile,
        user: User
    ) -> Resume:
        # 1. Validate file extension
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file format '{ext}'. Only PDF resumes (.pdf) are supported."
            )

        # 2. Save file to disk
        file_id = str(uuid.uuid4())
        safe_filename = f"{file_id}_{file.filename.replace(' ', '_')}"
        file_path = os.path.join(settings.UPLOAD_DIR, safe_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_size = os.path.getsize(file_path)
        if file_size > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
            os.remove(file_path)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE_MB}MB."
            )

        # 3. Parse PDF with NLP engine
        try:
            parsed = resume_parser.parse(file_path)
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Error parsing resume PDF: {str(e)}"
            )

        if not parsed.get("raw_text") or len(parsed.get("raw_text").strip()) < 20:
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded PDF appears empty or contains unscannable image-only text. Please provide an ATS-readable PDF."
            )

        # 4. Create Resume Record in DB
        resume_record = Resume(
            user_id=user.id,
            filename=file.filename,
            file_path=file_path,
            file_size=file_size,
            raw_text=parsed.get("raw_text", ""),
            candidate_name=parsed.get("name") or user.full_name,
            candidate_email=parsed.get("email") or user.email,
            candidate_phone=parsed.get("phone"),
            education_json=parsed.get("education", []),
            experience_json=parsed.get("experience", []),
            projects_json=parsed.get("projects", []),
            certifications_json=parsed.get("certifications", []),
            summary_text=parsed.get("summary")
        )
        db.add(resume_record)
        db.commit()
        db.refresh(resume_record)

        # 5. Save associated skills
        for skill_name in parsed.get("skills", []):
            cat = get_skill_category(skill_name)
            skill_entry = ResumeSkill(
                resume_id=resume_record.id,
                skill_name=skill_name,
                category=cat
            )
            db.add(skill_entry)

        db.commit()
        db.refresh(resume_record)
        return resume_record

    def get_user_resumes(self, db: Session, user: User) -> List[Resume]:
        return db.query(Resume).filter(Resume.user_id == user.id).order_by(Resume.created_at.desc()).all()

    def get_resume_by_id(self, db: Session, resume_id: str, user: User) -> Resume:
        resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == user.id).first()
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found or unauthorized access."
            )
        return resume

    def delete_resume(self, db: Session, resume_id: str, user: User) -> dict:
        resume = self.get_resume_by_id(db, resume_id, user)
        if resume.file_path and os.path.exists(resume.file_path):
            try:
                os.remove(resume.file_path)
            except Exception:
                pass

        db.delete(resume)
        db.commit()
        return {"success": True, "message": "Resume deleted successfully."}

resume_service = ResumeService()
