import streamlit as st
import pdfplumber
import re
import time
from datetime import timedelta

# Set up page configuration as the very first Streamlit command
st.set_page_config(
    page_title="MockTest Pro",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 1. CUSTOM CSS FOR TESTBOOK-STYLE UI
# ==========================================
def apply_custom_css():
    st.markdown("""
    <style>
        /* General App Theme Overrides */
        .main { background-color: #f8f9fa; }
        
        /* Metric and Card Designs */
        .metric-card {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            border-left: 5px solid #007bff;
            margin-bottom: 20px;
        }
        
        /* Question Palette Button Styling */
        .palette-btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 40px;
            height: 40px;
            margin: 5px;
            border-radius: 6px;
            font-weight: bold;
            font-size: 14px;
            cursor: pointer;
            border: 1px solid #ced4da;
            text-align: center;
        }
        .palette-current { border: 3px solid #007bff !important; box-shadow: 0 0 5px rgba(0,123,255,0.5); }
        .palette-answered { background-color: #28a745 !important; color: white !important; border-color: #28a745 !important; }
        .palette-unanswered { background-color: #dc3545 !important; color: white !important; border-color: #dc3545 !important; }
        .palette-review { background-color: #6f42c1 !important; color: white !important; border-color: #6f42c1 !important; }
        .palette-not-visited { background-color: #e9ecef !important; color: #495057 !important; }
        
        /* Custom alert/status elements */
        .status-box {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
            font-weight: 5px;
        }
        .status-correct { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .status-wrong { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        
        /* Sidebar styling enhancements */
        .sidebar .sidebar-content { background-color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. SESSION STATE INITIALIZATION
# ==========================================
def init_session_state():
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"
    if 'raw_text' not in st.session_state:
        st.session_state.raw_text = ""
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'answer_key' not in st.session_state:
        st.session_state.answer_key = {}
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    if 'test_start_time' not in st.session_state:
        st.session_state.test_start_time = None
    if 'test_duration_minutes' not in st.session_state:
        st.session_state.test_duration_minutes = 30
    if 'test_submitted' not in st.session_state:
        st.session_state.test_submitted = False
    if 'time_taken_seconds' not in st.session_state:
        st.session_state.time_taken_seconds = 0
    if 'visited_questions' not in st.session_state:
        st.session_state.visited_questions = set()

# ==========================================
# 3. INTELLIGENT PARSING ENGINE (REGICES)
# ==========================================
def extract_pdf_data(uploaded_file):
    """Extracts layout text and isolates the final page for the answer key."""
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            if len(pdf.pages) < 2:
                return None, None, "PDF must contain at least 2 pages (Questions + Answer Key)."
            
            # Extract content from question pages
            question_text = ""
            for page in pdf.pages[:-1]:
                text = page.extract_text()
                if text:
                    question_text += text + "\n"
            
            # Extract content from final page (Answer Key)
            last_page_text = pdf.pages[-1].extract_text()
            if not last_page_text:
                return None, None, "Could not extract text from the last page (Answer Key)."
                
            return question_text, last_page_text, None
    except Exception as e:
        return None, None, f"Corrupted or invalid PDF structure: {str(e)}"

def parse_answer_key(text):
    """
    Intelligently parses multiple structures of answer keys:
    1. A | 1-A | 1 : A | 1) A | Q1 A | 1. Ans(A)
    """
    answers = {}
    # Clean up string variants to normalize common splitters
    normalized = re.sub(r'(Ans[\(\ balance\)]*|ans[:\s]*)', '', text, flags=re.IGNORECASE)
    
    # Target common patterns: (Question Number Index) -> (Delimiter) -> (Option A-D/E)
    pattern = re.compile(r'(?:Q(?:uestion)?\s*)?(\d+)\s*[\.\-\)\:\s]*\s*([A-E])', re.IGNORECASE)
    matches = pattern.findall(normalized)
    
    for num, opt in matches:
        answers[int(num)] = opt.upper().strip()
        
    return answers

def parse_questions(text, answer_key):
    """Splits text body using strict regex hooks to separate questions and choices."""
    questions_list = []
    
    # Matches Q1., Q 1., 1., 1), Question 1
    q_split_pattern = r'(?:\n|\A)(?:Q(?:uestion)?\s*\.?\s*)?(\d+)[\.\)]\s+'
    
    parts = re.split(q_split_pattern, text)
    if len(parts) < 3:
        return []

    # Reconstruct extracted block iterations
    for i in range(1, len(parts), 2):
        q_num = int(parts[i])
        q_body = parts[i+1]
        
        # Regex to catch individual options dynamically (A., A), (A), a))
        opt_pattern = re.compile(
            r'(?:[\n\s]|\A)(?:[\(\[]?)([A-E])(?:[\.\)\]]|\s+)\s*([\s\S]*?)(?=(?:[\n\s]|\A)(?:[\(\[]?)[B-E](?:[\.\)\]]|\s+)|$)',
            re.IGNORECASE
        )
        
        opts_found = opt_pattern.findall(q_body)
        opts_dict = {'A': '', 'B': '', 'C': '', 'D': '', 'E': ''}
        
        # Clean question text context prior to option layouts
        first_opt_idx = re.search(r'(?:[\n\s]|\A)(?:[\(\[]?)[A-E](?:[\.\)\]]|\s+)', q_body, re.IGNORECASE)
        actual_question = q_body[:first_opt_idx.start()].strip() if first_opt_idx else q_body.strip()
        
        for letter, content in opts_found:
            opts_dict[letter.upper()] = content.strip()
            
        corr_ans = answer_key.get(q_num, "")
        
        questions_list.append({
            "question_number": q_num,
            "question": actual_question,
            "A": opts_dict['A'],
            "B": opts_dict['B'],
            "C": opts_dict['C'],
            "D": opts_dict['D'],
            "correct_answer": corr_ans,
            "user_answer": None,
            "review": False
        })
        
    return sorted(questions_list, key=lambda x: x["question_number"])

# ==========================================
# 4. VIEW RENDERING UTILITIES
# ==========================================
def render_question_palette():
    """Renders the standard Testbook Right Sidebar Grid Palette."""
    st.write("### Question Palette")
    cols = st.columns(5)
    
    for idx, q in enumerate(st.session_state.questions):
        q_num = q["question_number"]
        col_idx = idx % 5
        
        # Determine status styling tags
        status_class = "palette-not-visited"
        if idx in st.session_state.visited_questions:
            status_class = "palette-unanswered"
        if q["user_answer"] is not None:
            status_class = "palette-answered"
        if q["review"]:
            status_class = "palette-review"
        if idx == st.session_state.current_question_index:
            status_class += " palette-current"
            
        with cols[col_idx]:
            if st.button(f"{q_num}", key=f"btn_pal_{idx}"):
                st.session_state.current_question_index = idx
                st.session_state.visited_questions.add(idx)
                st.rerun()

def render_legend():
    """Renders palette descriptions cleanly."""
    st.markdown("""
    <div style='display: flex; flex-wrap: wrap; gap: 10px; margin-top: 15px; font-size:12px;'>
        <span style='padding: 4px 8px; border-radius:4px; background-color:#28a745; color:white;'>Answered</span>
        <span style='padding: 4px 8px; border-radius:4px; background-color:#dc3545; color:white;'>Unanswered</span>
        <span style='padding: 4px 8px; border-radius:4px; background-color:#6f42c1; color:white;'>Marked for Review</span>
        <span style='padding: 4px 8px; border-radius:4px; background-color:#e9ecef; color:#495057;'>Not Visited</span>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 5. CORE PAGES
# ==========================================
def render_home_page():
    st.title("🎯 Welcome to MockTest Pro")
    st.markdown("""
    Transform your flat MCQ Test PDF files into fully interactive, responsive **Testbook-style digital examination panels** instantly.
    
    ### ⚙️ How it works:
    1. **Upload your PDF**: Ensure your exam questions occupy the primary runtime pages and your answer sheet rests on the final page layout.
    2. **Review Configuration & Parsing**: System engines will partition standard configurations dynamically.
    3. **Select Practice or Mock Session Engine**: Manage evaluations either step-by-step or under standard countdown parameters.
    """)
    
    st.info("Navigate to the **Upload PDF** section via the sidebar menu to initialize processing components.")

def render_upload_page():
    st.title("📂 Document Ingestion Framework")
    uploaded_file = st.file_uploader("Upload MCQ Document Object (PDF Asset Format)", type=["pdf"])
    
    if uploaded_file is not None:
        with st.spinner("Processing structural parsing patterns..."):
            q_text, ans_text, err = extract_pdf_data(uploaded_file)
            
            if err:
                st.error(err)
                return
                
            ans_key = parse_answer_key(ans_text)
            if not ans_key:
                st.warning("Warning: Could not isolate target mappings from the detected final page matrix. Verify structural patterns manually.")
                
            parsed_qs = parse_questions(q_text, ans_key)
            
            if parsed_qs:
                st.session_state.questions = parsed_qs
                st.session_state.answer_key = ans_key
                st.session_state.visited_questions = {0}
                st.session_state.current_question_index = 0
                st.session_state.test_submitted = False
                
                st.success(f"Success! Parsed {len(parsed_qs)} questions with {len(ans_key)} matching answer nodes.")
                st.balloons()
            else:
                st.error("Failed to map text blocks into discrete question nodes. Verify structure match filters.")

def render_practice_page():
    st.title("💡 Real-time Practice Engine")
    
    if not st.session_state.questions:
        st.warning("No active evaluation schema loaded. Please process a valid file first via the **Upload PDF** engine.")
        return
        
    q_idx = st.session_state.current_question_index
    q = st.session_state.questions[q_idx]
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"### Question {q['question_number']}")
        st.markdown(f"**{q['question']}**")
        
        options = [f"A. {q['A']}", f"B. {q['B']}", f"C. {q['C']}", f"D. {q['D']}"]
        
        # Determine existing target index choice mapped
        current_sel = None
        if q["user_answer"]:
            current_sel = ["A", "B", "C", "D"].index(q["user_answer"])
            
        sel_opt = st.radio("Choose Option Select:", options, index=current_sel, key=f"prac_{q_idx}")
        
        if sel_opt:
            chosen_letter = sel_opt[0]
            st.session_state.questions[q_idx]["user_answer"] = chosen_letter
            
            # Instant Feedback Engine (Practice Mode Core Specification)
            if chosen_letter == q["correct_answer"]:
                st.markdown('<div class="status-box status-correct">✔ Correct Answer!</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="status-box status-wrong">✘ Wrong. Correct Answer is Option: <b>{q["correct_answer"]}</b></div>', unsafe_allow_html=True)
                
            st.markdown("> **Explanation/Reference Note:**\n> The structural processing pipeline isolated this verification from the parsed PDF schema key target block.")
            
        # Context Control Triggers Block
        st.write("---")
        btn_c1, btn_c2, btn_c3 = st.columns(3)
        with btn_c1:
            if st.button("Previous Question", disabled=(q_idx == 0)):
                st.session_state.current_question_index -= 1
                st.rerun()
        with btn_c2:
            if st.button("Clear Response"):
                st.session_state.questions[q_idx]["user_answer"] = None
                st.rerun()
        with btn_c3:
            if st.button("Next Question", disabled=(q_idx == len(st.session_state.questions) - 1)):
                st.session_state.current_question_index += 1
                st.session_state.visited_questions.add(st.session_state.current_question_index)
                st.rerun()
                
    with col2:
        render_question_palette()
        render_legend()

