import streamlit as st
import pandas as pd
import pdfplumber
import plotly.graph_objects as go
from matcher import calculate_similarity
from ats import get_missing_keywords
from skills import extract_skills

# Must be the first Streamlit command
st.set_page_config(page_title="CareerFit | ATS Scanner", page_icon="💼", layout="wide")

# Custom CSS for a professional, clean SaaS look
custom_css = """
<style>
    /* Main background and font */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    h1, h2, h3 {
        color: #1E293B;
        font-family: 'Inter', sans-serif;
    }
    /* Hide default Streamlit elements */
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div[data-baseweb="textarea"] > div > small {display: none !important;}
    
    /* Enhance metric display */
    div[data-testid="stMetricValue"] {
        color: #2563EB;
        font-weight: 700;
    }
    
    /* Clean up expanders */
    .streamlit-expanderHeader {
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        color: #334155 !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ----------------- HELPER FUNCTIONS -----------------
@st.cache_data(show_spinner=False)
def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
    return text

def create_radar_chart(resume_skills, jd_skills):
    all_skills = list(set(resume_skills + jd_skills))
    if not all_skills or len(all_skills) < 3:
        return None
    
    resume_vals = [1 if skill in resume_skills else 0 for skill in all_skills]
    jd_vals = [1 if skill in jd_skills else 0 for skill in all_skills]

    all_skills.append(all_skills[0])
    resume_vals.append(resume_vals[0])
    jd_vals.append(jd_vals[0])

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=resume_vals, theta=all_skills, fill='toself', name='My Skills',
        line_color='#2563EB', fillcolor='rgba(37, 99, 235, 0.4)'
    ))
    fig.add_trace(go.Scatterpolar(
        r=jd_vals, theta=all_skills, fill='toself', name='Required Skills', 
        line_color='#94A3B8', fillcolor='rgba(148, 163, 184, 0.2)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=False, range=[0, 1]),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="center", x=0.5),
        margin=dict(t=20, b=20, l=20, r=20)
    )
    return fig

# ----------------- UI LAYOUT -----------------

st.markdown("<h1 style='text-align: center; color: #1E293B;'>CareerFit ATS Scanner</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.1rem; color: #64748B; margin-bottom: 2rem;'>Evaluate your master resume against targeted job descriptions to identify your highest-probability matches.</p>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### My Profile")
    st.markdown("Upload your core resume document.")
    resume_file = st.file_uploader("Upload Resume", type=["pdf"], label_visibility="collapsed")
    
    st.divider()
    st.caption("🔒 All processing is done locally. Your data is not stored.")

# Main content area
st.markdown("### Job Descriptions")
st.markdown("Upload the roles you are considering applying for (PDF format).")
jd_files = st.file_uploader("Upload Job Descriptions", type=["pdf"], accept_multiple_files=True, label_visibility="collapsed")

st.write("") # Spacer

if st.button("Evaluate Fit", type="primary", use_container_width=True):
    if not resume_file:
        st.error("Please upload your Master Resume in the sidebar to proceed.")
    elif not jd_files:
        st.error("Please upload at least one Job Description.")
    else:
        results = []
        
        # Modern loading status indicator
        with st.status("Analyzing your profile fit...", expanded=True) as status:
            st.write("📄 Extracting skills from your master resume...")
            my_resume_text = extract_text_from_pdf(resume_file)
            my_skills = extract_skills(my_resume_text)
            
            st.write(f"🔄 Cross-referencing against {len(jd_files)} job requirements...")
            for jd_file in jd_files:
                jd_text = extract_text_from_pdf(jd_file)
                jd_skills = extract_skills(jd_text)
                
                match_score = calculate_similarity(my_resume_text, jd_text)
                missing_kw = get_missing_keywords(my_resume_text, jd_text)
                
                results.append({
                    "Job Title": jd_file.name.replace(".pdf", ""),
                    "Match Score": match_score,
                    "Missing Keywords": ", ".join(missing_kw) if missing_kw else "None detected",
                    "JD Skills": jd_skills
                })
                
            status.update(label="Analysis Complete!", state="complete", expanded=False)
            
        # Compile dataframe
        df = pd.DataFrame(results).sort_values(by="Match Score", ascending=False).reset_index(drop=True)
        df.index = df.index + 1
        
        # Top Match Summary
        st.divider()
        st.markdown("### 🏆 Top Matches")
        
        # Styled Dataframe using Column Configs for a professional look
        st.dataframe(
            df[["Job Title", "Match Score", "Missing Keywords"]],
            column_config={
                "Job Title": st.column_config.TextColumn("Job Title / File", width="medium"),
                "Match Score": st.column_config.ProgressColumn(
                    "Match %",
                    help="Semantic similarity score based on AI embeddings",
                    format="%.2f%%",
                    min_value=0,
                    max_value=100,
                ),
                "Missing Keywords": st.column_config.TextColumn("Identified Gaps", width="large")
            },
            hide_index=True,
            use_container_width=True
        )
        
        st.write("")
        st.markdown("### 📊 Detailed Breakdown")
        
        # Visually clean expanders
        for i, row in df.iterrows():
            with st.expander(f"{row['Job Title']}  ( {row['Match Score']}% )", expanded=(i==0)):
                col_text, col_chart = st.columns([1, 1.2])
                
                with col_text:
                    st.metric(label="Overall Match", value=f"{row['Match Score']}%")
                    
                    st.markdown("**Actionable Gaps:**")
                    if row["Missing Keywords"] != "None detected":
                        # Display keywords as clean inline code snippets
                        gaps = [f"`{kw}`" for kw in row["Missing Keywords"].split(", ")]
                        st.markdown(" ".join(gaps))
                    else:
                        st.info("No significant gaps detected.")
                        
                    st.markdown("**Core Required Skills:**")
                    if row['JD Skills']:
                        skills = [f"`{sk}`" for sk in row['JD Skills']]
                        st.markdown(" ".join(skills))
                    else:
                        st.write("None explicitly parsed.")
                        
                with col_chart:
                    radar_fig = create_radar_chart(my_skills, row['JD Skills'])
                    if radar_fig:
                        st.plotly_chart(radar_fig, use_container_width=True, config={'displayModeBar': False})
                    else:
                        st.caption("Insufficient skills detected to plot a radar chart.")
