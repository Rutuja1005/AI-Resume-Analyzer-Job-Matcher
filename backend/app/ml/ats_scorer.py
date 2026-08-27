import re
from typing import Dict, List, Any

class ATSScorer:
    """
    Simulates Applicant Tracking System (ATS) parsing & scoring algorithms.
    Evaluates 7 distinct structural and qualitative dimensions.
    """

    ACTION_VERBS = {
        "accelerated", "accomplished", "achieved", "architected", "automated",
        "built", "championed", "collaborated", "constructed", "created",
        "decreased", "delivered", "deployed", "designed", "developed",
        "devised", "directed", "eliminated", "enabled", "engineered",
        "enhanced", "established", "executed", "expanded", "expedited",
        "formulated", "generated", "guided", "implemented", "improved",
        "increased", "initiated", "innovated", "inspected", "installed",
        "instituted", "integrated", "launched", "lead", "led", "leveraged",
        "maximized", "mentored", "migrated", "minimized", "modeled",
        "modernized", "negotiated", "orchestrated", "organized", "overhauled",
        "oversaw", "pioneered", "planned", "produced", "programmed",
        "reduced", "refactored", "resolved", "restructured", "revamped",
        "scaled", "simplified", "spearheaded", "standardized", "streamlined",
        "strengthened", "structured", "surpassed", "transformed", "upgraded"
    }

    def score_keyword_coverage(self, resume_text: str, jd_keywords: List[str]) -> Dict[str, Any]:
        """Factor 1: Keyword Coverage (Max 25 pts)"""
        max_score = 25.0
        if not jd_keywords:
            return {"score": 25.0, "max_score": max_score, "status": "passed", "feedback": "Job description contains standard keyword distributions."}

        text_lower = resume_text.lower()
        matched = sum(1 for kw in jd_keywords if kw.lower() in text_lower)
        ratio = matched / len(jd_keywords)
        score = round(ratio * max_score, 1)

        status = "passed" if ratio >= 0.7 else "warning" if ratio >= 0.4 else "failed"
        feedback = f"Matched {matched}/{len(jd_keywords)} primary keywords ({int(ratio*100)}% keyword density)."
        return {"score": score, "max_score": max_score, "status": status, "feedback": feedback}

    def score_section_completeness(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Factor 2: Standard Resume Sections (Max 20 pts)"""
        max_score = 20.0
        sections_found = 0
        total_sections = 5
        missing_sec = []

        if resume_data.get("summary") or len(resume_data.get("raw_text", "")) > 100:
            sections_found += 1
        else:
            missing_sec.append("Professional Summary")

        if resume_data.get("skills") and len(resume_data.get("skills")) > 0:
            sections_found += 1
        else:
            missing_sec.append("Skills Section")

        if resume_data.get("experience") and len(resume_data.get("experience")) > 0:
            sections_found += 1
        else:
            missing_sec.append("Work Experience")

        if resume_data.get("education") and len(resume_data.get("education")) > 0:
            sections_found += 1
        else:
            missing_sec.append("Education")

        if (resume_data.get("projects") and len(resume_data.get("projects")) > 0) or (resume_data.get("certifications") and len(resume_data.get("certifications")) > 0):
            sections_found += 1
        else:
            missing_sec.append("Projects or Certifications")

        score = round((sections_found / total_sections) * max_score, 1)
        status = "passed" if sections_found >= 4 else "warning" if sections_found >= 3 else "failed"
        feedback = "All primary ATS sections detected." if not missing_sec else f"Missing standard sections: {', '.join(missing_sec)}."

        return {"score": score, "max_score": max_score, "status": status, "feedback": feedback}

    def score_contact_information(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Factor 3: Contact Details Check (Max 15 pts)"""
        max_score = 15.0
        has_email = bool(resume_data.get("email"))
        has_phone = bool(resume_data.get("phone"))
        has_name = bool(resume_data.get("name") and resume_data.get("name") != "Candidate")

        score = 0.0
        if has_name:
            score += 5.0
        if has_email:
            score += 5.0
        if has_phone:
            score += 5.0

        status = "passed" if score >= 15.0 else "warning" if score >= 10.0 else "failed"
        feedback = "Complete contact information (Name, Email, Phone) extracted." if score >= 15 else "Incomplete contact details may cause ATS parsing rejections."
        return {"score": score, "max_score": max_score, "status": status, "feedback": feedback}

    def score_quantifiable_achievements(self, resume_text: str) -> Dict[str, Any]:
        """Factor 4: Measurable Metrics & KPIs (Max 15 pts)"""
        max_score = 15.0
        # Check for metrics: %, $, numbers with scale (k, M, B), multipliers (2x, 5x)
        metric_patterns = [
            r'\b\d+%\b',
            r'\$\s*\d+(?:,\d+)*(?:\.\d+)?(?:\s*(?:k|m|million|billion))?\b',
            r'\b\d+x\b',
            r'\b(?:reduced|increased|improved|optimized|boosted|saved)\s+by\s+\d+',
            r'\b\d+\s*(?:ms|sec|seconds|minutes|users|requests|tps|qps|stars|downloads)\b'
        ]

        found_metrics = 0
        for pattern in metric_patterns:
            matches = re.findall(pattern, resume_text, re.IGNORECASE)
            found_metrics += len(matches)

        if found_metrics >= 5:
            score = 15.0
            status = "passed"
            feedback = f"Outstanding quantification: {found_metrics} high-impact metric markers found."
        elif found_metrics >= 2:
            score = 10.0
            status = "warning"
            feedback = f"Moderate quantification: {found_metrics} metrics found. Add more % improvements or dollar amounts."
        else:
            score = 5.0
            status = "failed"
            feedback = "Weak metric presence. Bullet points should contain quantifiable results (e.g. 'boosted throughput by 35%')."

        return {"score": score, "max_score": max_score, "status": status, "feedback": feedback}

    def score_formatting_and_length(self, resume_text: str) -> Dict[str, Any]:
        """Factor 5: Word Count & Text Format Health (Max 15 pts)"""
        max_score = 15.0
        words = resume_text.split()
        word_count = len(words)

        if 350 <= word_count <= 1100:
            score = 15.0
            status = "passed"
            feedback = f"Optimal resume length ({word_count} words). Fits standard 1-2 page guideline."
        elif 200 <= word_count < 350:
            score = 10.0
            status = "warning"
            feedback = f"Resume is slightly short ({word_count} words). Expand on accomplishments."
        elif 1100 < word_count <= 1800:
            score = 10.0
            status = "warning"
            feedback = f"Resume is long ({word_count} words). Condense bullet points for concise readability."
        else:
            score = 5.0
            status = "failed"
            feedback = f"Resume length outside recommended ATS range ({word_count} words)."

        return {"score": score, "max_score": max_score, "status": status, "feedback": feedback}

    def score_action_verbs(self, resume_text: str) -> Dict[str, Any]:
        """Factor 6: Strong Action Verbs Density (Max 10 pts)"""
        max_score = 10.0
        words = [w.lower().strip(".,;:()[]") for w in resume_text.split()]
        matched_verbs = set(words).intersection(self.ACTION_VERBS)
        verb_count = len(matched_verbs)

        if verb_count >= 8:
            score = 10.0
            status = "passed"
            feedback = f"Strong leadership and action orientation ({verb_count} distinct action verbs)."
        elif verb_count >= 4:
            score = 7.0
            status = "warning"
            feedback = f"Moderate action verbs ({verb_count} distinct verbs). Replace passive voice with active verbs."
        else:
            score = 3.0
            status = "failed"
            feedback = "Low action verb density. Start bullet points with dynamic verbs like 'Architected', 'Streamlined', 'Pioneered'."

        return {"score": score, "max_score": max_score, "status": status, "feedback": feedback}

    def score_skill_relevance(self, matching_skills_count: int, total_job_skills: int) -> Dict[str, Any]:
        """Factor 7: Role Skill Relevance (Normalized check)"""
        if total_job_skills == 0:
            return {"score": 10.0, "max_score": 10.0, "status": "passed", "feedback": "Skill profile matches job requirements."}

        ratio = matching_skills_count / total_job_skills
        score = round(ratio * 10.0, 1)
        status = "passed" if ratio >= 0.6 else "warning" if ratio >= 0.3 else "failed"
        feedback = f"Relevant skill coverage: {matching_skills_count} matching technologies."
        return {"score": score, "max_score": 10.0, "status": status, "feedback": feedback}

    def evaluate(
        self,
        resume_data: Dict[str, Any],
        job_data: Dict[str, Any],
        matching_skills_count: int
    ) -> Dict[str, Any]:
        """Runs the 7-dimension ATS audit and synthesizes actionable recommendations."""
        resume_text = resume_data.get("raw_text", "")
        keywords = job_data.get("important_keywords", [])
        total_job_skills = len(job_data.get("all_skills", []))

        kw_score = self.score_keyword_coverage(resume_text, keywords)
        sec_score = self.score_section_completeness(resume_data)
        contact_score = self.score_contact_information(resume_data)
        metrics_score = self.score_quantifiable_achievements(resume_text)
        format_score = self.score_formatting_and_length(resume_text)
        verbs_score = self.score_action_verbs(resume_text)
        relevance_score = self.score_skill_relevance(matching_skills_count, total_job_skills)

        # Sum of 25 + 20 + 15 + 15 + 15 + 10 = 100
        total_ats = round(
            kw_score["score"] +
            sec_score["score"] +
            contact_score["score"] +
            metrics_score["score"] +
            format_score["score"] +
            verbs_score["score"],
            1
        )
        total_ats = min(100.0, max(0.0, total_ats))

        # Strengths & Critical Improvements
        strengths = []
        improvements = []

        for name, item in [
            ("Keyword Coverage", kw_score),
            ("Resume Structure", sec_score),
            ("Contact Details", contact_score),
            ("Measurable Impact", metrics_score),
            ("Format & Length", format_score),
            ("Action Verbs", verbs_score)
        ]:
            if item["status"] == "passed":
                strengths.append(f"{name}: {item['feedback']}")
            elif item["status"] in ["warning", "failed"]:
                improvements.append(f"{name}: {item['feedback']}")

        return {
            "total_ats_score": total_ats,
            "keyword_coverage": kw_score,
            "section_completeness": sec_score,
            "contact_information": contact_score,
            "quantifiable_achievements": metrics_score,
            "formatting_and_length": format_score,
            "action_verbs_density": verbs_score,
            "skill_relevance": relevance_score,
            "strengths": strengths,
            "critical_improvements": improvements
        }

ats_scorer = ATSScorer()
