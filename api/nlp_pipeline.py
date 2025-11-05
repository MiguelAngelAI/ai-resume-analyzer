# api/nlp_pipeline.py
from sentence_transformers import SentenceTransformer
import numpy as np

_model = SentenceTransformer("intfloat/multilingual-e5-small")

def embed_texts(texts):
    """Devuelve embeddings normalizados (np.ndarray) para una lista de textos."""
    embs = _model.encode(texts, convert_to_numpy=True)
    norms = np.linalg.norm(embs, axis=1, keepdims=True)
    norms[norms == 0.0] = 1.0
    return embs / norms
