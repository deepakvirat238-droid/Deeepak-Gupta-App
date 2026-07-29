import streamlit as st
import pdfplumber
import re
import time

# ----------------------------
# App Config
# ----------------------------
st.set_page_config(
    page_title="MockTest Pro",
    page_icon="📝",
    layout="wide"
)

# ----------------------------
# Session State
# ----------------------------
DEFAULTS = {
    "pdf_loaded": False,
    "pdf_text": "",
    "answer_text": "",
    "questions": [],
    "answer_key": {},
    "current": 0,
    "user_answers": {},
    "review": [],
    "mode": "",
    "score": 0,
    "start_time": None,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ----------------------------
# Sidebar
# ----------------------------
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

# ----------------------------
# Home
# ----------------------------
if page == "🏠 Home":
    st.title("📝 MockTest Pro")
    st.write("Convert any MCQ PDF into a Testbook-style mock test.")

# ----------------------------
# Upload PDF
# ----------------------------
elif page == "📂 Upload PDF":

    st.title("📂 Upload PDF")

    uploaded_pdf = st.file_uploader(
        "Choose PDF",
        type=["pdf"]
    )

    if uploaded_pdf:
        st.success(f"Selected: {uploaded_pdf.name}")

        with pdfplumber.open(uploaded_pdf) as pdf:

    question_text = ""
    answer_text = ""

    total_pages = len(pdf.pages)

    for i, page in enumerate(pdf.pages):

        text = page.extract_text()

        if not text:
            continue

        if i == total_pages - 1:
            answer_text = text
        else:
            question_text += text + "\n"

st.session_state["pdf_loaded"] = True
st.session_state["pdf_text"] = question_text
st.session_state["answer_text"] = answer_text

st.success("✅ PDF Read Successfully")

with st.expander("📄 Question Pages"):
    st.text_area(
        "Questions",
        question_text,
        height=250
    )

with st.expander("🔑 Last Page (Answer Key)"):
    st.text_area(
        "Answer Key",
        answer_text,
        height=180
    )

# ----------------------------
# Practice Mode
# ----------------------------
elif page == "🎯 Practice Mode":
    st.title("🎯 Practice Mode")
    st.info("Please upload a PDF first.")

# ----------------------------
# Mock Test
# ----------------------------
elif page == "📝 Mock Test":
    st.title("📝 Mock Test")
    st.info("Please upload a PDF first.")

# ----------------------------
# Result
# ----------------------------
elif page == "📊 Result":
    st.title("📊 Result")
    st.info("No result available.")
    
