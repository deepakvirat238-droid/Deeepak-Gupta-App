import streamlit as st
import pdfplumber
import re
import time

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="MockTest Pro",
    page_icon="📝",
    layout="wide"
)

# =====================================
# SESSION STATE
# =====================================

defaults = {
    "pdf_loaded": False,
    "questions": [],
    "answer_key": {},
    "current_question": 0,
    "user_answers": {},
    "review_questions": [],
    "mode": "",
    "pdf_text": "",
    "answer_text": "",
    "timer_start": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""
<style>

.main{
    padding-top:10px;
}

.block-container{
    padding-top:1rem;
}

.stButton>button{
    width:100%;
    border-radius:10px;
    height:45px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# SIDEBAR
# =====================================

st.sidebar.title("📝 MockTest Pro")

menu = st.sidebar.radio(
    "Select",
    [
        "📂 Upload PDF",
        "🎯 Practice Mode",
        "📝 Mock Test",
        "📊 Result"
    ]
)

st.sidebar.divider()

if st.session_state.pdf_loaded:
    st.sidebar.success("✅ PDF Loaded")
else:
    st.sidebar.warning("❌ No PDF Loaded")

# =====================================
# HOME
# =====================================

if menu == "📂 Upload PDF":

    st.title("📂 Upload MCQ PDF")

    uploaded_pdf = st.file_uploader(
        "Choose PDF",
        type=["pdf"]
    )

    if uploaded_pdf:

        st.success(uploaded_pdf.name)

        if st.button("Read PDF"):

            st.info("PDF Reader will be added in Part 2.")

elif menu == "🎯 Practice Mode":

    st.title("🎯 Practice Mode")

    st.info("Please upload PDF first.")

elif menu == "📝 Mock Test":

    st.title("📝 Mock Test")

    st.info("Please upload PDF first.")

elif menu == "📊 Result":

    st.title("📊 Result")

    st.info("No Result Available.")
