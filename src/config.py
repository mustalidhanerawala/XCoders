"""
Global configuration for the AI Candidate Ranking System.
Only constants and configuration values should live here.
"""

# ==========================================================
# FILE PATHS
# ==========================================================

CANDIDATE_FILE = "data/candidates.jsonl"
JOB_DESCRIPTION_FILE = "data/job_description.txt"
OUTPUT_FILE = "output/top_100_candidates.csv"


# ==========================================================
# EMBEDDING MODEL
# ==========================================================

# Small, fast and accurate enough for CPU.
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


# ==========================================================
# FINAL SCORE WEIGHTS
# Total = 100
# ==========================================================

WEIGHTS = {
    "semantic_similarity": 25,
    "required_skills": 20,
    "preferred_skills": 8,
    "experience": 10,
    "current_title": 8,
    "career_history": 6,
    "projects_summary": 5,
    "education": 4,
    "industry": 3,
    "behavioral": 7,
    "certifications": 2,
    "location": 2,
}


# ==========================================================
# BEHAVIORAL SIGNAL WEIGHTS
# ==========================================================

BEHAVIOR_WEIGHTS = {
    "open_to_work": 2,
    "recent_activity": 2,
    "github": 1,
    "profile_complete": 1,
    "recruiter_response": 1,
}


# ==========================================================
# IDEAL EXPERIENCE RANGE
# ==========================================================

IDEAL_MIN_YOE = 5
IDEAL_MAX_YOE = 9


# ==========================================================
# PRODUCT COMPANIES
# ==========================================================

PRODUCT_COMPANIES = {
    "google",
    "meta",
    "amazon",
    "microsoft",
    "apple",
    "netflix",
    "uber",
    "swiggy",
    "zomato",
    "flipkart",
    "razorpay",
    "cred",
    "phonepe",
    "atlassian",
    "meesho",
    "postman",
}


# ==========================================================
# SERVICE COMPANIES
# ==========================================================

SERVICE_COMPANIES = {
    "tcs",
    "infosys",
    "wipro",
    "cognizant",
    "capgemini",
    "mindtree",
    "ltimindtree",
    "accenture",
    "tech mahindra",
    "hcl",
}


# ==========================================================
# REQUIRED SKILL KEYWORDS
# ==========================================================

REQUIRED_KEYWORDS = {
    "python",
    "embeddings",
    "retrieval",
    "ranking",
    "recommendation",
    "vector database",
    "vector search",
    "faiss",
    "milvus",
    "pinecone",
    "weaviate",
    "qdrant",
    "opensearch",
    "elasticsearch",
    "bm25",
    "sentence transformer",
    "bge",
    "e5",
    "llm",
    "machine learning",
    "evaluation",
    "ndcg",
    "mrr",
    "map",
    "a/b testing",
}


# ==========================================================
# NICE TO HAVE
# ==========================================================

PREFERRED_KEYWORDS = {
    "lora",
    "qlora",
    "peft",
    "distributed systems",
    "recommendation systems",
    "ranking systems",
    "opensource",
    "github",
    "hr tech",
    "recruitment",
    "marketplace",
}


# ==========================================================
# NEGATIVE KEYWORDS
# ==========================================================

NEGATIVE_KEYWORDS = {
    "computer vision",
    "speech recognition",
    "robotics",
    "marketing",
    "sales",
    "graphic design",
    "photoshop",
}


# ==========================================================
# SIMPLE SKILL NORMALIZATION
# ==========================================================

SKILL_SYNONYMS = {

    "ml": "machine learning",
    "machine-learning": "machine learning",

    "llms": "llm",
    "large language models": "llm",

    "rag": "retrieval",

    "vector db": "vector database",
    "vector databases": "vector database",

    "elastic search": "elasticsearch",

    "sentence-transformers": "sentence transformer",

    "fine tuning": "fine-tuning",
    "finetuning": "fine-tuning",

    "recommender systems": "recommendation systems",
}


# ==========================================================
# HONEYPOT LIMITS
# ==========================================================

MAX_ADVANCED_SKILLS = 15

MAX_SKILL_MONTH_FACTOR = 1.5

MAX_ALLOWED_JOB_OVERLAP_MONTHS = 2


# ==========================================================
# DATE FORMAT
# ==========================================================

DATE_FORMAT = "%Y-%m-%d"