import pytest
from app.ml.matcher import resume_matcher

def test_matching_algorithm():
    resume_payload = {
        "raw_text": "Experienced Python Backend Engineer with strong expertise in FastAPI, PostgreSQL, Docker, Redis, and React. Built scalable microservices.",
        "skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "Redis", "React"],
        "education": [{"degree": "Bachelor of Science", "field_of_study": "Computer Science"}],
        "experience": [{"title_and_company": "Software Engineer (3 years)"}]
    }

    job_payload = {
        "raw_text": "Looking for a Python Backend Developer skilled in Python, FastAPI, PostgreSQL, Docker, and Kubernetes. AWS experience is a plus.",
        "all_skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "Kubernetes", "AWS"],
        "required_skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
        "education_requirements": ["Computer Science"],
        "experience_level": "Mid Level (3-5 years estimated)",
        "important_keywords": ["Python", "FastAPI", "Microservices", "Backend"]
    }

    results = resume_matcher.match(resume_payload, job_payload)

    assert results["overall_match_score"] > 50.0
    assert "Python" in results["matching_skills"]
    assert "FastAPI" in results["matching_skills"]
    assert "Kubernetes" in results["missing_skills_raw"]
    assert "AWS" in results["missing_skills_raw"]
    assert len(results["match_explanation"]) > 20
