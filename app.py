import streamlit as st
import pdfplumber
import re
import time

# ======================================
# MOCKTEST PRO V5
# PART 1
# ======================================

st.set_page_config(
    page_title="MockTest Pro",
    page_icon="📝",
    layout="wide"
)

# ---------- Session State ----------

if "app" not in st.session_state:
    st.session_state.app = {
        "pdf_loaded": False,
        "pdf_name": "",
        "pdf_text": "",
        "answer_text": "",
        "questions": [],
        "answer_key": {},
        "current": 0,
        "mode": "",
        "user_answers": {},
        "review": [],
        "score": 0,
        "start_time": None
    }

APP = st.session_state.app

# ---------- Header ----------

st.title("📝 MockTest Pro")
st.caption("Convert any MCQ PDF into a Testbook Style Mock Test")

# ---------- Sidebar ----------

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📂 Upload PDF",
        "🎯 Practice Mode",
        "📝 Mock Test",
        "📊 Result"
    ]
)

# ---------- Home ----------

if menu == "🏠 Home":

    st.subheader("Welcome")

    st.info(
        """
Features

✅ PDF Upload

✅ Auto Question Detection

✅ Auto Answer Key Detection

✅ Practice Mode

✅ Mock Test

✅ Timer

✅ Save & Next

✅ Previous

✅ Question Palette

✅ Result Analysis
"""
    )

# ---------- Upload ----------

elif menu == "📂 Upload PDF":

    st.subheader("Upload MCQ PDF")

    pdf = st.file_uploader(
        "Choose PDF",
        type=["pdf"]
    )

    if pdf:

        APP["pdf_name"] = pdf.name

        st.success(pdf.name)

        if st.button("Read PDF"):

            st.info("PDF Reader will be added in Part 2.")

# ---------- Practice ----------

elif menu == "🎯 Practice Mode":

    st.warning("Upload a PDF first.")

# ---------- Mock Test ----------

elif menu == "📝 Mock Test":

    st.warning("Upload a PDF first.")

# ---------- Result ----------

elif menu == "📊 Result":

    st.warning("No Result Available.")
    
