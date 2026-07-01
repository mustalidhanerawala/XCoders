from datetime import datetime

from config import (
    DATE_FORMAT,
    MAX_ADVANCED_SKILLS,
    MAX_ALLOWED_JOB_OVERLAP_MONTHS,
    MAX_SKILL_MONTH_FACTOR,
)


class HoneypotDetector:

    def detect(self, candidate):

        penalty = 0
        reasons = []

        total_years = candidate["years_of_experience"]
        total_months = total_years * 12

        # -----------------------------
        # Too many advanced skills
        # -----------------------------

        advanced = 0

        for skill in candidate.get("skills", []):

            if isinstance(skill, dict):
                prof = str(skill.get("proficiency", "")).lower()
                if prof in ("advanced", "expert"):
                    advanced += 1

        if advanced > MAX_ADVANCED_SKILLS:
            penalty += 15
            reasons.append("too_many_advanced_skills")

        # -----------------------------
        # Skill duration impossible
        # -----------------------------

        for skill in candidate.get("skills", []):

            if isinstance(skill, dict):

                months = skill.get("duration_months", 0)

                if months > total_months * MAX_SKILL_MONTH_FACTOR:
                    penalty += 20
                    reasons.append("impossible_skill_duration")
                    break

        # -----------------------------
        # Career overlap
        # -----------------------------

        jobs = []

        for job in candidate["career_history"]:

            try:

                start = datetime.strptime(
                    job["start_date"],
                    DATE_FORMAT,
                )

                end = job["end_date"]

                if end is None:
                    end = datetime.today()

                else:
                    end = datetime.strptime(
                        end,
                        DATE_FORMAT,
                    )

                jobs.append((start, end))

            except Exception:
                pass

        jobs.sort(key=lambda x: x[0])

        for i in range(1, len(jobs)):

            previous_end = jobs[i - 1][1]

            current_start = jobs[i][0]

            overlap = (
                previous_end - current_start
            ).days / 30

            if overlap > MAX_ALLOWED_JOB_OVERLAP_MONTHS:

                penalty += 20

                reasons.append("career_overlap")

                break

        # -----------------------------
        # Impossible education
        # -----------------------------

        for edu in candidate["education"]:

            end = edu.get("end_year")

            if end:

                years_after = (
                    datetime.today().year - end
                )

                if years_after > total_years + 5:

                    penalty += 10

                    reasons.append("education_timeline")

                    break

        return {

            "penalty": penalty,

            "reasons": reasons,
        }