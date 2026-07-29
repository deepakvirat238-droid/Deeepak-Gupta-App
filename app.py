import streamlit as st
import pdfplumber
import re
import time

# ===========================
# PAGE CONFIG
# ===========================

st.set_page_config(
    page_title="MockTest Pro",
    page_icon="📝",
    layout="wide"
)

# ===========================
# SESSION STATE
# ===========================

defaults = {
    "pdf_loaded": False,
    "questions": [],
    "answers": [],
    "current": 0,
    "mode": None,
    "user_answers": {},
    "review": set(),
    "timer_start": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ===========================
# SIDEBAR
# ===========================

st.sidebar.title("📝 MockTest Pro")

menu = st.sidebar.radio(
    "Menu",
    [
        "📂 Upload PDF",
        "🎯 Practice Mode",
        "📝 Mock Test",
        "📊 Result"
    ]
)

st.sidebar.divider()

if st.session_state["pdf_loaded"]:
    st.sidebar.success("✅ PDF Loaded")
else:
    st.sidebar.warning("❌ No PDF")

# ===========================
# UPLOAD PAGE
# ===========================

if menu == "📂 Upload PDF":

    st.title("📂 Upload MCQ PDF")

    uploaded = st.file_uploader(
        "Choose PDF",
        type=["pdf"]
    )

    if uploaded:
        st.success("PDF uploaded successfully.")

        if st.button("Read PDF"):
            st.info("PDF reading will be added in Part 2.")