def render_mock_page():
    st.title("⏳ Simulated Examination Portal (Mock Mode)")
    
    if not st.session_state.questions:
        st.warning("No active evaluation schema loaded. Please process a valid file first via the **Upload PDF** engine.")
        return
        
    # Timer Infrastructure
    if st.session_state.test_start_time is None:
        st.session_state.test_start_time = time.time()
        
    elapsed = time.time() - st.session_state.test_start_time
    total_allowed = st.session_state.test_duration_minutes * 60
    remaining = max(0, total_allowed - elapsed)
    
    if remaining == 0 and not st.session_state.test_submitted:
        st.session_state.test_submitted = True
        st.session_state.time_taken_seconds = total_allowed
        st.error("Time limit reached. Your test configuration has been locked and submitted automatically.")
        st.session_state.current_page = "Result"
        st.rerun()

    # Upper Display Bar Layout
    t_col1, t_col2 = st.columns([3, 1])
    with t_col1:
        st.info("🚨 Mock Session Active: Answers remain hidden until final package block submission metrics are run.")
    with t_col2:
        st.metric("Time Remaining", str(timedelta(seconds=int(remaining))))
        
    if st.session_state.test_submitted:
        st.warning("This examination profile has closed submission pipelines. View results via the target menu matrix.")
        return

    q_idx = st.session_state.current_question_index
    q = st.session_state.questions[q_idx]
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"### Question {q['question_number']}")
        st.markdown(f"**{q['question']}**")
        
        options = [f"A. {q['A']}", f"B. {q['B']}", f"C. {q['C']}", f"D. {q['D']}"]
        
        current_sel = None
        if q["user_answer"]:
            current_sel = ["A", "B", "C", "D"].index(q["user_answer"])
            
        sel_opt = st.radio("Select choice vector:", options, index=current_sel, key=f"mock_{q_idx}")
        
        # Navigation Actions Blocks
        st.write("---")
        b1, b2, b3, b4 = st.columns(4)
        
        with b1:
            if st.button("Previous Page Block", disabled=(q_idx == 0)):
                st.session_state.current_question_index -= 1
                st.rerun()
        with b2:
            if st.button("Clear Response Node"):
                st.session_state.questions[q_idx]["user_answer"] = None
                st.rerun()
        with b3:
            if st.button("Mark For Review"):
                st.session_state.questions[q_idx]["review"] = True
                if sel_opt:
                    st.session_state.questions[q_idx]["user_answer"] = sel_opt[0]
                if q_idx < len(st.session_state.questions) - 1:
                    st.session_state.current_question_index += 1
                    st.session_state.visited_questions.add(st.session_state.current_question_index)
                st.rerun()
        with b4:
            if st.button("Save & Next"):
                if sel_opt:
                    st.session_state.questions[q_idx]["user_answer"] = sel_opt[0]
                st.session_state.questions[q_idx]["review"] = False
                if q_idx < len(st.session_state.questions) - 1:
                    st.session_state.current_question_index += 1
                    st.session_state.visited_questions.add(st.session_state.current_question_index)
                st.rerun()
                
        st.write("---")
        if st.button("Submit Assessment Portfolio", type="primary", use_container_width=True):
            st.session_state.test_submitted = True
            st.session_state.time_taken_seconds = elapsed
            st.session_value = "Result"
            st.success("Responses registered successfully.")
            st.rerun()
            
    with col2:
        render_question_palette()
        render_legend()

