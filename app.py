import streamlit as st
import pdfplumber
import re

# --------------------------
# PAGE CONFIG
# --------------------------

st.set_page_config(
    page_title="MockTest Pro v2",
    page_icon="📘",
    layout="wide"
)

# --------------------------
# CSS
# --------------------------

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

</style>
""", unsafe_allow_html=True)

# --------------------------
# SESSION
# --------------------------

if "questions" not in st.session_state:
    st.session_state.questions=[]

# --------------------------
# PDF TEXT
# --------------------------

def extract_text_from_pdf(pdf):

    text=""

    with pdfplumber.open(pdf) as pdf_file:

        for page in pdf_file.pages:

            page_text=page.extract_text()

            if page_text:

                text+=page_text+"\n"

    return text

# --------------------------
# QUESTION DETECTOR
# --------------------------

def detect_questions(text):

    pattern=r'(Q\.?\d+.*?)(?=Q\.?\d+|$)'

    questions=re.findall(
        pattern,
        text,
        flags=re.DOTALL|re.IGNORECASE
    )

    return questions

# --------------------------
# TITLE
# --------------------------

st.title("📘 MockTest Pro v2")

st.write("Professional PDF to Quiz Converter")

st.divider()

uploaded_pdf=st.file_uploader(
    "📄 Upload PDF",
    type=["pdf"]
)

if uploaded_pdf:

    st.success(f"✅ {uploaded_pdf.name} uploaded successfully")

    if st.button("📥 Extract Text"):

        with st.spinner("Reading PDF..."):

            text=extract_text_from_pdf(uploaded_pdf)

        st.success("PDF Read Successfully")

        st.text_area(
            "Extracted Text",
            text,
            height=400
                    questions = detect_questions(text)

        st.success(f"Questions Found: {len(questions)}")

        st.divider()

        for i, q in enumerate(questions[:10], start=1):

            with st.expander(f"Question {i}"):

                st.write(q)

        st.session_state.questions = questions

if st.session_state.questions:

    st.divider()

    st.subheader("📋 Extracted Question List")

    for i, q in enumerate(st.session_state.questions, start=1):

        st.write(f"**Q{i}.** {q[:120]}...")
    )
