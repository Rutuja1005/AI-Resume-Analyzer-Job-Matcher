import re
from typing import Dict, List, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from app.ml.skill_ontology import CANONICAL_SKILL_MAP, SKILL_TO_CATEGORY, get_canonical_skill

class JobDescriptionAnalyzer:
    """
    Analyzes Job Descriptions to extract required/preferred skills,
    experience constraints, education expectations, and prominent keywords.
    """

    EXPERIENCE_PATTERNS = [
        r"(?i)(\d+\+?\s*(?:to|-)\s*\d+|\d+\+?)\s*(?:years?|yrs?)\s*(?:of)?\s*(?:relevant|hands-on|industry|software)?\s*experience",
        r"(?i)minimum\s*(?:of)?\s*(\d+)\s*(?:years?|yrs?)",
        r"(?i)(\d+)\s*(?:years?|yrs?)\s*(?:of)?\s*experience"
    ]

    EDUCATION_KEYWORDS = [
        "Bachelor's", "Master's", "PhD", "B.S.", "M.S.", "B.Tech", "M.Tech",
        "Computer Science", "Software Engineering", "Information Technology",
        "STEM", "Electrical Engineering", "Mathematics", "Statistics"
    ]

    # Stopwords list for keyword ranking
    CUSTOM_STOPWORDS = {
        "and", "the", "to", "of", "a", "in", "for", "is", "on", "that", "by", "this", "with",
        "i", "you", "it", "not", "or", "be", "are", "from", "at", "as", "your", "all", "have",
        "new", "more", "an", "was", "we", "will", "home", "can", "us", "about", "if", "page",
        "my", "has", "search", "free", "but", "our", "one", "other", "do", "no", "information",
        "time", "they", "site", "he", "up", "may", "what", "which", "their", "news", "out",
        "use", "any", "there", "see", "only", "so", "his", "when", "contact", "here", "business",
        "who", "web", "also", "now", "help", "get", "pm", "view", "online", "c", "e", "first",
        "am", "been", "would", "how", "were", "me", "s", "services", "some", "these", "click",
        "like", "service", "than", "find", "price", "date", "back", "top", "people", "had",
        "list", "name", "just", "over", "state", "year", "day", "into", "email", "two", "health",
        "world", "re", "next", "used", "go", "work", "last", "most", "products", "music", "buy",
        "data", "make", "them", "should", "product", "system", "post", "her", "city", "t", "add",
        "policy", "number", "such", "please", "available", "copyright", "support", "message", "after",
        "best", "software", "then", "jan", "good", "video", "well", "where", "info", "rights",
        "public", "books", "high", "school", "through", "m", "each", "links", "she", "review",
        "years", "order", "very", "privacy", "book", "items", "company", "r", "read", "group",
        "need", "many", "user", "said", "de", "does", "set", "under", "general", "research",
        "university", "january", "mail", "full", "map", "reviews", "program", "life", "know",
        "games", "way", "days", "management", "p", "part", "could", "great", "united", "hotel",
        "real", "item", "international", "center", "must", "skills", "experience", "candidate",
        "role", "team", "working", "requirements", "responsibilities", "job", "position", "ability",
        "strong", "plus", "preferred", "required", "opportunity", "environment", "build", "looking"
    }

    def extract_skills(self, text: str) -> Dict[str, Any]:
        """Identifies skills from JD text, distinguishing required from preferred sections."""
        text_lower = text.lower()
        extracted_skills = set()

        sorted_keys = sorted(CANONICAL_SKILL_MAP.keys(), key=lambda x: len(x), reverse=True)

        for skill_key in sorted_keys:
            pattern = r'(?<![a-zA-Z0-9])' + re.escape(skill_key) + r'(?![a-zA-Z0-9])'
            if re.search(pattern, text_lower):
                canonical = CANONICAL_SKILL_MAP[skill_key]
                extracted_skills.add(canonical)

        # Separate into required vs preferred based on surrounding context
        required_skills = []
        preferred_skills = []

        preferred_section_match = re.search(r'(?i)(?:preferred|nice\s+to\s+have|bonus|plus|desired|optional)[\s\S]*', text)
        preferred_text = preferred_section_match.group(0).lower() if preferred_section_match else ""

        for skill in extracted_skills:
            if preferred_text and skill.lower() in preferred_text and skill.lower() not in text_lower[:len(text_lower)-len(preferred_text)]:
                preferred_skills.append(skill)
            else:
                required_skills.append(skill)

        # Categorize
        by_category: Dict[str, List[str]] = {}
        for skill in extracted_skills:
            cat = SKILL_TO_CATEGORY.get(skill.lower(), "Technical Skills")
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(skill)

        return {
            "all_skills": sorted(list(extracted_skills)),
            "required_skills": sorted(required_skills),
            "preferred_skills": sorted(preferred_skills),
            "by_category": by_category
        }

    def extract_experience_level(self, text: str) -> str:
        """Extracts required experience years or seniority level."""
        for pattern in self.EXPERIENCE_PATTERNS:
            match = re.search(pattern, text)
            if match:
                return f"{match.group(1)} years of experience"

        if re.search(r"(?i)\b(senior|lead|principal|staff|architect)\b", text):
            return "Senior Level (5+ years estimated)"
        elif re.search(r"(?i)\b(mid-level|intermediate|3-5 years)\b", text):
            return "Mid Level (3-5 years estimated)"
        elif re.search(r"(?i)\b(junior|entry-level|associate|fresh|graduate|intern)\b", text):
            return "Entry / Junior Level (0-2 years estimated)"

        return "Not explicitly specified (General Level)"

    def extract_education_requirements(self, text: str) -> List[str]:
        """Finds education credentials referenced in JD."""
        found = []
        for kw in self.EDUCATION_KEYWORDS:
            if re.search(r'(?i)\b' + re.escape(kw) + r'\b', text):
                found.append(kw)
        return list(set(found))

    def extract_important_keywords(self, text: str, top_n: int = 15) -> List[str]:
        """Uses TF-IDF uni-gram and bi-gram term frequency to extract top distinct keywords."""
        if not text.strip():
            return []

        try:
            vectorizer = TfidfVectorizer(
                stop_words=list(self.CUSTOM_STOPWORDS),
                ngram_range=(1, 2),
                max_features=100
            )
            tfidf_matrix = vectorizer.fit_transform([text])
            feature_names = vectorizer.get_feature_names_out()
            scores = tfidf_matrix.toarray()[0]

            scored_words = sorted(zip(feature_names, scores), key=lambda x: x[1], reverse=True)
            # Filter out numbers and very short strings
            keywords = [
                w.title() for w, s in scored_words
                if len(w) > 2 and not re.match(r'^\d+$', w)
            ]
            return keywords[:top_n]
        except Exception:
            # Fallback simple frequency count
            words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
            filtered = [w for w in words if w not in self.CUSTOM_STOPWORDS]
            counts = {}
            for w in filtered:
                counts[w] = counts.get(w, 0) + 1
            top = sorted(counts.items(), key=lambda x: x[1], reverse=True)
            return [w[0].title() for w in top[:top_n]]

    def analyze(self, text: str, title: Optional[str] = None, company: Optional[str] = None) -> Dict[str, Any]:
        """Comprehensive Job Description Analysis."""
        skills_info = self.extract_skills(text)
        exp_level = self.extract_experience_level(text)
        edu_reqs = self.extract_education_requirements(text)
        keywords = self.extract_important_keywords(text)

        # Infer title if not supplied
        inferred_title = title or "Software Engineer"
        if not title:
            lines = [l.strip() for l in text.split("\n") if l.strip()]
            if lines and len(lines[0].split()) <= 6:
                inferred_title = lines[0].title()

        return {
            "title": inferred_title,
            "company": company or "Target Organization",
            "required_skills": skills_info["required_skills"],
            "preferred_skills": skills_info["preferred_skills"],
            "all_skills": skills_info["all_skills"],
            "skills_by_category": skills_info["by_category"],
            "experience_level": exp_level,
            "education_requirements": edu_reqs,
            "important_keywords": keywords,
            "raw_text": text
        }

jd_analyzer = JobDescriptionAnalyzer()
