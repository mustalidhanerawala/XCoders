import orjson
from pathlib import Path

from config import (
    CANDIDATE_FILE,
    JOB_DESCRIPTION_FILE,
)


class CandidateParser:
    """
    Reads and parses candidates.jsonl efficiently.
    """

    def __init__(self, candidate_file=CANDIDATE_FILE):
        self.candidate_file = Path(candidate_file)

    def load_candidates(self):
        """
        Generator that yields one candidate at a time.
        Uses almost no RAM.
        """

        with self.candidate_file.open("rb") as f:

            for line in f:

                line = line.strip()

                if not line:
                    continue

                yield orjson.loads(line)

    def total_candidates(self):
        """
        Counts total candidates.
        """

        with self.candidate_file.open("rb") as f:
            return sum(1 for _ in f)


class JDParser:
    """
    Reads the job description.
    """

    def __init__(self, jd_file=JOB_DESCRIPTION_FILE):
        self.jd_file = Path(jd_file)

    def load(self):

        with self.jd_file.open(
            "r",
            encoding="utf-8"
        ) as f:

            return f.read()


def normalize_text(text):
    """
    Basic text normalization.
    """

    if text is None:
        return ""

    return (
        str(text)
        .lower()
        .replace("\n", " ")
        .replace("\t", " ")
        .strip()
    )


def extract_candidate(candidate):
    """
    Converts raw JSON into a normalized dictionary.
    """

    profile = candidate.get("profile", {})
    redrob = candidate.get("redrob_signals", {})
    skills = []
    for skill in candidate.get("skills", []):
        skills.append({

        "name": normalize_text(
            skill.get("name")
        ),

        "proficiency": normalize_text(
            skill.get("proficiency")
        ),

        "duration_months": skill.get(
            "duration_months",
            0,
        ),

        "endorsements": skill.get(
            "endorsements",
            0,
        ),
    })
    certifications = [
        normalize_text(cert.get("name", cert))
        for cert in candidate.get("certifications", [])
    ]

    career = []

    for job in candidate.get("career_history", []):

        career.append({
            "company": normalize_text(job.get("company")),
            "title": normalize_text(job.get("title")),
            "description": normalize_text(job.get("description")),
            "industry": normalize_text(job.get("industry")),
            "duration_months": job.get("duration_months", 0),
            "is_current": job.get("is_current", False),
            "start_date": job.get("start_date"),
            "end_date": job.get("end_date"),
        })

    education = []

    for edu in candidate.get("education", []):

        education.append({

            "degree": normalize_text(edu.get("degree")),

            "field": normalize_text(
                edu.get("field_of_study")
            ),

            "tier": normalize_text(
                edu.get("tier")
            ),
        })

    combined_text = " ".join([

    profile.get("headline", ""),

    profile.get("summary", ""),

    profile.get("current_title", ""),

    profile.get("current_company", ""),

    profile.get("current_industry", ""),

    " ".join(
        skill["name"]
        for skill in skills
    ),

    " ".join(
        job["description"]
        for job in career
    ),

    " ".join(
        job["title"]
        for job in career
    ),

    " ".join(
        cert
        for cert in certifications
    )

]).lower()
    return {

        "candidate_id": candidate.get("candidate_id"),

        "headline": normalize_text(
            profile.get("headline")
        ),

        "summary": normalize_text(
            profile.get("summary")
        ),

        "location": normalize_text(
            profile.get("location")
        ),

        "country": normalize_text(
            profile.get("country")
        ),

        "years_of_experience": profile.get(
            "years_of_experience",
            0,
        ),

        "current_title": normalize_text(
            profile.get("current_title")
        ),

        "current_company": normalize_text(
            profile.get("current_company")
        ),

        "current_industry": normalize_text(
            profile.get("current_industry")
        ),

        "skills": skills,

        "career_history": career,

        "education": education,

        "certifications": certifications,
        "combined_text": combined_text,

        "redrob_signals": redrob,
    }


def parse_job_description():

    jd = JDParser()

    return normalize_text(jd.load())