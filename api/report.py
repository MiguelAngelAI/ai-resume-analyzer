# api/report.py
from datetime import datetime

def build_markdown_report(cv_name: str, jd_name: str, details: dict) -> str:
    s = details["scores"]
    skills = details["skills"]
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")

    md = []
    md.append(f"# AI Resume Analyzer — Reporte")
    md.append(f"_Generado: {ts}_\n")
    md.append(f"**CV:** {cv_name}  \n**Job Description:** {jd_name}\n")

    md.append("## Puntajes")
    md.append(f"- Skill Coverage: **{s['skill_coverage']}%**")
    md.append(f"- Semantic Fit: **{s['semantic_fit']}%**")
    md.append(f"- Format & Completeness: **{s['format']}%**")
    md.append(f"- **Match Score (Final): {s['final']}%**\n")

    md.append("## Skills del JD detectadas")
    md.append(", ".join(skills["jd_all"]) if skills["jd_all"] else "_(No detectadas)_")
    md.append("\n## Skills en común (CV ∩ JD)")
    md.append(", ".join(skills["match"]) if skills["match"] else "_(Ninguna)_")
    md.append("\n## Gaps (Skills del JD que faltan en el CV)")
    md.append(", ".join(skills["missing"]) if skills["missing"] else "_(Sin gaps)_")

    md.append("\n## Recomendaciones")
    if skills["missing"]:
        md.append("- Agregá una sección **Skills** con los términos faltantes si realmente los conocés.")
        md.append("- Añadí **bullets con métricas** en experiencias relevantes.")
        md.append("- Destacá proyectos donde uses los skills faltantes.")
    else:
        md.append("- El CV ya cubre las skills clave del JD. Pulí bullets con logros cuantificables.")
    md.append("- Incluí enlaces a **GitHub/LinkedIn** visibles.")
    md.append("- Mantené el CV en **1 página** si es posible.")

    return "\n".join(md) + "\n"
