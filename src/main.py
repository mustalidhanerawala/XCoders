import heapq
import pandas as pd
from tqdm import tqdm

from config import (
    OUTPUT_FILE,
)

from parser import (
    CandidateParser,
    extract_candidate,
    parse_job_description,
)

from jd_parser import JDParser
from feature_engine import FeatureEngine
from embeddings import EmbeddingEngine
from honeypot import HoneypotDetector
from scorer import CandidateScorer
from reasoner import ReasonGenerator


# ==========================================================
# MAIN
# ==========================================================

def main():

    # ------------------------------------------------------
    # Load Job Description
    # ------------------------------------------------------

    print("\nLoading Job Description...")

    jd = JDParser().extract()

    jd_text = parse_job_description()

    # ------------------------------------------------------
    # Initialize Engines
    # ------------------------------------------------------

    feature_engine = FeatureEngine(jd)

    scorer = CandidateScorer()

    honeypot_detector = HoneypotDetector()

    reasoner = ReasonGenerator()

    embedding_engine = EmbeddingEngine()

    embedding_engine.build_jd_embedding(jd_text)

    # ------------------------------------------------------
    # Candidate Loader
    # ------------------------------------------------------

    parser = CandidateParser()

    total = parser.total_candidates()

    # ------------------------------------------------------
    # Stage 1
    # Fast Filtering
    # ------------------------------------------------------

    print("\nStage 1 : Fast filtering 100000 candidates")

    TOP_K = 500

    heap = []

    for raw_candidate in tqdm(
        parser.load_candidates(),
        total=total,
    ):

        candidate = extract_candidate(raw_candidate)

        fast_features = feature_engine.fast_extract(candidate)

        fast_score = scorer.fast_score(fast_features)

        item = (
            fast_score,
            candidate["candidate_id"],
            candidate,
        )

        if len(heap) < TOP_K:

            heapq.heappush(heap, item)

        else:

            if item > heap[0]:

                heapq.heapreplace(heap, item)

    # ------------------------------------------------------
    # Convert Heap
    # ------------------------------------------------------

    shortlisted = [

        item[2]

        for item in sorted(
            heap,
            reverse=True,
        )

    ]

    print(f"\nShortlisted : {len(shortlisted)} candidates")
        # ------------------------------------------------------
    # Stage 2
    # Semantic Embeddings
    # ------------------------------------------------------

    print("\nStage 2 : Semantic ranking")

    texts = [

        c["combined_text"][:1500]

        for c in shortlisted

    ]

    embeddings = embedding_engine.batch_encode(
        texts,
        batch_size=256,
    )

    similarities = embedding_engine.similarity_batch(
        embeddings
    )

    # ------------------------------------------------------
    # Final Scoring
    # ------------------------------------------------------

    print("\nStage 3 : Final scoring")

    final = []

    for candidate, semantic in tqdm(

        zip(shortlisted, similarities),

        total=len(shortlisted),

    ):

        features = feature_engine.full_extract(
            candidate
        )

        honeypot = honeypot_detector.detect(
            candidate
        )

        score = scorer.final_score(

            features,

            float(semantic),

            honeypot,

        )

        final.append({

            "candidate": candidate,

            "features": features,

            "semantic": float(semantic),

            "honeypot": honeypot,

            "score": score,

        })

    # ------------------------------------------------------
    # Sort Final Ranking
    # ------------------------------------------------------

    final.sort(

        key=lambda x: (

            -x["score"],

            x["candidate"]["candidate_id"],

        )

    )
        # ------------------------------------------------------
    # Generate Top 100
    # ------------------------------------------------------

    print("\nStage 4 : Generating Top 100")

    rows = []

    for rank, row in enumerate(final[:100], start=1):

        reasoning = reasoner.generate(

            row["candidate"],

            row["features"],

            row["semantic"],

            row["honeypot"],

            row["score"],

            rank,

            jd,

        )

        rows.append({

            "candidate_id": row["candidate"]["candidate_id"],

            "rank": rank,

            "score": row["score"],

            "reasoning": reasoning,

        })

    # ------------------------------------------------------
    # Save CSV
    # ------------------------------------------------------

    df = pd.DataFrame(

        rows,

        columns=[

            "candidate_id",

            "rank",

            "score",

            "reasoning",

        ],

    )

    df["score"] = df["score"].round(4)

    df.to_csv(

        OUTPUT_FILE,

        index=False,

        encoding="utf-8",

    )

    print("\nDone!")

    print(f"CSV saved to: {OUTPUT_FILE}")

    print("\nTop 10 Candidates\n")

    print(

        df.head(10).to_string(

            index=False

        )

    )


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":

    main()