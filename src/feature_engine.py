from text_utils import (
    combine_text_fields,
    count_keyword_matches,
    skill_match_score,
    text_similarity,
)


class FeatureEngine:

    def __init__(self, jd):
        self.jd = jd

    # =====================================================
    # STAGE 1
    # Fast features (100k candidates)
    # =====================================================

    def fast_extract(self, candidate):

        skills = [s["name"] for s in candidate["skills"]]

        years = candidate["years_of_experience"]

        title = candidate["current_title"].lower()

        required_overlap = len(
            set(skills) &
            set(self.jd["required_skills"])
        )

        preferred_overlap = len(
            set(skills) &
            set(self.jd["preferred_skills"])
        )

        title_bonus = 0

        for t in self.jd["desired_titles"]:

            if t in title:

                title_bonus = 1

                break

        rr = candidate["redrob_signals"]

        behaviour = (
            rr.get("profile_completeness_score", 0)
            + rr.get("github_activity_score", 0)
        ) / 200

        return {

            "required_overlap": required_overlap,

            "preferred_overlap": preferred_overlap,

            "years": years,

            "title_bonus": title_bonus,

            "behaviour": behaviour,

        }

    # =====================================================
    # STAGE 2
    # Expensive features (Top 500 only)
    # =====================================================

    def full_extract(self, candidate):

        text = combine_text_fields(candidate)

        skills = [s["name"] for s in candidate["skills"]]

        f = {}

        f["required_skill_score"] = skill_match_score(
            skills,
            self.jd["required_skills"],
        )

        f["preferred_skill_score"] = skill_match_score(
            skills,
            self.jd["preferred_skills"],
        )

        exp = self.jd["experience"]

        years = candidate["years_of_experience"]

        if years < exp["min"]:

            experience = years / max(exp["min"], 1)

        elif years <= exp["max"]:

            experience = 1

        else:

            experience = max(
                0.5,
                1 - (years - exp["max"]) * 0.05,
            )

        f["experience_score"] = experience

        title_score = 0

        for t in self.jd["desired_titles"]:

            title_score = max(

                title_score,

                text_similarity(
                    candidate["current_title"],
                    t,
                )

            )

        f["title_score"] = title_score / 100

        f["required_keyword_hits"] = count_keyword_matches(
            text,
            self.jd["required_skills"],
        )

        f["preferred_keyword_hits"] = count_keyword_matches(
            text,
            self.jd["preferred_skills"],
        )

        f["negative_keyword_hits"] = count_keyword_matches(
            text,
            self.jd["negative_keywords"],
        )

        career = " ".join(

            job["company"]

            for job in candidate["career_history"]

        ).lower()

        f["product_company"] = int(

            any(

                x in career

                for x in [

                    "google",

                    "meta",

                    "amazon",

                    "microsoft",

                    "uber",

                    "atlassian",

                    "swiggy",

                    "zomato",

                    "flipkart",

                    "phonepe",

                ]

            )

        )

        f["service_company"] = int(

            any(

                x in career

                for x in [

                    "tcs",

                    "infosys",

                    "accenture",

                    "wipro",

                    "capgemini",

                    "cognizant",

                    "mindtree",

                ]

            )

        )

        rr = candidate["redrob_signals"]

        f["open_to_work"] = int(
            rr.get("open_to_work_flag", False)
        )

        f["profile_complete"] = (
            rr.get(
                "profile_completeness_score",
                0,
            ) / 100
        )

        f["github_score"] = (
            rr.get(
                "github_activity_score",
                0,
            ) / 100
        )

        f["response_rate"] = rr.get(
            "recruiter_response_rate",
            0,
        )

        f["saved_by_recruiters"] = rr.get(
            "saved_by_recruiters_30d",
            0,
        )

        f["notice_period"] = rr.get(
            "notice_period_days",
            999,
        )

        return f