import re
import os
from typing import Dict, List, Any, Optional
import pdfplumber
import pypdf
from app.ml.skill_ontology import CANONICAL_SKILL_MAP, SKILL_TO_CATEGORY, get_canonical_skill

class ResumeParser:
    """
    Production-grade Resume Parser.
    Extracts text, contact details, standard sections, technical skills,
    education history, and projects from PDF resumes.
    """

    # Section Headers Patterns
    SECTION_PATTERNS = {
        "summary": r"(?i)(?:summary|professional\s+summary|about\s+me|profile|objective)",
        "skills": r"(?i)(?:technical\s+skills|skills\s*&?\s*technologies|core\s+competencies|skills|technologies|expertise)",
        "experience": r"(?i)(?:work\s+experience|professional\s+experience|experience|employment\s+history|career\s+history)",
        "education": r"(?i)(?:education|academic\s+background|qualifications|academic\s+history)",
        "projects": r"(?i)(?:projects|key\s+projects|personal\s+projects|academic\s+projects)",
        "certifications": r"(?i)(?:certifications|certificates|licenses|courses\s*&?\s*certifications|achievements)"
    }

    # Regex patterns for contact data
    EMAIL_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    PHONE_REGEX = r'(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'
    INTERNATIONAL_PHONE_REGEX = r'(\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,5}[-.\s]?\d{3,5}'
    LINKEDIN_REGEX = r'(?:https?://)?(?:www\.)?linkedin\.com/in/([a-zA-Z0-9_-]+)'
    GITHUB_REGEX = r'(?:https?://)?(?:www\.)?github\.com/([a-zA-Z0-9_-]+)'

    # Degree patterns
    DEGREE_PATTERNS = [
        r"(?i)\b(?:B\.?S\.?|B\.?Sc\.?|B\.?E\.?|B\.?Tech\.?|Bachelor(?:'s)?(?:\s+of\s+[\w\s]+)?)\b",
        r"(?i)\b(?:M\.?S\.?|M\.?Sc\.?|M\.?E\.?|M\.?Tech\.?|Master(?:'s)?(?:\s+of\s+[\w\s]+)?|MBA)\b",
        r"(?i)\b(?:Ph\.?D\.?|Doctorate|Doctor\s+of\s+[\w\s]+)\b",
        r"(?i)\b(?:Associate(?:'s)?(?:\s+Degree)?|Diploma)\b"
    ]

    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extracts text preserving line breaks using pdfplumber with pypdf fallback."""
        text = ""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Resume file not found at: {file_path}")

        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text(layout=False)
                    if extracted:
                        text += extracted + "\n"
        except Exception:
            # Fallback to pypdf
            try:
                reader = pypdf.PdfReader(file_path)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
            except Exception as e:
                raise ValueError(f"Failed to read PDF document: {str(e)}")

        return text.strip()

    def extract_name(self, text: str) -> Optional[str]:
        """Heuristically extracts candidate name from header lines."""
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        if not lines:
            return None

        # Check top 5 lines for name candidate
        for line in lines[:5]:
            # Skip lines with emails, links, or section headings
            if "@" in line or "http" in line or "linkedin" in line or "github" in line:
                continue
            if re.match(r"(?i)^(resume|curriculum vitae|cv)$", line):
                continue
            
            # Words count test (typically 2-4 words, capitalized)
            words = line.split()
            if 2 <= len(words) <= 4:
                # Check if words are mostly alphabetical
                if all(re.match(r"^[A-Za-z.'-]+$", w) for w in words):
                    # Exclude phrases like "Software Engineer" or "Page 1 of 2"
                    if not re.search(r"(?i)\b(engineer|developer|manager|analyst|specialist|designer|resume|cv|summary|page)\b", line):
                        return line.title()

        # Fallback to first non-empty line
        return lines[0].title() if len(lines[0].split()) <= 4 else "Candidate"

    def extract_email(self, text: str) -> Optional[str]:
        match = re.search(self.EMAIL_REGEX, text)
        return match.group(0).lower() if match else None

    def extract_phone(self, text: str) -> Optional[str]:
        # First try international phone pattern
        match = re.search(self.INTERNATIONAL_PHONE_REGEX, text)
        if match and len(re.sub(r'\D', '', match.group(0))) >= 10:
            return match.group(0).strip()
        # Fallback
        match = re.search(self.PHONE_REGEX, text)
        return match.group(0).strip() if match else None

    def extract_skills(self, text: str) -> Dict[str, Any]:
        """Identifies skills from the entire resume text and groups by category."""
        text_lower = text.lower()
        extracted_skills = set()

        # Sort canonical map keys by length descending to match multi-word phrases first
        sorted_keys = sorted(CANONICAL_SKILL_MAP.keys(), key=lambda x: len(x), reverse=True)

        for skill_key in sorted_keys:
            # Word boundary regex matching to avoid substring collision (e.g. 'c' in 'react')
            pattern = r'(?<![a-zA-Z0-9])' + re.escape(skill_key) + r'(?![a-zA-Z0-9])'
            if re.search(pattern, text_lower):
                canonical = CANONICAL_SKILL_MAP[skill_key]
                extracted_skills.add(canonical)

        # Categorize
        by_category: Dict[str, List[str]] = {}
        for skill in extracted_skills:
            cat = SKILL_TO_CATEGORY.get(skill.lower(), "Technical Skills")
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(skill)

        # Sort category items
        for cat in by_category:
            by_category[cat].sort()

        return {
            "all_skills": sorted(list(extracted_skills)),
            "by_category": by_category
        }

    def segment_sections(self, text: str) -> Dict[str, str]:
        """Segments raw text into structured sections based on standard headers."""
        lines = text.split("\n")
        sections: Dict[str, List[str]] = {
            "header": [],
            "summary": [],
            "skills": [],
            "experience": [],
            "education": [],
            "projects": [],
            "certifications": [],
            "other": []
        }

        current_section = "header"

        for line in lines:
            trimmed = line.strip()
            if not trimmed:
                continue

            # Check if this line matches a section header
            matched_section = None
            if len(trimmed.split()) <= 4 and len(trimmed) < 40:
                for sec_name, pattern in self.SECTION_PATTERNS.items():
                    if re.match(pattern, trimmed):
                        matched_section = sec_name
                        break

            if matched_section:
                current_section = matched_section
            else:
                sections[current_section].append(line)

        # Join lines
        return {sec: "\n".join(lines).strip() for sec, lines in sections.items()}

    def extract_education(self, text: str, education_section: str = "") -> List[Dict[str, Any]]:
        """Extracts degrees, institutions, and graduation years."""
        target_text = education_section if education_section else text
        education_records = []

        # Find degree mentions
        for pattern in self.DEGREE_PATTERNS:
            matches = re.finditer(pattern, target_text)
            for m in matches:
                degree_name = m.group(0).strip()
                # Find year near the match
                start_pos = max(0, m.start() - 100)
                end_pos = min(len(target_text), m.end() + 100)
                context = target_text[start_pos:end_pos]
                
                year_match = re.search(r'\b(20\d{2}|19\d{2})\b', context)
                grad_year = year_match.group(0) if year_match else None

                # Find possible major/field
                major_match = re.search(r'(?i)(?:in|of)\s+([A-Za-z\s]{3,30})(?:,|\n|\.|$)', context)
                major = major_match.group(1).strip() if major_match else None

                education_records.append({
                    "degree": degree_name,
                    "field_of_study": major,
                    "year": grad_year,
                    "institution": None
                })

        # If no strict degree pattern was found, search for university/college keywords
        if not education_records:
            uni_matches = re.findall(r'(?i)([A-Za-z\s]+(?:University|Institute|College|Academy)[\w\s]*)', target_text)
            for uni in uni_matches[:3]:
                education_records.append({
                    "degree": "Higher Education Degree",
                    "field_of_study": None,
                    "year": None,
                    "institution": uni.strip()
                })

        return education_records

    def extract_experience(self, experience_section: str) -> List[Dict[str, Any]]:
        """Parses experience bullets, roles, companies, and date intervals."""
        if not experience_section:
            return []

        experiences = []
        blocks = re.split(r'\n{2,}', experience_section)
        
        for block in blocks:
            lines = [l.strip() for l in block.split("\n") if l.strip()]
            if not lines:
                continue
            
            # Find year ranges like '2021 - 2024' or 'Jan 2020 - Present'
            date_match = re.search(r'(?i)((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|[0-9]{2}/)?\s*(?:19|20)\d{2}\s*[-–—to]\s*(?:(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|[0-9]{2}/)?\s*(?:19|20)\d{2}|Present|Current))', block)
            date_range = date_match.group(0) if date_match else None

            title = lines[0] if lines else "Professional Role"
            bullets = [l.lstrip("•-* ").strip() for l in lines[1:] if len(l.strip()) > 10]

            experiences.append({
                "title_and_company": title,
                "duration": date_range,
                "description": "\n".join(bullets) if bullets else block
            })

        return experiences

    def parse(self, file_path: str) -> Dict[str, Any]:
        """Complete resume parsing pipeline returning structured JSON."""
        raw_text = self.extract_text_from_pdf(file_path)
        sections = self.segment_sections(raw_text)
        skills_data = self.extract_skills(raw_text)
        education_data = self.extract_education(raw_text, sections.get("education", ""))
        experience_data = self.extract_experience(sections.get("experience", ""))

        # Extract projects
        project_text = sections.get("projects", "")
        projects = []
        if project_text:
            for p in re.split(r'\n{2,}', project_text):
                if len(p.strip()) > 15:
                    p_lines = [l.strip() for l in p.split("\n") if l.strip()]
                    projects.append({
                        "name": p_lines[0] if p_lines else "Project",
                        "details": "\n".join(p_lines[1:]) if len(p_lines) > 1 else p_lines[0]
                    })

        # Extract certifications
        cert_text = sections.get("certifications", "")
        certs = []
        if cert_text:
            for c in cert_text.split("\n"):
                c_clean = c.lstrip("•-* ").strip()
                if 5 < len(c_clean) < 120:
                    certs.append({"name": c_clean})

        return {
            "name": self.extract_name(raw_text),
            "email": self.extract_email(raw_text),
            "phone": self.extract_phone(raw_text),
            "skills": skills_data["all_skills"],
            "skills_by_category": skills_data["by_category"],
            "education": education_data,
            "experience": experience_data,
            "projects": projects,
            "certifications": certs,
            "summary": sections.get("summary") or sections.get("header"),
            "raw_text": raw_text
        }

resume_parser = ResumeParser()
