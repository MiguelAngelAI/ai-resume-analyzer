import streamlit as st
import requests
import plotly.graph_objects as go

st.set_page_config(page_title="AI Resume Analyzer", layout="centered", page_icon="🧠")

# --- Header ---
st.markdown("""
<style>
    .title { font-size: 2.5em; font-weight: bold; }
    .subheader { font-size: 1.1em; color: gray; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🧠 AI Resume Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Compare your CV against a job description and get actionable insights</div>', unsafe_allow_html=True)

st.markdown("---")

# --- Upload Section ---
col1, col2 = st.columns(2)
with col1:
    cv_file = st.file_uploader("📄 Upload your CV (PDF / DOCX)", type=["pdf", "docx"], key="cv")
with col2:
    jd_file = st.file_uploader("📑 Upload the Job Description (PDF / DOCX / TXT)", type=["pdf", "docx", "txt"], key="jd")

# --- Analyze Button ---
st.markdown("\n")
center_button = st.columns([1, 2, 1])[1]
with center_button:
    analyze = st.button("🔍 Analyze", use_container_width=True)

# --- Main Logic ---
if analyze and cv_file and jd_file:
    with st.spinner("Analyzing files..."):

        files = {
            "cv_file": (cv_file.name, cv_file, cv_file.type),
            "jd_file": (jd_file.name, jd_file, jd_file.type),
        }

        try:
            response = requests.post("http://127.0.0.1:8000/analyze", files=files)
            response.raise_for_status()
            result = response.json()
        except Exception as e:
            st.error(f"❌ Error while analyzing: {e}")
            st.stop()

        if "scores" not in result or "final" not in result["scores"]:
            st.error("❌ Could not calculate the score. Check the content of both files.")
            st.stop()

        # --- Display Main Score ---
        score = result["scores"]["final"]
        st.success(f"✅ Match Score: {score:.2f}%")

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": "Overall Fit (%)"},
            gauge={"axis": {"range": [0, 100]}, "bar": {"color": "green"}},
            number={"valueformat": ".1f"},
        ))
        st.plotly_chart(fig, use_container_width=True)

        # --- Display Sub-Scores ---
        if "scores" in result:
            st.markdown("### 🧩 Section Breakdown")
            for k in ["skill_coverage", "semantic_fit", "format"]:
                if k in result["scores"]:
                    st.progress(result["scores"][k] / 100.0, text=f"{k.replace('_', ' ').title()}: {result['scores'][k]:.1f}%")

        # --- Skills Overview ---
        with st.expander("🧠 Skills found in your CV"):
            st.write(", ".join(result.get("skills", {}).get("match", []) or ["None found."]))

        with st.expander("🚫 Missing skills from the job description"):
            st.write(", ".join(result.get("skills", {}).get("missing", []) or ["None"]))

        # --- Downloadable Report ---
        if "report_md" in result:
            st.markdown("### 📥 Download full report")
            st.download_button(
                label="💾 Download Markdown Report",
                data=result["report_md"],
                file_name="resume_analysis_report.md",
                mime="text/markdown",
            )
else:
    st.info("Please upload both your CV and a Job Description to start the analysis.")
