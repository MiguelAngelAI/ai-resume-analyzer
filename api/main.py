# api/main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from api.extract import extract_text_from_pdf, extract_text_from_docx
from api.scoring import analyze                 # ✅ reemplaza final_score
from api.report import build_markdown_report    # ✅ nuevo import
import tempfile

app = FastAPI(title="AI Resume Analyzer API", version="0.3")

# 🔓 Permitir peticiones desde la app Streamlit (frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API online"}


# 🧾 Endpoint para extraer texto de un solo archivo
@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    ext = file.filename.split(".")[-1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    if ext == "pdf":
        text = extract_text_from_pdf(tmp_path)
    elif ext == "docx":
        text = extract_text_from_docx(tmp_path)
    elif ext == "txt":
        with open(tmp_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    else:
        return {"error": "Formato no soportado"}

    return {"filename": file.filename, "length": len(text), "preview": text[:400]}


# 🧠 Endpoint principal: comparar CV vs Job Description (versión avanzada)
@app.post("/analyze")
async def analyze_endpoint(cv_file: UploadFile = File(...), jd_file: UploadFile = File(...)):
    """Compara un CV y un Job Description y devuelve puntajes, gaps y reporte Markdown"""

    def read_uploaded_file(upload: UploadFile):
        ext = upload.filename.split(".")[-1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
            content = upload.file.read()
            tmp.write(content)
            tmp_path = tmp.name

        if ext == "pdf":
            return extract_text_from_pdf(tmp_path), content
        elif ext == "docx":
            return extract_text_from_docx(tmp_path), content
        elif ext == "txt":
            try:
                return content.decode("utf-8", errors="ignore"), content
            except Exception:
                return content.decode("latin-1", errors="ignore"), content
        else:
            return "", content

    # Extraer texto limpio de ambos archivos
    cv_text, _ = read_uploaded_file(cv_file)
    jd_text, _ = read_uploaded_file(jd_file)

    # Analizar (obtiene sub-scores + skills)
    details = analyze(cv_text, jd_text)

    # Generar reporte Markdown
    report_md = build_markdown_report(cv_file.filename, jd_file.filename, details)

    return {
        "scores": details["scores"],
        "skills": details["skills"],
        "cv_length": len(cv_text),
        "jd_length": len(jd_text),
        "report_md": report_md
    }
