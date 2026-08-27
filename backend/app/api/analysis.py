from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import json
from app.database.connection import get_db
from app.schemas.analysis import MatchRequest, MatchResponse, AnalysisHistoryItem
from app.services.analysis_service import analysis_service
from app.utils.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/analysis", tags=["Analysis & Matching"])

@router.post("/match", response_model=MatchResponse, status_code=status.HTTP_201_CREATED, summary="Match Resume with Job Description")
def match_resume_to_job(
    request: MatchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Executes full ML similarity matching, ATS compliance scoring,
    and missing skill gap roadmap generation.
    """
    return analysis_service.run_match_analysis(db, request, current_user)

@router.get("/history", response_model=List[AnalysisHistoryItem], summary="Get Analysis History")
def get_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieves all past match analyses for the authenticated user."""
    return analysis_service.get_analysis_history(db, current_user)

@router.get("/{id}", response_model=MatchResponse, summary="Get Full Analysis by ID")
def get_analysis(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieves full analysis score breakdown, ATS audit, and missing skills."""
    return analysis_service.get_analysis_by_id(db, id, current_user)

@router.get("/{id}/export", summary="Export Analysis Report")
def export_analysis_report(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Exports structured analysis report as a formatted JSON document."""
    report = analysis_service.get_analysis_by_id(db, id, current_user)
    # Convert datetime to ISO string
    if "created_at" in report and hasattr(report["created_at"], "isoformat"):
        report["created_at"] = report["created_at"].isoformat()

    json_data = json.dumps(report, indent=2)
    return Response(
        content=json_data,
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename=Analysis_Report_{id[:8]}.json"}
    )
