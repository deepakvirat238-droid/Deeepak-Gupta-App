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

        if st.button("Read PDF"):
            st.info("PDF Reader will be added in Step 2.")

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
    
