import re

from rapidfuzz import fuzz

from config import SKILL_SYNONYMS


def normalize_text(text):
    """
    Lowercase + remove punctuation + collapse spaces.
    """

    if text is None:
        return ""

    text = str(text).lower()

    text = text.replace("&", " and ")

    text = re.sub(r"[^a-z0-9+#./ ]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def normalize_skill(skill):
    """
    Normalize a skill name.
    """

    skill = normalize_text(skill)

    if skill in SKILL_SYNONYMS:
        return SKILL_SYNONYMS[skill]

    return skill


def normalize_skill_list(skills):

    result = []

    for skill in skills:

        if isinstance(skill, dict):
            result.append(
                normalize_skill(
                    skill["name"]
                )
            )

        else:
            result.append(
                normalize_skill(skill)
            )

    return sorted(set(result))

def tokenize(text):
    """
    Convert text into unique tokens.
    """

    text = normalize_text(text)

    return set(text.split())


def fuzzy_match(a, b, threshold=85):
    """
    Returns True if two strings are similar.
    """

    a = normalize_text(a)
    b = normalize_text(b)

    return fuzz.token_sort_ratio(a, b) >= threshold


def contains_phrase(text, phrase):
    """
    Check whether phrase exists in text.
    """

    text = normalize_text(text)

    phrase = normalize_text(phrase)

    return phrase in text


def count_keyword_matches(text, keywords):
    """
    Count how many keywords appear.
    """

    text = normalize_text(text)

    count = 0

    for keyword in keywords:

        if contains_phrase(text, keyword):
            count += 1

    return count


def skill_overlap(candidate_skills, jd_skills):
    """
    Exact overlap after normalization.
    """

    candidate = set(
        normalize_skill_list(candidate_skills)
    )

    jd = set(
        normalize_skill_list(jd_skills)
    )

    return candidate.intersection(jd)


def skill_match_score(candidate_skills, jd_skills):
    """
    Returns score between 0 and 1.
    """

    if len(jd_skills) == 0:
        return 0.0

    overlap = skill_overlap(
        candidate_skills,
        jd_skills,
    )

    return len(overlap) / len(jd_skills)


def fuzzy_skill_overlap(candidate_skills, jd_skills):
    """
    Finds fuzzy matches.
    """

    matched = set()

    candidate = normalize_skill_list(candidate_skills)

    jd = normalize_skill_list(jd_skills)

    for c in candidate:

        for j in jd:

            if fuzzy_match(c, j):

                matched.add(j)

    return matched


def text_similarity(a, b):
    """
    Simple fuzzy similarity score (0-100).
    """

    return fuzz.token_set_ratio(
        normalize_text(a),
        normalize_text(b),
    )


def combine_text_fields(candidate):
    """
    Build one searchable text blob.
    """

    fields = [

        candidate.get("headline", ""),

        candidate.get("summary", ""),

        candidate.get("current_title", ""),

        candidate.get("current_company", ""),

        candidate.get("current_industry", ""),

    ]

    for job in candidate.get("career_history", []):

        fields.append(job.get("title", ""))

        fields.append(job.get("description", ""))

        fields.append(job.get("company", ""))

    for edu in candidate.get("education", []):

        fields.append(edu.get("degree", ""))

        fields.append(edu.get("field", ""))

    for skill in candidate.get("skills", []):
        if isinstance(skill, dict):
            fields.append(skill.get("name", ""))
        else:
            fields.append(skill)

    fields.extend(candidate.get("certifications", []))

    return normalize_text(" ".join(fields))