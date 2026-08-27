import re
import numpy as np
from typing import Dict, List, Any, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ResumeJobMatcher:
    """
    NLP & Machine Learning Resume-to-Job Matching Engine.
    Combines TF-IDF vectorization, Cosine Similarity, Skill Entity Overlaps,
    Education Alignment, and Experience Level calibration.
    """

    STOPWORDS = set([
        "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are",
        "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both",
        "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't",
        "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't",
        "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
        "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll",
        "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's",
        "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on",
        "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own",
        "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some",
        "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then",
        "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this",
        "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we",
        "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's",
        "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with",
        "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your",
        "yours", "yourself", "yourselves"
    ])

    def preprocess_text(self, text: str) -> str:
        """Cleans, normalizes, removes punctuation, and filters stopwords."""
        # Convert to lower
        text = text.lower()
        # Replace non-alphanumeric (except standard programming marks like c++, c#) with space
        text = re.sub(r'[^\w\s+#.]', ' ', text)
        # Tokenize
        tokens = text.split()
        # Filter stopwords and 1-char tokens (unless C or R)
        filtered = [t for t in tokens if t not in self.STOPWORDS and (len(t) > 1 or t in ['c', 'r'])]
        return " ".join(filtered)

    def compute_tfidf_cosine_similarity(self, resume_text: str, jd_text: str) -> float:
        """Calculates TF-IDF Cosine Similarity score between 0.0 and 100.0."""
        clean_resume = self.preprocess_text(resume_text)
        clean_jd = self.preprocess_text(jd_text)

        if not clean_resume or not clean_jd:
            return 0.0

        vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            min_df=1,
            max_features=5000,
            sublinear_tf=True
        )

        try:
            tfidf_matrix = vectorizer.fit_transform([clean_resume, clean_jd])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            # Scale to 0-100 and round
            return float(np.clip(similarity * 100.0, 0.0, 100.0))
        except Exception:
            return 50.0

    def calculate_skill_match(self, resume_skills: List[str], job_skills: List[str]) -> Tuple[float, List[str], List[str]]:
        """Calculates exact skill coverage percentage."""
        if not job_skills:
            return 100.0, resume_skills, []

        resume_skills_set = {s.lower().strip() for s in resume_skills}
        matching = []
        missing = []

        for skill in job_skills:
            if skill.lower().strip() in resume_skills_set:
                matching.append(skill)
            else:
                missing.append(skill)

        match_pct = (len(matching) / len(job_skills)) * 100.0
        return round(match_pct, 1), matching, missing

    def calculate_keyword_match(self, resume_text: str, keywords: List[str]) -> float:
        """Calculates keyword presence in resume text."""
        if not keywords:
            return 100.0

        resume_lower = resume_text.lower()
        matched = 0
        for kw in keywords:
            if kw.lower() in resume_lower:
                matched += 1

        return round((matched / len(keywords)) * 100.0, 1)

    def calculate_education_match(self, resume_education: List[Dict[str, Any]], jd_education: List[str]) -> float:
        """Calculates degree alignment score."""
        if not jd_education:
            return 100.0
        if not resume_education:
            return 40.0  # Basic penalty if missing explicit education

        resume_edu_text = " ".join([
            str(e.get("degree", "")) + " " + str(e.get("field_of_study", ""))
            for e in resume_education
        ]).lower()

        matches = sum(1 for req in jd_education if req.lower() in resume_edu_text)
        return min(100.0, round((matches / max(len(jd_education), 1)) * 100.0 + 30.0, 1))

    def calculate_experience_match(self, resume_experiences: List[Dict[str, Any]], exp_level: str) -> float:
        """Estimates experience alignment."""
        exp_count = len(resume_experiences)
        if "Senior" in exp_level:
            if exp_count >= 3:
                return 95.0
            elif exp_count >= 2:
                return 80.0
            else:
                return 60.0
        elif "Mid" in exp_level:
            if exp_count >= 2:
                return 95.0
            elif exp_count >= 1:
                return 85.0
            else:
                return 70.0
        elif "Entry" in exp_level:
            return 95.0 if exp_count >= 1 else 85.0

        return 85.0

    def generate_explanation(
        self,
        overall: float,
        skill_pct: float,
        tfidf_sim: float,
        matching_count: int,
        missing_count: int,
        total_job_skills: int
    ) -> str:
        """Constructs a comprehensive narrative explaining how scores were derived."""
        verdict = "Excellent Fit" if overall >= 80 else "Strong Contender" if overall >= 65 else "Moderate Alignment" if overall >= 45 else "Skill Gap Identified"
        
        explanation = (
            f"Candidate Match Assessment: {verdict} ({overall}% Overall Score).\n\n"
            f"• Skill Overlap: {skill_pct}% ({matching_count} out of {total_job_skills} required technologies matched).\n"
            f"• NLP Semantic Alignment: {tfidf_sim:.1f}% TF-IDF Cosine Similarity between resume narrative and job requirements.\n"
            f"• Composite Formula: (40% Skill Overlap) + (30% TF-IDF Cosine Similarity) + (15% Experience Calibration) + (15% Education Alignment).\n"
        )
        if missing_count > 0:
            explanation += f"• Critical Focus: Candidate should address {missing_count} missing technical competencies to maximize interview chances."
        else:
            explanation += "• Candidate showcases complete coverage of all core technical skills specified in the job posting."

        return explanation

    def match(
        self,
        resume_data: Dict[str, Any],
        job_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Runs the entire multi-dimensional matching pipeline."""
        resume_text = resume_data.get("raw_text", "")
        jd_text = job_data.get("raw_text", "")
        resume_skills = resume_data.get("skills", [])
        job_skills = job_data.get("all_skills", [])
        keywords = job_data.get("important_keywords", [])

        # 1. Cosine similarity
        cosine_score = self.compute_tfidf_cosine_similarity(resume_text, jd_text)

        # 2. Skill match
        skill_score, matching_skills, missing_skills = self.calculate_skill_match(resume_skills, job_skills)

        # 3. Keyword match
        keyword_score = self.calculate_keyword_match(resume_text, keywords)

        # 4. Education match
        education_score = self.calculate_education_match(
            resume_data.get("education", []),
            job_data.get("education_requirements", [])
        )

        # 5. Experience match
        experience_score = self.calculate_experience_match(
            resume_data.get("experience", []),
            job_data.get("experience_level", "")
        )

        # 6. Overall Weighted Score
        overall_score = (
            0.40 * skill_score +
            0.30 * cosine_score +
            0.15 * experience_score +
            0.15 * education_score
        )
        overall_score = round(float(np.clip(overall_score, 0.0, 100.0)), 1)

        # 7. Explanation
        explanation = self.generate_explanation(
            overall=overall_score,
            skill_pct=skill_score,
            tfidf_sim=cosine_score,
            matching_count=len(matching_skills),
            missing_count=len(missing_skills),
            total_job_skills=len(job_skills)
        )

        return {
            "overall_match_score": overall_score,
            "skill_match_score": skill_score,
            "keyword_match_score": keyword_score,
            "education_match_score": education_score,
            "experience_match_score": experience_score,
            "cosine_similarity_score": cosine_score,
            "matching_skills": matching_skills,
            "missing_skills_raw": missing_skills,
            "match_explanation": explanation
        }

resume_matcher = ResumeJobMatcher()
