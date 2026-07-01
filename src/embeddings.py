from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from config import EMBEDDING_MODEL


class EmbeddingEngine:

    def __init__(self):

        print("Loading embedding model...")

        self.model = SentenceTransformer(EMBEDDING_MODEL)

        self.jd_embedding = None

    def build_jd_embedding(self, jd_text):

        self.jd_embedding = self.model.encode(
            jd_text,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )

    def batch_encode(self, texts, batch_size=256):

        return self.model.encode(
            texts,
            batch_size=batch_size,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

    def similarity_batch(self, embeddings):

        return cosine_similarity(
            embeddings,
            self.jd_embedding.reshape(1, -1)
        ).flatten()