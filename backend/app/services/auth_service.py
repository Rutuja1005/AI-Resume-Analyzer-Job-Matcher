from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.auth import UserRegister, UserLogin
from app.utils.security import get_password_hash, verify_password, create_access_token

class AuthService:
    def register_user(self, db: Session, user_in: UserRegister) -> dict:
        existing = db.query(User).filter(User.email == user_in.email.lower()).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email address already exists."
            )

        hashed_pwd = get_password_hash(user_in.password)
        db_user = User(
            email=user_in.email.lower(),
            hashed_password=hashed_pwd,
            full_name=user_in.full_name or "Candidate",
            role="candidate"
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        token = create_access_token(data={"sub": db_user.id, "email": db_user.email})
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": db_user
        }

    def authenticate_user(self, db: Session, login_data: UserLogin) -> dict:
        user = db.query(User).filter(User.email == login_data.email.lower()).first()
        if not user or not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = create_access_token(data={"sub": user.id, "email": user.email})
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": user
        }

auth_service = AuthService()
