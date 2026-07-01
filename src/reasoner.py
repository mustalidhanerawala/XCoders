class ReasonGenerator:

    def generate(
        self,
        candidate,
        features,
        semantic_similarity,
        honeypot,
        score,
        rank,
        jd,
    ):

        sentences = []

        years = candidate["years_of_experience"]

        if years:
            sentences.append(
                f"{years:.1f} years of professional experience."
            )

        title = candidate["current_title"]

        company = candidate["current_company"]

        if title and company:
            sentences.append(
                f"Currently works as {title} at {company}."
            )

        elif title:
            sentences.append(
                f"Current role is {title}."
            )

        matched = []

        candidate_skills = {

            s["name"].lower()

            for s in candidate["skills"]

        }

        for skill in jd["required_skills"]:

            if skill.lower() in candidate_skills:

                matched.append(skill)

        if matched:

            shown = ", ".join(matched[:5])

            sentences.append(

                f"Matches important JD skills including {shown}."

            )

        if features["experience_score"] >= 0.95:

            sentences.append(

                "Experience falls within the desired range."

            )

        elif features["experience_score"] < 0.7:

            sentences.append(

                "Experience is below the preferred range."

            )

        if semantic_similarity >= 0.75:

            sentences.append(

                "Career history is highly aligned with the responsibilities described in the JD."

            )

        elif semantic_similarity >= 0.55:

            sentences.append(

                "Career history shows good alignment with the JD."

            )

        elif semantic_similarity >= 0.40:

            sentences.append(

                "Career history demonstrates partial alignment with the JD."

            )

        if features["product_company"]:

            sentences.append(

                "Has experience in product-focused engineering environments."

            )

        if features["service_company"]:

            sentences.append(

                "Most experience appears to come from service-based organizations."

            )

        if features["github_score"] >= 0.5:

            sentences.append(

                "Shows strong GitHub activity."

            )

        if features["open_to_work"]:

            sentences.append(

                "Currently marked as open to work."

            )

        if features["notice_period"] <= 30:

            sentences.append(

                "Short notice period supports faster availability."

            )

        if honeypot["penalty"] > 0:

            sentences.append(

                "Profile contains timeline or consistency concerns."

            )

        if features["negative_keyword_hits"] > 0:

            sentences.append(

                "Some experience is outside the primary focus of the role."

            )

        # Rank-aware ending

        if rank <= 10:

            sentences.append(

                "Overall, this profile is an excellent match for the position."

            )

        elif rank <= 30:

            sentences.append(

                "Overall, this profile is a strong match for the position."

            )

        elif rank <= 60:

            sentences.append(

                "Overall, this profile is a good match for the position."

            )

        else:

            sentences.append(

                "Overall, this profile meets several important requirements but has more gaps than higher-ranked candidates."

            )

        return " ".join(sentences)