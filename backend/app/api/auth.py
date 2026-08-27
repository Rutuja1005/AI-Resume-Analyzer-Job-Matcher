from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.auth import UserRegister, UserLogin, Token, UserResponse
from app.services.auth_service import auth_service
from app.utils.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED, summary="Register a new user")
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    """Creates a new user profile with hashed password and generates initial JWT token."""
    return auth_service.register_user(db, user_in)

@router.post("/login", response_model=Token, summary="Authenticate user & obtain JWT")
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """Verifies user credentials and returns JWT bearer access token."""
    return auth_service.authenticate_user(db, login_data)

@router.get("/me", response_model=UserResponse, summary="Get current user details")
def get_me(current_user: User = Depends(get_current_user)):
    """Returns currently authenticated user profile."""
    return current_user
