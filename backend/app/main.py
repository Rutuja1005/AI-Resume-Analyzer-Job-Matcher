import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database.connection import engine, Base
from app.api import api_router
import app.models  # Ensure models are imported for metadata creation

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Resume Analyzer & Job Matcher API",
    description="""
    Production-grade REST API for parsing PDF resumes, analyzing job descriptions,
    computing multi-factor ML similarity scores, generating ATS compliance audits,
    and identifying prioritized skill gaps with learning roadmaps.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/api/openapi.json"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal Server Error: {str(exc)}"}
    )

# Healthcheck
@app.get("/api/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": "1.0.0"
    }

# Mount API Router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Root Endpoint
@app.get("/", tags=["System"])
def root():
    return {
        "message": "Welcome to AI Resume Analyzer & Job Matcher API",
        "docs": "/docs",
        "health": "/api/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
