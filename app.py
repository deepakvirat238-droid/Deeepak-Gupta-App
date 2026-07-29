import streamlit as st
import pandas as pd
import pdfplumber
import re
import io
import json
import time
from datetime import datetime
from fpdf import FPDF

st.set_page_config(
    page_title="MockTest Pro v2",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>

.main{
    padding:15px;
}

.stButton>button{
    width:100%;
    border-radius:10px;
    height:45px;
    font-weight:bold;
}

.question-box{
    padding:15px;
    border-radius:12px;
    border:1px solid #ddd;
    margin-bottom:15px;
}

.palette-btn{
    width:40px;
    height:40px;
    border-radius:50%;
    margin:2px;
}

</style>
""", unsafe_allow_html=True)
if "questions" not in st.session_state:
    st.session_state.questions=[]

if "current_question" not in st.session_state:
    st.session_state.current_question=0

if "answers" not in st.session_state:
    st.session_state.answers={}

if "review" not in st.session_state:
    st.session_state.review=[]

if "visited" not in st.session_state:
    st.session_state.visited=[]

if "timer" not in st.session_state:
    st.session_state.timer=0
