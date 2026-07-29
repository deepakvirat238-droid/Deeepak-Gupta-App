import streamlit as st
import pdfplumber
import re
import time

# -----------------------------
# APP CONFIG
# -----------------------------
st.set_page_config(
    page_title="MockTest Pro",
    page_icon="📝",
    layout="wide"
)

# -----------------------------
# SESSION STATE
# -----------------------------
if "pdf_loaded" not in st.session_state:
    st.session_state.pdf_loaded = False

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

if "answer_text" not in st.session_state:
    st.session_state.answer_text = ""

if "questions" not in st.session_state:
    st.session_state.questions = []

if "answer_key" not in st.session_state:
    st.session_state.answer_key = {}

if "current" not in st.session_state:
    st.session_state.current = 0

if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}

if "review" not in st.session_state:
    st.session_state.review = []

if "score" not in st.session_state:
    st.session_state.score = 0

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("📝 MockTest Pro")

page = st.sidebar.radio(
    "Menu",
    [
        "🏠 Home",
        "📂 Upload PDF",
        "🎯 Practice Mode",
        "📝 Mock Test",
        "📊 Result"
    ]
)

# -----------------------------
# HOME
# -----------------------------
if page == "🏠 Home":

    st.title("📝 MockTest Pro")

    st.write("Convert MCQ PDF into Testbook Style Mock Test.")

# -----------------------------
# UPLOAD PAGE
# -----------------------------
elif page == "📂 Upload PDF":

    st.title("📂 Upload PDF")

    uploaded_pdf = st.file_uploader(
        "Choose PDF",
        type=["pdf"]
    )

    if uploaded_pdf:

        st.success(uploaded_pdf.name)

        if st.button("Read PDF"):

            st.info("Step 2 will add PDF Reader.")

# -----------------------------
# PRACTICE
# -----------------------------
elif page == "🎯 Practice Mode":

    st.title("🎯 Practice Mode")

    st.warning("Upload PDF First")

# -----------------------------
# MOCK TEST
# -----------------------------
elif page == "📝 Mock Test":

    st.title("📝 Mock Test")

    st.warning("Upload PDF First")

# -----------------------------
# RESULT
# -----------------------------
elif page == "📊 Result":

    st.title("📊 Result")

    st.info("No Result Yet")
    
