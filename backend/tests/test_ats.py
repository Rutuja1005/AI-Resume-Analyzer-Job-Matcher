import pytest
from app.ml.ats_scorer import ats_scorer

def test_ats_scorer():
    resume_payload = {
        "raw_text": """
        Taylor Reed
        taylor.reed@sample.com
        (555) 444-3322
        
        Summary
        Results-driven engineer with 5 years building scalable web services and cloud native architectures.
        
        Experience
        Senior Software Engineer
        • Architected and deployed microservices reducing API latency by 40%.
        • Automated CI/CD pipelines increasing deployment frequency by 3x.
        • Spearheaded database migration to PostgreSQL saving $12,000 monthly in infrastructure costs.
        
        Skills
        Python, FastAPI, Docker, PostgreSQL, Redis, Kubernetes
        
        Education
        B.S. in Computer Science
        """,
        "skills": ["Python", "FastAPI", "Docker", "PostgreSQL", "Redis", "Kubernetes"],
        "education": [{"degree": "B.S. in Computer Science"}],
        "experience": [{"title_and_company": "Senior Software Engineer"}],
        "projects": [{"name": "Cloud Platform"}],
        "name": "Taylor Reed",
        "email": "taylor.reed@sample.com",
        "phone": "(555) 444-3322",
        "summary": "Results-driven engineer..."
    }

    job_payload = {
        "raw_text": "We need an engineer with Python, FastAPI, Docker, and PostgreSQL experience.",
        "all_skills": ["Python", "FastAPI", "Docker", "PostgreSQL", "Kubernetes"],
        "important_keywords": ["Python", "FastAPI", "Microservices", "Latency"]
    }

    ats_result = ats_scorer.evaluate(resume_payload, job_payload, matching_skills_count=4)
    assert ats_result["total_ats_score"] >= 70.0
    assert ats_result["contact_information"]["score"] == 15.0
    assert ats_result["section_completeness"]["score"] >= 15.0
    assert len(ats_result["strengths"]) > 0
