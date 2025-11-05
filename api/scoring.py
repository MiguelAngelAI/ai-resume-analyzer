# api/scoring.py
import re
from api.nlp_pipeline import embed_texts
from api.skills import extract_skills

def clean_text(t: str) -> str:
    return re.sub(r"\s+", " ", t.strip().lower())

def skill_coverage_details(cv_text: str, jd_text: str):
    cv_sk = extract_skills(cv_text)
    jd_sk = extract_skills(jd_text)
    common = sorted(cv_sk & jd_sk)
    missing = sorted(jd_sk - cv_sk)
    coverage = len(common) / max(len(jd_sk), 1)
    return coverage, common, missing, sorted(jd_sk)

def semantic_fit(cv_text: str, jd_text: str) -> float:
    cv_vec, jd_vec = embed_texts([cv_text, jd_text])
    cos = float((cv_vec[0] * jd_vec[1]).sum())
    return (cos + 1.0) / 2.0

def format_score(cv_text: str) -> float:
    t = cv_text
    checks = 0
    total = 5
    if re.search(r"@|linkedin\.com|github\.com", t, re.I): checks += 1
    if re.search(r"\b(20\d{2}|19\d{2})\b", t): checks += 1
    if len(t) > 800: checks += 1
    if re.search(r"•|- |\n- ", t): checks += 1
    if re.search(r"\b(email|phone|tel)\b", t, re.I): checks += 1
    return checks / total

def analyze(cv_text: str, jd_text: str):
    s_cov, common, missing, jd_all = skill_coverage_details(cv_text, jd_text)
    s_sem = semantic_fit(cv_text, jd_text)
    s_fmt = format_score(cv_text)

    final = (0.40*s_cov + 0.40*s_sem + 0.20*s_fmt) * 100.0

    return {
        "scores": {
            "skill_coverage": round(s_cov*100, 2),
            "semantic_fit":  round(s_sem*100, 2),
            "format":        round(s_fmt*100, 2),
            "final":         round(final, 2),
        },
        "skills": {
            "match": common,
            "missing": missing,
            "jd_all": jd_all
        }
    }
