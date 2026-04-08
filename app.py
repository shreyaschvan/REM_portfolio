import streamlit as st
import os
import json
from pathlib import Path
from streamlit_pdf_viewer import pdf_viewer  # Make sure to install this!

# ─────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Shreyas | Portfolio & Assignments",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CSS — premium dark-mode Midnight Emerald & Gold
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp {
    background: linear-gradient(135deg, #040d0c 0%, #0a1f1c 40%, #0f172a 100%);
}

section[data-testid="stSidebar"] {
    background: rgba(5, 15, 13, 0.9);
    backdrop-filter: blur(16px);
    border-right: 1px solid rgba(255,255,255,0.05);
}

.glass-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(16, 185, 129, 0.1);
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 24px;
    backdrop-filter: blur(12px);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.glass-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.3);
}

.hero { text-align: center; padding: 48px 16px 36px; }
.hero h1 {
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #34d399 0%, #fbbf24 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
}

.section-heading {
    font-size: 1.6rem;
    font-weight: 700;
    color: #6ee7b7;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.stat-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.25);
    border-radius: 999px;
    padding: 8px 20px;
    color: #a7f3d0;
    font-size: 0.92rem;
    margin: 4px;
}

.skill-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(20, 184, 166, 0.15), rgba(16, 185, 129, 0.15));
    border: 1px solid rgba(52, 211, 153, 0.3);
    border-radius: 10px;
    padding: 8px 18px;
    color: #6ee7b7;
    font-size: 0.88rem;
    margin: 4px;
}

.pdf-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(16, 185, 129, 0.1);
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 14px;
    color: #e2e8f0;
}

.contact-link {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    color: #fbbf24;
    text-decoration: none;
    padding: 10px 20px;
    border-radius: 12px;
    background: rgba(251, 191, 36, 0.08);
    border: 1px solid rgba(251, 191, 36, 0.2);
    margin: 4px;
    transition: 0.3s;
}
.contact-link:hover {
    background: rgba(251, 191, 36, 0.15);
    border: 1px solid rgba(251, 191, 36, 0.4);
}

.custom-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(52, 211, 153, 0.3), transparent);
    margin: 32px 0;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Data helpers
# ─────────────────────────────────────────────
UPLOAD_DIR = Path("uploaded_assignments")
UPLOAD_DIR.mkdir(exist_ok=True)
META_FILE = UPLOAD_DIR / "meta.json"

def load_meta():
    if META_FILE.exists():
        return json.loads(META_FILE.read_text())
    return []

def save_meta(data):
    META_FILE.write_text(json.dumps(data, indent=2))

def save_uploaded_pdf(uploaded_file, subject, description):
    file_path = UPLOAD_DIR / uploaded_file.name
    file_path.write_bytes(uploaded_file.getbuffer())
    meta = load_meta()
    meta.append({
        "filename": uploaded_file.name,
        "subject": subject,
        "description": description,
        "size_kb": round(len(uploaded_file.getbuffer()) / 1024, 1),
    })
    save_meta(meta)

def delete_pdf(filename):
    meta = [m for m in load_meta() if m["filename"] != filename]
    save_meta(meta)
    fpath = UPLOAD_DIR / filename
    if fpath.exists(): fpath.unlink()

# ─────────────────────────────────────────────
# Profile Data
# ─────────────────────────────────────────────
PROFILE = {
    "name": "Shreyas Chavan",
    "tagline": "AI/ML Engineering Student • Full-Stack Developer",
    "about": (
        "I am a final-year engineering student with a focus on AI and Machine Learning. "
        "I specialize in building intelligent systems like Medi-Vision Hybrid and prescription automation tools."
    ),
    "skills": ["Python", "Streamlit", "Flask", "React", "Machine Learning", "Deep Learning", "SQL", "Git"],
    "education": [
        {
            "degree": "B.Tech (Honors in AI & ML)",
            "institution": "Engineering University",
            "period": "2022 – 2026",
            "details": "Specializing in medical imaging diagnostics and process automation.",
        }
    ],
    "contact": {
        "email": "chavanshreyas732@gmail.com",
        "linkedin": "www.linkedin.com/in/shreyas-chavan-673344321",
    },
}