def render_result_page():
    st.title("📊 Analytical Assessment Report Metrics")
    
    if not St.session_state.questions:
        st.warning("No contextual metric history discovered to parse output matrices.")
        return
        
    if not st.session_state.test_submitted:
        st.info("Active processing schema details require submission profiles explicitly before finalizing reports.")
        return
        
    # Calculate performance tracking values
    total_q = len(st.session_state.questions)
    correct = 0
    wrong = 0
    skipped = 0
    
    for q in st.session_state.questions:
        if q["user_answer"] is None:
            skipped += 1
        elif q["user_answer"] == q["correct_answer"]:
            correct += 1
        else:
            wrong += 1
            
    accuracy = (correct / (correct + wrong) * 100) if (correct + wrong) > 0 else 0
    pct = (correct / total_q) * 100
    
    # Render layout metric display grids
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Evaluation Nodes", total_q)
    m2.metric("Verified Valid", correct)
    m3.metric("Incorrect Violations", wrong)
    m4.metric("Bypassed Steps", skipped)
    
    m5, m6, m7 = st.columns(3)
    m5.metric("System Precision Accuracy", f"{accuracy:.2f}%")
    m6.metric("Weighted Percentage Score", f"{pct:.2f}%")
    m7.metric("Calculated Elapsed Run Duration", str(timedelta(seconds=int(st.session_state.time_taken_seconds))))
    
    st.write("---")
    st.markdown("### 🏆 Performance Rank Analysis Matrix")
    st.info("Estimated Relative System Index Rank: **#1 / Placeholder Evaluation Core**")
    
    # Detailed Review Accordion Breakdown Block
    st.write("---")
    st.write("### Comprehensive Answer Matrix Breakdown & Diagnostics Review")
    for idx, q in enumerate(st.session_state.questions):
        with st.expander(f"Question {q['question_number']}: Evaluation State Profile Verification"):
            st.markdown(f"**Question Structure Body Content:** {q['question']}")
            st.write(f"A. {q['A']}")
            st.write(f"B. {q['B']}")
            st.write(f"C. {q['C']}")
            st.write(f"D. {q['D']}")
            st.write(f"**Target System True Reference Matrix Key:** {q['correct_answer']}")
            st.write(f"**User Choice Selection Matrix Node Value:** {q['user_answer']}")

