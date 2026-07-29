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
# =====================================
# QUIZ MODE
# =====================================

if st.session_state.questions:

    st.divider()
    st.header("📝 Quiz Mode")

    score = 0

    for i, raw_question in enumerate(st.session_state.questions):

        mcq = parse_mcq(raw_question)

        if not mcq:
            continue

        st.markdown(f"### Q{i+1}")

        st.write(mcq["question"])

        if len(mcq["options"]) >= 2:

            st.radio(
                "Choose your answer",
                mcq["options"],
                key=f"quiz_{i}"
            )

    st.button("Submit Quiz")
    # =====================================
# ANSWER KEY
# =====================================

if "answers" not in st.session_state:
    st.session_state.answers = {}

st.divider()
st.header("📋 Answer Key")

st.info(
    "Enter the correct option for each question "
    "(A/B/C/D)."
)

for i, raw_question in enumerate(st.session_state.questions):

    st.session_state.answers[i] = st.selectbox(
        f"Correct Answer - Q{i+1}",
        ["A", "B", "C", "D"],
        key=f"answer_{i}"
    )

# =====================================
# RESULT
# =====================================

if st.button("✅ Calculate Score"):

    total = len(st.session_state.questions)
    score = 0

    for i in range(total):

        user = st.session_state.get(f"quiz_{i}")

        correct = st.session_state.answers[i]

        if user:

            if user.upper().startswith(correct):
                score += 1

    st.divider()

    st.success(f"Score : {score}/{total}")

    if total > 0:

        percentage = score * 100 / total

        st.write(f"Percentage : {percentage:.2f}%")

        if percentage >= 90:
            st.balloons()
            st.success("Excellent!")

        elif percentage >= 75:
            st.success("Very Good!")

        elif percentage >= 50:
            st.warning("Good, keep practicing.")

        else:
            st.error("Needs Improvement.")
# =====================================
# AUTO ANSWER KEY DETECTION
# =====================================

def detect_answer_key(text):

    answers = {}

    patterns = [

        r'(\d+)\s*[-:]\s*([ABCD])',

        r'(\d+)\.\s*([ABCD])',

        r'Q\.?\s*(\d+)\s*[-:]\s*([ABCD])'

    ]

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        if matches:

            for qno, ans in matches:

                answers[int(qno)] = ans.upper()

            break

    return answers

# =====================================
# SHOW DETECTED ANSWERS
# =====================================

if st.session_state.text:

    auto_answers = detect_answer_key(
        st.session_state.text
    )

    if auto_answers:

        st.divider()

        st.header("✅ Auto Detected Answer Key")

        st.write(auto_answers)

    else:

        st.info(
            "No Answer Key detected in PDF."
    )