# ─────────────────────────────────────────────
# Sidebar Navigation
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧭 Navigation")
    page = st.radio("Go to", ["🏠 Home", "📄 Assignments", "📬 Contact"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown(f"<div style='text-align:center;'><span style='color:#34d399; font-weight:700;'>{PROFILE['name']}</span></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Page Content
# ─────────────────────────────────────────────
if page == "🏠 Home":
    st.markdown(f"<div class='hero'><h1>{PROFILE['name']}</h1><p style='color:#a7f3d0;'>{PROFILE['tagline']}</p></div>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="stat-pill">🛠️ {len(PROFILE["skills"])} Skills</div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="stat-pill">🎓 Graduating 2026</div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="stat-pill">📄 {len(load_meta())} Assignments</div>', unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">👋 About Me</div>', unsafe_allow_html=True)
    st.markdown(f"<div style='color:#e2e8f0; line-height:1.6;'>{PROFILE['about']}</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-heading" style="margin-top:30px;">🛠️ Tech Stack</div>', unsafe_allow_html=True)
    skills_html = "".join([f'<span class="skill-badge">{s}</span>' for s in PROFILE["skills"]])
    st.markdown(f"<div>{skills_html}</div>", unsafe_allow_html=True)

elif page == "📄 Assignments":
    st.markdown('<div class="section-heading">📄 My Assignments</div>', unsafe_allow_html=True)
    
    with st.expander("➕ Upload New Assignment"):
        with st.form("upload_form", clear_on_submit=True):
            uploaded = st.file_uploader("Select PDF", type=["pdf"])
            subject = st.text_input("Subject")
            desc = st.text_input("Short Description")
            if st.form_submit_button("Upload") and uploaded:
                save_uploaded_pdf(uploaded, subject, desc)
                st.success("File saved!")
                st.rerun()

    meta = load_meta()
    if not meta:
        st.info("No assignments yet.")
    else:
        for entry in meta:
            col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
            with col1:
                st.markdown(f"<div class='pdf-card'><b>{entry['filename']}</b><br><small>{entry['subject']} | {entry['size_kb']}KB</small></div>", unsafe_allow_html=True)
            with col2:
                if st.button("👁️ View", key=f"view_{entry['filename']}"):
                    st.session_state["viewing_pdf"] = entry["filename"]
            with col3:
                if st.button("🗑️ Delete", key=f"del_{entry['filename']}"):
                    delete_pdf(entry["filename"])
                    st.rerun()

    if "viewing_pdf" in st.session_state:
        viewing = st.session_state["viewing_pdf"]
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        
        pdf_path = UPLOAD_DIR / viewing
        
        if pdf_path.exists():
            title_col, btn_col = st.columns([0.85, 0.15])
            with title_col:
                st.markdown(f"<h3 style='color:#6ee7b7;'>📖 Viewing: {viewing}</h3>", unsafe_allow_html=True)
            with btn_col:
                if st.button("✖️ Close", use_container_width=True):
                    del st.session_state["viewing_pdf"]
                    st.rerun()
            
            with open(pdf_path, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
            
            st.download_button(
                label="⬇️ Download PDF",
                data=pdf_bytes,
                file_name=viewing,
                mime="application/pdf",
                type="primary"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            try:
                pdf_viewer(input=pdf_bytes, width=800, height=800)
            except Exception as e:
                st.error("Viewer component failed. Please use the download button above.")
        else:
            st.error("File not found on disk.")

elif page == "📬 Contact":
    st.markdown('<div class="section-heading">📬 Contact</div>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="glass-card" style="max-width:500px;">
            <a href="mailto:{PROFILE['contact']['email']}" class="contact-link">✉️ {PROFILE['contact']['email']}</a><br>
            <a href="{PROFILE['contact']['linkedin']}" class="contact-link">🔗 LinkedIn</a>
        </div>
    """, unsafe_allow_html=True)