import streamlit as st
import pdfplumber
import re

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="MockTest Pro v2",
    page_icon="📘",
    layout="wide"
)

# =====================================
# CSS
# =====================================

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
    border:1px solid #dddddd;
    border-radius:10px;
    padding:15px;
    margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# SESSION STATE
# =====================================

if "questions" not in st.session_state:
    st.session_state.questions = []

if "text" not in st.session_state:
    st.session_state.text = ""

# =====================================
# PDF TEXT EXTRACTOR
# =====================================

def extract_text_from_pdf(pdf_file):

    full_text = ""

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                full_text += page_text + "\n"

    return full_text

# =====================================
# QUESTION DETECTOR
# =====================================

def detect_questions(text):

    pattern = r"(Q\.?\s*\d+.*?)(?=Q\.?\s*\d+|$)"

    questions = re.findall(
        pattern,
        text,
        flags=re.DOTALL | re.IGNORECASE
    )

    return questions

# =====================================
# TITLE
# =====================================

st.title("📘 MockTest Pro v2")

st.write("Professional PDF to Quiz Converter")

st.divider()

uploaded_pdf = st.file_uploader(
    "📄 Upload PDF",
    type=["pdf"]
            )
# =====================================
# PDF READER
# =====================================

if uploaded_pdf:

    st.success(f"✅ {uploaded_pdf.name} uploaded successfully")

    if st.button("📥 Extract Text"):

        with st.spinner("Reading PDF..."):

            text = extract_text_from_pdf(uploaded_pdf)

            st.session_state.text = text

            st.session_state.questions = detect_questions(text)

# =====================================
# SHOW TEXT
# =====================================

if st.session_state.text:

    st.success("PDF Read Successfully")

    st.text_area(
        "Extracted Text",
        st.session_state.text,
        height=400
    )

# =====================================
# SHOW QUESTIONS
# =====================================

if st.session_state.questions:

    st.success(
        f"Questions Found : {len(st.session_state.questions)}"
    )

    st.divider()

    st.subheader("Detected Questions")

    for i, q in enumerate(
        st.session_state.questions,
        start=1
    ):

        with st.expander(f"Question {i}"):

            st.write(q)
    # =====================================
# PARSE QUESTION + OPTIONS
# =====================================

def parse_mcq(question_text):

    lines = [line.strip() for line in question_text.split("\n") if line.strip()]

    if not lines:
        return None

    question = ""
    options = []

    for line in lines:

        if re.match(r'^\(?[A-Da-d]\)|^[A-Da-d][\.\)]', line):
            options.append(line)
        else:
            if len(options) == 0:
                question += line + " "
            else:
                options[-1] += " " + line

    return {
        "question": question.strip(),
        "options": options
    }

# =====================================
# SHOW PARSED QUESTIONS
# =====================================

if st.session_state.questions:

    st.divider()

    st.subheader("Parsed MCQs")

    for i, raw_question in enumerate(st.session_state.questions[:20], start=1):

        mcq = parse_mcq(raw_question)

        if mcq:

            st.markdown(f"### Question {i}")

            st.write(mcq["question"])

            for option in mcq["options"]:
                st.write(option)

            st.divider()