def render_settings_page():
    st.title("⚙️ Engine Architecture Configurations")
    st.session_state.test_duration_minutes = st.number_input(
        "Default Allocation Countdown Span (Minutes Window Parameter)", 
        min_value=5, max_value=180, value=st.session_state.test_duration_minutes
    )
    st.success("Runtime runtime variables successfully modified down state channels.")

# ==========================================
# 6. ROUTER & ENTRY POINT
# ==========================================
def main():
    apply_custom_css()
    init_session_state()
    
    # Sidebar Routing Architecture Configuration
    st.sidebar.title("💎 MockTest Pro Dashboard")
    page_selection = st.sidebar.radio(
        "Navigation Portal Route Selector Panel:",
        ["Home", "Upload PDF", "Practice Mode", "Mock Test", "Result", "Settings"]
    )
    
    st.session_state.current_page = page_selection
    
    if st.session_state.current_page == "Home":
        render_home_page()
    elif st.session_state.current_page == "Upload PDF":
        render_upload_page()
    elif st.session_state.current_page == "Practice Mode":
        render_practice_page()
    elif st.session_state.current_page == "Mock Test":
        render_mock_page()
    elif st.session_state.current_page == "Result":
        render_result_page()
    elif st.session_state.current_page == "Settings":
        render_settings_page()

if __name__ == "__main__":
    main()

    
