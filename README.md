# XCoders – AI Candidate Ranking System

XCoders is an AI-powered candidate ranking system that evaluates and ranks candidates against a job description using NLP-based feature extraction, embeddings, and rule-based scoring logic. The system is designed to simulate real-world hiring intelligence by combining structured parsing, semantic matching, and heuristic scoring.

---

## 🚀 Features

- 📄 Job Description parsing (skills, experience, roles)
- 👤 Candidate feature extraction
- 🧠 Semantic embeddings support (optional integration)
- 📊 Multi-factor ranking system
- 🚨 Honeypot / fraud signal detection
- 🔍 Skill-based matching + normalization
- 📈 Explainable ranking reasoning system

---

## 📁 Project Structure
XCoders/
│
├── src/
│   ├── main.py              # Entry point
│   ├── jd_parser.py         # Job description parser
│   ├── parser.py            # Text parsing utilities
│   ├── feature_engine.py    # Feature extraction for candidates
│   ├── embeddings.py        # Embedding utilities
│   ├── scorer.py            # Ranking score calculation
│   ├── reasoner.py          # Explanation generator
│   ├── honeypot.py          # Fraud / invalid profile detection
│   ├── text_utils.py        # Text normalization utilities
│   └── config.py            # Configuration settings
│
├── data/
│   ├── job_description.txt  # Sample JD input
│   ├── sample.jsonl         # Sample dataset
│   └── candidates.jsonl     # Large dataset (ignored in git)
│
├── output/
│   └── top_100_candidates.csv
│
└── README.md

---

## ⚙️ How It Works
-Job Description Parsing: Extracts required skills, preferred skills, experience, and roles.
-Candidate Processing: Converts candidate profiles into structured features.
-Feature Engineering: Builds combined representations for scoring.
-Scoring Engine: Computes ranking score using weighted logic.
-Reason Generation: Produces human-readable explanations for rankings.
-Honeypot Detection: Filters suspicious or low-quality profiles.

---

## 🧪 Example Flow
</>
-
from src.main import run_pipeline
results = run_pipeline()
print(results[:10])

---

## 📦 Installation
</>
-
git clone https://github.com/<your-username>/XCoders.git
cd XCoders
pip install -r requirements.txt

---

## ▶️ Run Project
-python src/main.py

---

## Important Notes
-.venv/ is ignored 
-data/ folder is partially ignored due to large dataset files. So please add data/candidates.jsonl
