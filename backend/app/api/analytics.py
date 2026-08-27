from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.analysis import DashboardStatsResponse
from app.services.analysis_service import analysis_service
from app.utils.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/analytics", tags=["Dashboard Analytics"])

@router.get("/dashboard", response_model=DashboardStatsResponse, summary="Get Dashboard Analytics")
def get_dashboard_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns aggregated KPIs, match trends, score distributions,
    and frequent missing skill frequencies for the user dashboard.
    """
    return analysis_service.get_dashboard_stats(db, current_user)
