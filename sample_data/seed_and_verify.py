import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from fastapi.testclient import TestClient
from app.main import app
from app.database.connection import Base, engine

# Ensure tables exist
Base.metadata.create_all(bind=engine)

client = TestClient(app)

print("=" * 60)
print("RUNNING END-TO-END SYSTEM SEEDING & VERIFICATION")
print("=" * 60)

# 1. Healthcheck
res_health = client.get("/api/health")
assert res_health.status_code == 200
print("[OK] Healthcheck passed:", res_health.json())

# 2. Register Candidate
user_payload = {
    "email": "demo.candidate@resumematcher.ai",
    "password": "DemoPassword123!",
    "full_name": "Alex Morgan"
}
res_auth = client.post("/api/auth/register", json=user_payload)
if res_auth.status_code == 400: # Already exists, login instead
    res_auth = client.post("/api/auth/login", json={"email": user_payload["email"], "password": user_payload["password"]})

assert res_auth.status_code in [200, 201]
token = res_auth.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print("[OK] Authenticated candidate user with JWT token.")

# 3. Upload Sample PDF Resume
pdf_path = "sample_data/sample_resume_senior_fullstack.pdf"
with open(pdf_path, "rb") as f:
    files = {"file": ("sample_resume_senior_fullstack.pdf", f, "application/pdf")}
    res_upload = client.post("/api/resumes/upload", files=files, headers=headers)

assert res_upload.status_code == 201, res_upload.text
resume_data = res_upload.json()
resume_id = resume_data["id"]
print(f"[OK] Uploaded & Parsed PDF: {resume_data['filename']}")
print(f"  - Extracted Name: {resume_data['candidate_name']}")
print(f"  - Extracted Skills ({len(resume_data['skills'])}): {resume_data['skills'][:6]}...")

# 4. Ingest Job Description
with open("sample_data/sample_jd_fullstack_react_dev.txt", "r", encoding="utf-8") as f:
    jd_text = f.read()

job_payload = {
    "title": "Senior Full-Stack Engineer",
    "company": "StripeTech Innovations",
    "job_description_text": jd_text
}
res_job = client.post("/api/jobs/analyze", json=job_payload, headers=headers)
assert res_job.status_code == 201, res_job.text
job_data = res_job.json()
job_id = job_data["id"]
print(f"[OK] Analyzed Job Description: {job_data['title']} at {job_data['company']}")
print(f"  - Required Skills: {job_data['required_skills']}")

# 5. Run Match Analysis
match_payload = {
    "resume_id": resume_id,
    "job_description_id": job_id
}
res_match = client.post("/api/analysis/match", json=match_payload, headers=headers)
assert res_match.status_code == 201, res_match.text
match_res = res_match.json()
print(f"[OK] ML Match Analysis Complete:")
print(f"  - Overall Match Score: {match_res['overall_match_score']}%")
print(f"  - Skill Match Score:   {match_res['skill_match_score']}%")
print(f"  - ATS Compliance:      {match_res['ats_score']}%")
print(f"  - Matching Skills:     {len(match_res['matching_skills'])} items")
print(f"  - Missing Skills Gap:  {len(match_res['missing_skills'])} items")

# 6. Check Dashboard Analytics
res_dash = client.get("/api/analytics/dashboard", headers=headers)
assert res_dash.status_code == 200
dash = res_dash.json()
print("[OK] Dashboard Analytics aggregated successfully:")
print(f"  - Total Resumes: {dash['total_resumes']}, Total Analyses: {dash['total_analyses']}")
print(f"  - Avg Match: {dash['avg_match_score']}%, Avg ATS: {dash['avg_ats_score']}%")

# 7. Check JSON Report Export
analysis_id = match_res["analysis_id"]
res_exp = client.get(f"/api/analysis/{analysis_id}/export", headers=headers)
assert res_exp.status_code == 200
assert len(res_exp.text) > 100
print(f"[OK] Exported report JSON verified ({len(res_exp.text)} bytes).")

print("=" * 60)
print("ALL SYSTEM VERIFICATIONS PASSED SUCCESSFULLY (100% READY)")
print("=" * 60)
