# api/skills.py
import re

SKILLS_BASE = {
    "python", "fastapi", "flask", "django", "pandas", "numpy", "scikit-learn", "pytorch",
    "tensorflow", "transformers", "hugging face", "sentence-transformers", "langchain",
    "faiss", "chromadb", "sql", "postgresql", "mysql", "mongodb", "redis", "docker",
    "kubernetes", "git", "github actions", "ci/cd", "streamlit", "gradio", "react",
    "javascript", "html", "css", "azure", "aws", "gcp", "mlops", "api", "rest", "nlp",
    "computer vision", "llm", "rnn", "cnn", "xgboost", "lightgbm", "plotly", "matplotlib", "seaborn"
}

def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())

def extract_skills(text: str):
    t = normalize(text)
    found = set()
    for s in SKILLS_BASE:
        pattern = r"\b" + re.escape(s) + r"\b"
        if re.search(pattern, t):
            found.add(s)
    return found
