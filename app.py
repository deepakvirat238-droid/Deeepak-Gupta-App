import streamlit as st
import pdfplumber
import re
import time
from datetime import timedelta

# Streamlit configurations for matching structural dashboard metrics
st.set_page_config(
    page_title="MockTest Pro — Premium CBT Examination Suite",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 1. ACTUAL TESTBOOK / TCS iON CBT PANE CSS
# ==========================================
def apply_testbook_theme():
    st.markdown("""
    <style>
        /* Base Styling & Font Set */
        .main { background-color: #f4f7f9 !important; padding-top: 0px !important; }
        
        /* TCS iON Examination Top Banner */
        .cbt-top-bar {
            background-color: #4682B4;
            color: white;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 3px solid #315b7d;
            margin-bottom: 15px;
        }
        
        /* Section Header Layout */
        .section-tab {
            background-color: #e7f1f9;
            color: #1e4f75;
            padding: 8px 20px;
            font-weight: bold;
            border-top: 3px solid #4682B4;
            display: inline-block;
            margin-bottom: 10px;
            border-radius: 4px 4px 0 0;
        }

        /* Question Canvas View Box */
        .q-container {
            background-color: #ffffff;
            border: 1px solid #cfdadf;
            padding: 20px;
            min-height: 250px;
            margin-bottom: 15px;
            border-radius: 4px;
        }
        
        .q-number-title {
            font-size: 16px;
            font-weight: bold;
            color: #333;
            border-bottom: 1px solid #eaeaea;
            padding-bottom: 8px;
            margin-bottom: 12px;
        }
        
        /* Sidebar Identity Panel Mock */
        .profile-box {
            background-color: #ffffff;
            border: 1px solid #cfdadf;
            padding: 10px;
            text-align: center;
            margin-bottom: 15px;
            border-radius: 4px;
        }
        
        /* Real Palette Status Tags styling mapping */
        .status-summary-table {
            width: 100%;
            font-size: 12px;
            margin-bottom: 15px;
            border-collapse: collapse;
        }
        .status-summary-table td { padding: 4px 2px; }
        
        /* Custom Native Button Overrides for Testbook Colors */
        div.stButton > button {
            border-radius: 2px !important;
            font-size: 13px !important;
        }
        
        /* Dynamic Indicator Badges */
        .feedback-box {
            border-radius: 4px;
            padding: 15px;
            margin: 15px 0;
            font-weight: 500;
        }
        .feedback-success { background-color: #e8f5e9; color: #2e7d32; border-left: 5px solid #4caf50; }
        .feedback-danger { background-color: #ffebee; color: #c62828; border-left: 5px solid #f44336; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. SESSION STATE MANAGEMENT
# ==========================================
def init_session_state():
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'answer_key' not in st.session_state:
        st.session_state.answer_key = {}
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    if 'test_start_time' not in st.session_state:
        st.session_state.test_start_time = None
    if 'test_duration_minutes' not in st.session_state:
        st.session_state.test_duration_minutes = 60
    if 'test_submitted' not in st.session_state:
        st.session_state.test_submitted = False
    if 'time_taken_seconds' not in st.session_state:
        st.session_state.time_taken_seconds = 0
    if 'visited_questions' not in st.session_state:
        st.session_state.visited_questions = set()

# ==========================================
# 3. ADVANCED HIGH-ACCURACY PARSING ENGINE
# ==========================================
def extract_pdf_data(uploaded_file):
    """Robust raw layout reader isolating question block sheets from target metrics keys."""
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            total_pages = len(pdf.pages)
            if total_pages < 2:
                return None, None, "PDF requires multiple pages to process structurally (Questions + Answer Key)."
            
            question_text = ""
            for page in pdf.pages[:-1]:
                text = page.extract_text()
                if text:
                    question_text += text + "\n"
            
            last_page_text = pdf.pages[-1].extract_text()
            return question_text, last_page_text, None
    except Exception as e:
        return None, None, f"Parsing exception error discovered: {str(e)}"

def parse_answer_key(text):
    """
    High-accuracy key mapper targeting multiple formats:
    1.B | 1. B | 1-B | 1)B | Q1 B
    """
    answers = {}
    if not text:
        return answers
    
    # Pre-clean known layout noise headers
    clean_text = re.sub(r'(ANSWER\s*KEY|Ans[:\s]*|Answer\s*Sheet)', '', text, flags=re.IGNORECASE)
    
    # Matches digit index boundaries mapping straight to options selection matrices
    pattern = re.compile(r'(?:Q(?:uestion)?\s*)?(\d+)\s*[\.\-\)\:\s]*\s*([A-E])', re.IGNORECASE)
    matches = pattern.findall(clean_text)
    
    for num, option in matches:
        answers[int(num)] = option.upper().strip()
    return answers

def parse_questions(text, answer_key):
    """
    High-accuracy multi-line parser. Detects option delimiters smoothly
    even if spaces/periods are completely missing (e.g. 'A Mars', 'B venus').
    """
    questions_list = []
    if not text:
        return questions_list

    # Splits cleanly on standard variations of Question markers: Q1., Q 1., 1., 1), Question 1
    q_split_pattern = r'(?:\n|\A)(?:Q(?:uestion)?\s*\.?\s*)?(\d+)[\.\)]\s+'
    parts = re.split(q_split_pattern, text)
    
    if len(parts) < 3:
        return questions_list

    for i in range(1, len(parts), 2):
        q_num = int(parts[i])
        q_body = parts[i+1]
        
        # Super dynamic regex catching standard Option groups with space/non-dot lookaheads
        opt_pattern = re.compile(
            r'(?:[\n\s]|\A)(?:[\(\[]?)([A-E])(?:[\.\)\]]|\s+)\s*([\s\S]*?)(?=(?:[\n\s]|\A)(?:[\(\[]?)[B-E](?:[\.\)\]]|\s+)|$)',
            re.IGNORECASE
        )
        
        opts_found = opt_pattern.findall(q_body)
        opts_dict = {'A': 'Option A', 'B': 'Option B', 'C': 'Option C', 'D': 'Option D', 'E': ''}
        
        # Calculate start boundaries to securely isolate the core base prompt question string text block
        first_opt_idx = re.search(r'(?:[\n\s]|\A)(?:[\(\[]?)[A-E](?:[\.\)\]]|\s+)', q_body, re.IGNORECASE)
        actual_question = q_body[:first_opt_idx.start()].strip() if first_opt_idx else q_body.strip()
        
        for letter, content in opts_found:
            cleaned_content = content.strip()
            # Clean up line break garbage formatting leftovers
            cleaned_content = re.sub(r'\s+', ' ', cleaned_content)
            opts_dict[letter.upper()] = cleaned_content
            
        questions_list.append({
            "question_number": q_num,
            "question": actual_question,
            "A": opts_dict['A'],
            "B": opts_dict['B'],
            "C": opts_dict['C'],
            "D": opts_dict['D'],
            "correct_answer": answer_key.get(q_num, "A"),  # Defaults safely if missing mapping node
            "user_answer": None,
            "review": False
        })
        
    return sorted(questions_list, key=lambda x: x["question_number"])

# ==========================================
# 4. COMPACT NAV PALETTE ENGINE
# ==========================================
def render_sidebar_palette():
    answered = sum(1 for q in st.session_state.questions if q["user_answer"] is not None and not q["review"])
    marked_review = sum(1 for q in st.session_state.questions if q["review"])
    not_visited = len(st.session_state.questions) - len(st.session_state.visited_questions)
    not_answered = len(st.session_state.questions) - answered - marked_review - not_visited

    st.markdown(f"""
    <div class="profile-box">
        <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" width="55" style="margin-bottom:5px;"><br/>
        <b>Kanchan Kumari</b><br/><span style="font-size:11px;color:grey;">Roll No: 2026045</span>
    </div>
    <table class="status-summary-table">
        <tr>
            <td><span style="background:#28a745;color:white;padding:2px 6px;font-weight:bold;border-radius:2px;">{answered}</span> Answered</td>
            <td><span style="background:#dc3545;color:white;padding:2px 6px;font-weight:bold;border-radius:2px;">{not_answered}</span> Not Answered</td>
        </tr>
        <tr>
            <td><span style="background:#6f42c1;color:white;padding:2px 6px;font-weight:bold;border-radius:2px;">{marked_review}</span> Marked Review</td>
            <td><span style="background:#e9ecef;color:#495057;padding:2px 6px;font-weight:bold;border-radius:2px;">{not_visited}</span> Not Visited</td>
        </tr>
    </table>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.write("🎰 **Question Palette Grid:**")
    
    total_qs = len(st.session_state.questions)
    grid_cols = 4
    for i in range(0, total_qs, grid_cols):
        cols = st.columns(grid_cols)
        for j in range(grid_cols):
            idx = i + j
            if idx < total_qs:
                q = st.session_state.questions[idx]
                q_num = q["question_number"]
                
                status_symbol = "⬜"
                if idx == st.session_state.current_question_index:
                    status_symbol = "🔵"
                elif q["review"]:
                    status_symbol = "🟣"
                elif q["user_answer"] is not None:
                    status_symbol = "🟢"
                elif idx in st.session_state.visited_questions:
                    status_symbol = "🔴"
                    
                with cols[j]:
                    if st.button(f"{status_symbol}{q_num}", key=f"cbt_pal_{idx}", use_container_width=True):
                        st.session_state.current_question_index = idx
                        st.session_state.visited_questions.add(idx)
                        st.rerun()

# ==========================================
# 5. CORE WORKFLOW INTEGRATION ROUTERS
# ==========================================
def render_home_page():
    st.title("🎯 MockTest Pro — Premium Exam Portal")
    st.markdown("""
    Welcome to India's most accurate and authentic CBT simulation desk framework.
    
    ### 🚀 High Accuracy Architecture:
    * **Spatial Parsing Architecture**: Captures flat spacing choice configurations like `A Mars` without throwing breaking text faults.
    * **TCS iON Responsive Matrix Panel**: Replicates standard Testbook layout alignments perfectly.
    * **Integrated Dual Run Engine Modules**: Switch instantly to fit custom execution routines.
    """)
    st.info("Please navigate to the **Upload PDF** section using the left-hand navigation menu matrix.")

def render_upload_page():
    st.subheader("📂 Document Asset Framework Ingestion Center")
    uploaded_file = st.file_uploader("Upload MCQ Document Data Blueprint (PDF Asset)", type=["pdf"])
    
    if uploaded_file is not None:
        with st.spinner("Analyzing structural layouts and tracking options grids..."):
            q_text, ans_text, err = extract_pdf_data(uploaded_file)
            if err:
                st.error(err)
                return
            ans_key = parse_answer_key(ans_text)
            parsed_qs = parse_questions(q_text, ans_key)
            
            if parsed_qs:
                st.session_state.questions = parsed_qs
                st.session_state.answer_key = ans_key
                st.session_state.visited_questions = {0}
                st.session_state.current_question_index = 0
                st.session_state.test_submitted = False
                st.session_state.test_start_time = None
                st.success(f"Processing Complete! Successfully mapped {len(parsed_qs)} evaluation nodes inside localized memory spaces.")
            else:
                st.error("Failed to map separate questions. Ensure your asset contains sequential digit numbering markers.")

def render_practice_page():
    if not st.session_state.questions:
        st.warning("No functional datasets loaded. Ingest an item portfolio first using the **Upload PDF** engine route.")
        return
        
    q_idx = st.session_state.current_question_index
    q = st.session_state.questions[q_idx]
    
    st.markdown('<div class="section-tab">Section Workspace: General Performance Booster Practice</div>', unsafe_allow_html=True)
    
    col_left, col_right = st.columns([3, 1])
    
    with col_left:
        st.markdown(f"""
        <div class="q-container">
            <div class="q-number-title">Question No. {q['question_number']}</div>
            <p style='font-size:15px;'><b>{q['question']}</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        opts = [f"A. {q['A']}", f"B. {q['B']}", f"C. {q['C']}", f"D. {q['D']}"]
        curr_sel = ["A", "B", "C", "D"].index(q["user_answer"]) if q["user_answer"] else None
        
        selected_option = st.radio("Choose option select input node variant:", opts, index=curr_sel, key=f"p_rad_{q_idx}")
        
        if selected_option:
            ans_char = selected_option[0]
            st.session_state.questions[q_idx]["user_answer"] = ans_char
            if ans_char == q["correct_answer"]:
                st.markdown('<div class="feedback-box feedback-success">✔ Correct Selection Verified!</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="feedback-box feedback-danger">✘ Incorrect choice coordinate. Core target key value is: <b>Option {q["correct_answer"]}</b></div>', unsafe_allow_html=True)
                
        st.write("---")
        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("⬅ Previous Item", disabled=(q_idx == 0), use_container_width=True, key="prac_prev"):
                st.session_state.current_question_index -= 1
                st.rerun()
        with b2:
            if st.button("🧹 Reset Target Node", use_container_width=True, key="prac_clear"):
                st.session_state.questions[q_idx]["user_answer"] = None
                st.rerun()
        with b3:
            if st.button("Save & Forward ➡", disabled=(q_idx == len(st.session_state.questions) - 1), use_container_width=True, key="prac_next"):
                st.session_state.current_question_index += 1
                st.session_state.visited_questions.add(st.session_state.current_question_index)
                st.rerun()

    with col_right:
        render_sidebar_palette()

def render_mock_page():
    if not st.session_state.questions:
        st.warning("No functional datasets loaded. Ingest an item portfolio first using the **Upload PDF** engine route.")
        return
        
    if st.session_state.test_start_time is None:
        st.session_state.test_start_time = time.time()
        
    elapsed = time.time() - st.session_state.test_start_time
    allowed_sec = st.session_state.test_duration_minutes * 60
    rem_sec = max(0, allowed_sec - elapsed)
    
    if rem_sec == 0 and not st.session_state.test_submitted:
        st.session_state.test_submitted = True
        st.session_state.time_taken_seconds = allowed_sec
        st.session_state.current_page = "Result"
        st.rerun()
        
    # Top Information Bar Injection Replication
    st.markdown(f"""
    <div class="cbt-top-bar">
        <span>📋 Online Examination System Mock Core Workspace Panel</span>
        <span>⏳ Countdown Running Remaining Clock: {str(timedelta(seconds=int(rem_sec)))}</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-tab">Main Target major Paper Testing Evaluation Section</div>', unsafe_allow_html=True)
    
    q_idx = st.session_state.current_question_index
    q = st.session_state.questions[q_idx]
    
    col_left, col_right = st.columns([3, 1])
    
    with col_left:
        st.markdown(f"""
        <div class="q-container">
            <div class="q-number-title">Question No. {q['question_number']}</div>
            <p style='font-size:15px;'><b>{q['question']}</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        opts = [f"A. {q['A']}", f"B. {q['B']}", f"C. {q['C']}", f"D. {q['D']}"]
        curr_sel = ["A", "B", "C", "D"].index(q["user_answer"]) if q["user_answer"] else None
        
        selected_option = st.radio("Choose Option Select:", opts, index=curr_sel, key=f"m_rad_{q_idx}")
        
        st.write("---")
        # Standard Action Configuration Matrix Row Placement Layout
        act_c1, act_c2, act_c3, act_c4 = st.columns(4)
        
        with act_c1:
            if st.button("🟣 Mark for Review & Next", use_container_width=True, key="mock_review"):
                st.session_state.questions[q_idx]["review"] = True
                if selected_option:
                    st.session_state.questions[q_idx]["user_answer"] = selected_option[0]
                if q_idx < len(st.session_state.questions) - 1:
                    st.session_state.current_question_index += 1
                    st.session_state.visited_questions.add(st.session_state.current_question_index)
                st.rerun()
                
        with act_c2:
            if st.button("🧹 Clear Response", use_container_width=True, key="mock_clear"):
                st.session_state.questions[q_idx]["user_answer"] = None
                st.session_state.questions[q_idx]["review"] = False
                st.rerun()
                
        with act_c3:
            if st.button("💾 Save & Next ➡", type="primary", use_container_width=True, key="mock_next"):
                if selected_option:
                    st.session_state.questions[q_idx]["user_answer"] = selected_option[0]
                st.session_state.questions[q_idx]["review"] = False
                if q_idx < len(st.session_state.questions) - 1:
                    st.session_state.current_question_index += 1
                    st.session_state.visited_questions.add(st.session_state.current_question_index)
                st.rerun()
                
        with act_c4:
            if st.button("🛑 Submit Evaluation Package", use_container_width=True, key="mock_submit"):
                st.session_state.test_submitted = True
                st.session_state.time_taken_seconds = elapsed
                st.session_state.current_page = "Result"
                st.rerun()

    with col_right:
        render_sidebar_palette()

def render_result_page():
    st.subheader("📊 Performance Analytics Dashboard Studio")
    
    if not st.session_state.questions or not st.session_state.test_submitted:
        st.warning("No comprehensive test submission log context discovered to compute tracking metrics.")
        return
        
    total_q = len(st.session_state.questions)
    correct, wrong, skipped = 0, 0, 0
    
    for q in st.session_state.questions:
        if q["user_answer"] is None:
            skipped += 1
        elif q["user_answer"] == q["correct_answer"]:
            correct += 1
        else:
            wrong += 1
            
    accuracy = (correct / (correct + wrong) * 100) if (correct + wrong) > 0 else 0
    
    r_c1, r_c2, r_c3 = st.columns(3)
    r_c1.metric("Total Extracted Items", total_q)
    r_c2.metric("Verified Valid Core Hits", correct)
    mismatches = r_c3.metric("Error Variance Misses", wrong)
    
    r_c4, r_c5 = st.columns(2)
    r_c4.metric("Engine Precision Index Score", f"{accuracy:.2f}%")
    r_c5.metric("Total Processing Runtime Allocated", str(timedelta(seconds=int(st.session_state.time_taken_seconds))))
    
    st.write("---")
    st.markdown("### 🔍 Item-by-Item Question & Key Matrix Diagnostic Audit Log")
    for idx, q in enumerate(st.session_state.questions):
        with st.expander(f"Question Log Matrix Target Element Entry Record Value #{q['question_number']}"):
            st.markdown(f"**Question Text Node Context Content:** {q['question']}")
            st.write(f"A. {q['A']}")
            st.write(f"B. {q['B']}")
            st.write(f"C. {q['C']}")
            st.write(f"D. {q['D']}")
            st.info(f"Verified System Reference Target Key Parameter: Option {q['correct_answer']} | Active Registration Selection Log Target Node Value: {q['user_answer'] if q['user_answer'] else 'Skipped/No Response Input Logged'}")

def render_settings_page():
    st.subheader("⚙️ System Architecture Configuration Controls")
    st.session_state.test_duration_minutes = st.number_input(
        "Define Session Allocation Parameters Counter Length (Minutes Duration Scale Layout Boundary Loop):",
        min_value=5, max_value=200, value=st.session_state.test_duration_minutes
    )
    st.success("Target environment global settings parameters altered successfully.")

# ==========================================
# 6. APP MAIN CONTROLLER ENTRY POINT
# ==========================================
def main():
    apply_testbook_theme()
    init_session_state()
    
    st.sidebar.markdown("<h2 style='text-align:center; color:#4682B4;'>📝 MockTest Pro</h2>", unsafe_allow_html=True)
    st.sidebar.write("---")
    
    navigation_panel_matrix_routes = st.sidebar.radio(
        "Navigation Portal Route Selector Panel Menu Hub:",
        ["Home", "Upload PDF", "Practice Mode", "Mock Test", "Result", "Settings"]
    )
    
    st.session_state.current_page = navigation_panel_matrix_routes
    
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
