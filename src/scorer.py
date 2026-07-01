from config import WEIGHTS


class CandidateScorer:

    # =====================================================
    # STAGE 1
    # Fast score (100k candidates)
    # =====================================================

    def fast_score(self, features):

        score = 0.0

        score += features["required_overlap"] * 40

        score += features["preferred_overlap"] * 15

        score += min(features["years"], 15) * 2

        score += features["title_bonus"] * 15

        score += features["behaviour"] * 10

        return score

    # =====================================================
    # STAGE 2
    # Final score (Top 500 candidates)
    # =====================================================

    def final_score(
        self,
        features,
        semantic_similarity,
        honeypot,
    ):

        score = 0.0

        # -------------------------
        # Semantic Similarity
        # -------------------------

        score += (
            semantic_similarity
            * WEIGHTS["semantic_similarity"]
        )

        # -------------------------
        # Skills
        # -------------------------

        score += (
            features["required_skill_score"]
            * WEIGHTS["required_skills"]
        )

        score += (
            features["preferred_skill_score"]
            * WEIGHTS["preferred_skills"]
        )

        # -------------------------
        # Experience
        # -------------------------

        score += (
            features["experience_score"]
            * WEIGHTS["experience"]
        )

        # -------------------------
        # Title
        # -------------------------

        score += (
            features["title_score"]
            * WEIGHTS["current_title"]
        )

        # -------------------------
        # Behaviour
        # -------------------------

        behaviour = 0

        behaviour += (
            features["open_to_work"] * 2
        )

        behaviour += (
            features["profile_complete"] * 2
        )

        behaviour += (
            features["github_score"] * 2
        )

        behaviour += (
            features["response_rate"] * 2
        )

        behaviour += min(
            features["saved_by_recruiters"] / 10,
            1,
        )

        if features["notice_period"] <= 30:
            behaviour += 1

        score += behaviour

        # -------------------------
        # Companies
        # -------------------------

        if features["product_company"]:
            score += 3

        if features["service_company"]:
            score -= 2

        # -------------------------
        # Keywords
        # -------------------------

        score += (
            features["required_keyword_hits"] * 0.5
        )

        score += (
            features["preferred_keyword_hits"] * 0.25
        )

        score -= (
            features["negative_keyword_hits"] * 0.75
        )

        # -------------------------
        # Honeypot
        # -------------------------

        score -= honeypot["penalty"]

        return round(max(score, 0), 4)