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

### src/
- main.py → Entry point  
- jd_parser.py → Job description parser  
- parser.py → Text parsing utilities  
- feature_engine.py → Feature extraction for candidates  
- embeddings.py → Embedding utilities  
- scorer.py → Ranking score calculation  
- reasoner.py → Explanation generator  
- honeypot.py → Fraud / invalid profile detection  
- text_utils.py → Text normalization utilities  
- config.py → Configuration settings  

### data/
- job_description.txt → Sample JD input  
- sample.jsonl → Sample dataset  
- candidates.jsonl → Large dataset (ignored in git due to size limits)  

### output/
- top_100_candidates.csv → Ranked results output  

### Root
- README.md → Project documentation

---

## ⚙️ How It Works

### 1. Job Description Parsing
- Extracts required skills, preferred skills, experience range, and target roles from the JD text.

### 2. Candidate Processing
- Each candidate profile is parsed into structured features.

### 3. Feature Engineering
- Combines candidate attributes into a unified representation for scoring.

### 4. Scoring Engine
- Computes a ranking score based on:
  - Skill overlap
  - Experience match
  - Relevance to JD
  - Penalty signals (negative keywords / mismatch)

### 5. Reason Generation
- Generates human-readable explanations for why a candidate was ranked high or low.

### 6. Honeypot Detection
- Flags suspicious or low-quality profiles before final ranking.
---

## 🧪 Example Flow

### Input
- Job Description → "ML Engineer with experience in embeddings and ranking systems"
- Candidate Profiles → JSONL dataset

### Processing Pipeline
1. JDParser extracts skills → `["python", "embeddings", "ranking"]`
2. FeatureEngine builds candidate vectors
3. Scorer computes match score
4. Honeypot filter removes invalid profiles
5. Reasoner generates explanation

### Output
Top ranked candidates:

1. Candidate A → Score: 0.92
   - Strong match in embeddings + ranking systems

2. Candidate B → Score: 0.87
   - Good ML experience but weaker retrieval systems match
---

## 📦 Installation

### 1. Clone Repository

```bash
git clone https://github.com/mustalidhanerawala/XCoders.git
cd XCoders
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

#### Windows

```bash
.venv\Scripts\activate
```

#### macOS / Linux

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```
---

---

## ▶️ Run Project
```bash
python src/main.py
```
---

## Important Notes
- .venv/ is ignored
- data/ folder is partially ignored due to large dataset files. So please add data/candidates.jsonl

---
