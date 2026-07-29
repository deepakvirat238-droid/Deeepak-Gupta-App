import streamlit as st
import pdfplumber
import re
import pandas as pd
from fpdf import FPDF

# ------------------------
# Page Config
# ------------------------

st.set_page_config(
    page_title="MockTest Pro v2",
    page_icon="📘",
    layout="wide"
)

# ------------------------
# CSS
# ------------------------

st.markdown("""
<style>

.main{
    padding:20px;
}

.stButton>button{
    width:100%;
    height:45px;
    border-radius:10px;
    font-weight:bold;
}

.question-box{
    border:1px solid #ddd;
    border-radius:10px;
    padding:15px;
    margin-bottom:15px;
}

</style>
""", unsafe_allow_html=True)

# ------------------------
# Session State
# ------------------------

if "questions" not in st.session_state:
    st.session_state.questions=[]

if "answers" not in st.session_state:
    st.session_state.answers={}

if "current_question" not in st.session_state:
    st.session_state.current_question=0

# ------------------------
# PDF Text Extractor
# ------------------------

def extract_text_from_pdf(pdf):

    full_text=""

    with pdfplumber.open(pdf) as pdf_file:

        for page in pdf_file.pages:

            txt=page.extract_text()

            if txt:
                full_text+=txt+"\n"

    return full_text

# ------------------------
# Title
# ------------------------

st.title("📘 MockTest Pro v2")

st.write("Professional PDF to Quiz Converter")
