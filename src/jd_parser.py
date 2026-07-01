import re

from parser import parse_job_description


class JDParser:

    def __init__(self):
        self.text = parse_job_description()

    def extract(self):

        return {

            "required_skills": self.required_skills(),

            "preferred_skills": self.preferred_skills(),

            "negative_keywords": self.negative_keywords(),

            "locations": self.locations(),

            "experience": self.experience(),

            "desired_titles": self.desired_titles(),
        }

    def required_skills(self):

        skills = [

            "python",

            "embeddings",

            "retrieval",

            "ranking",

            "llm",

            "machine learning",

            "vector database",

            "faiss",

            "pinecone",

            "weaviate",

            "qdrant",

            "milvus",

            "elasticsearch",

            "opensearch",

            "hybrid search",

            "sentence transformers",

            "bge",

            "e5",

            "evaluation",

            "ndcg",

            "mrr",

            "map",

            "a/b testing",

            "offline benchmark",

            "fine tuning",

            "lora",

            "qlora",

            "peft",

            "recommendation system",

            "search",

            "information retrieval",

            "distributed systems",
        ]

        found = []

        text = self.text.lower()

        for skill in skills:

            if skill in text:
                found.append(skill)

        return sorted(set(found))

    def preferred_skills(self):

        skills = [

            "learning to rank",

            "xgboost",

            "neural ranking",

            "hr tech",

            "marketplace",

            "open source",

            "github",

            "distributed inference",

            "large scale inference",

        ]

        found = []

        text = self.text.lower()

        for skill in skills:

            if skill in text:
                found.append(skill)

        return sorted(set(found))

    def negative_keywords(self):

        negatives = [

            "computer vision",

            "speech",

            "robotics",

            "consulting",

            "langchain",

            "research",

            "academic",

            "architecture",

            "tech lead",

            "marketing",

            "framework",

        ]

        found = []

        text = self.text.lower()

        for word in negatives:

            if word in text:
                found.append(word)

        return sorted(set(found))

    def locations(self):

        cities = [

            "pune",

            "noida",

            "mumbai",

            "hyderabad",

            "delhi",

        ]

        found = []

        text = self.text.lower()

        for city in cities:

            if city in text:
                found.append(city)

        return sorted(set(found))

    def experience(self):

        match = re.search(r"(\d+)\s*-\s*(\d+)\s*years", self.text.lower())

        if match:

            return {

                "min": int(match.group(1)),

                "max": int(match.group(2)),
            }

        return {

            "min": 0,

            "max": 100,
        }

    def desired_titles(self):

        titles = [

            "ai engineer",

            "machine learning engineer",

            "ml engineer",

            "applied scientist",

            "software engineer",

            "backend engineer",

            "search engineer",

            "ranking engineer",

        ]

        found = []

        text = self.text.lower()

        for title in titles:

            if title in text:
                found.append(title)

        return sorted(set(found))