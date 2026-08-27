import pytest
from app.ml.resume_parser import resume_parser
from app.ml.jd_analyzer import jd_analyzer
from app.ml.skill_ontology import get_canonical_skill

def test_entity_extraction_from_text():
    sample_text = """
    Alex Morgan
    Email: alex.morgan@techcorp.io
    Phone: (555) 234-5678
    LinkedIn: linkedin.com/in/alexmorgan-dev
    
    Professional Summary
    Experienced Full Stack Engineer with 6+ years of experience designing high-throughput distributed systems.
    
    Technical Skills
    Languages: Python, JavaScript, TypeScript, SQL, Go
    Frameworks: React, FastAPI, Django, Next.js, Node.js
    Cloud & DB: Docker, Kubernetes, AWS, PostgreSQL, Redis, MongoDB
    Tools: Git, CI/CD, PyTest, Tailwind CSS
    
    Work Experience
    Senior Software Engineer | CloudScale Inc (2021 - Present)
    • Architected RESTful microservices with FastAPI and PostgreSQL handling 5,000+ RPS.
    • Improved database query response times by 45% using Redis caching and index optimization.
    • Spearheaded migration of frontend systems to React and Next.js, boosting SEO performance by 35%.
    
    Education
    Bachelor of Science in Computer Science | Stanford University (2017 - 2021)
    """

    email = resume_parser.extract_email(sample_text)
    assert email == "alex.morgan@techcorp.io"

    phone = resume_parser.extract_phone(sample_text)
    assert "555" in phone and "5678" in phone

    name = resume_parser.extract_name(sample_text)
    assert "Alex" in name

    skills_data = resume_parser.extract_skills(sample_text)
    skills = skills_data["all_skills"]

    assert "Python" in skills
    assert "React" in skills
    assert "FastAPI" in skills
    assert "Docker" in skills
    assert "PostgreSQL" in skills

def test_jd_analyzer():
    jd_text = """
    Job Title: Senior Backend Engineer
    Company: Acme Tech
    
    Requirements:
    • 4+ years of professional experience with Python and FastAPI or Django.
    • Deep proficiency in PostgreSQL, Redis, and Docker.
    • Experience with AWS (EC2, S3, RDS) and Kubernetes.
    • Bachelor's Degree in Computer Science or related STEM field.
    
    Preferred / Nice to Have:
    • Familiarity with React and TypeScript.
    • Knowledge of Apache Kafka and Terraform.
    """

    analyzed = jd_analyzer.analyze(jd_text, title="Senior Backend Engineer", company="Acme Tech")
    assert analyzed["title"] == "Senior Backend Engineer"
    assert "Python" in analyzed["all_skills"]
    assert "FastAPI" in analyzed["all_skills"]
    assert "PostgreSQL" in analyzed["all_skills"]
    assert len(analyzed["important_keywords"]) > 0
