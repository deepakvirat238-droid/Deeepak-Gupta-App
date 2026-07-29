import streamlit as st
import pdfplumber
import re
import time
from datetime import timedelta

# Tablet aur Mobile compatibility ke liye layout setting adjust ki gyi hai
st.set_page_config(
    page_title="MockTest Pro — Tablet Responsive CBT Suite",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 1. TABLET & MOBILE RESPONSIVE CSS
# ==========================================
def apply_testbook_theme():
    st.markdown("""
    <style>
        /* Base Styling & Font Set */
        .main { background-color: #f4f7f9 !important; padding-top: 0px !important; }
        
        /* TCS iON Top Banner - Responsive for Tablets */
        .cbt-top-bar {
            background-color: #4682B4;
            color: white;
            padding: 10px 15px;
            font-size: 14px;
            font-weight: bold;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 3px solid #315b7d;
            margin-bottom: 12px;
            flex-wrap: wrap;
            gap: 10px;
        }
        
        /* Section Header Layout */
        .section-tab {
            background-color: #e7f1f9;
            color: #1e4f75;
            padding: 6px 15px;
            font-weight: bold;
            border-top: 3px solid #4682B4;
            display: inline-block;
            margin-bottom: 10px;
            border-radius: 4px 4px 0 0;
            font-size: 13px;
        }

        /* Question Canvas View Box (Tablet Optimization) */
        .q-container {
            background-color: #ffffff;
            border: 1px solid #cfdadf;
            padding: 15px;
            min-height: 200px;
            margin-bottom: 12px;
            border-radius: 4px;
            width: 100%;
            box-sizing: border-box;
        }
        
        .q-number-title {
            font-size: 15px;
            font-weight: bold;
            color: #333;
            border-bottom: 1px solid #eaeaea;
            padding-bottom: 6px;
            margin-bottom: 10px;
        }
        
        /* Sidebar Identity Panel Mock */
        .profile-box {
            background-color: #ffffff;
            border: 1px solid #cfdadf;
            padding: 10px;
            text-align: center;
            margin-bottom: 12px;
            border-radius: 4px;
        }
        
        /* Palette Status Summary Grid */
        .status-summary-table {
            width: 100%;
            font-size: 11px;
            margin-bottom: 12px;
            border-collapse: collapse;
        }
        .status-summary-table td { padding: 3px 2px; }
        
        /* Tablet Friendly Buttons Override */
        div.stButton > button {
            border-radius: 2px !important;
            font-size: 12px !important;
            padding: 6px 10px !important;
        }
        
        /* Feedback Alert Layouts */
        .feedback-box {
            border-radius: 4px;
            padding: 12px;
            margin: 12px 0;
            font-weight: 500;
            font-size: 13px;
        }
        .feedback-success { background-color: #e8f5e9; color: #2e7d32; border-left: 5px solid #4caf50; }
        .feedback-danger { background-color: #ffebee; color: #c62828; border-left: 5px solid #f44336; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. SESSION STATE ARTIFACT MANAGEMENT
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
# 3. ROBUST PARSING ENGINE
# ==========================================
def extract_pdf_data(uploaded_file):
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            total_pages = len(pdf.pages)
            if total_pages < 2:
                return None, None, "PDF requires multiple pages (Questions + Answer Key)."
            
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
    answers = {}
    if not text:
        return answers
    clean_text = re.sub(r'(ANSWER\s*KEY|Ans[:\s]*|Answer\s*Sheet)', '', text, flags=re.IGNORECASE)
    pattern = re.compile(r'(?:Q(?:uestion)?\s*)?(\d+)\s*[\.\-\)\:\s]*\s*([A-E])', re.IGNORECASE)
    matches = pattern.findall(clean_text)
    for num, option in matches:
        answers[int(num)] = option.upper().strip()
    return answers

def parse_questions(text, answer_key):
    questions_list = []
    if not text:
        return questions_list

    q_split_pattern = r'(?:\n|\A)(?:Q(?:uestion)?\s*\.?\s*)?(\d+)[\.\)]\s+'
    parts = re.split(q_split_pattern, text)
    
    if len(parts) < 3:
        return questions_list

    for i in range(1, len(parts), 2):
        q_num = int(parts[i])
        q_body = parts[i+1]
        
        opt_pattern = re.compile(
            r'(?:[\n\s]|\A)(?:[\(\[]?)([A-E])(?:[\.\)\]]|\s+)\s*([\s\S]*?)(?=(?:[\n\s]|\A)(?:[\(\[]?)[B-E](?:[\.\)\]]|\s+)|$)',
            re.IGNORECASE
        )
        
        opts_found = opt_pattern.findall(q_body)
        opts_dict = {'A': 'Option A', 'B': 'Option B', 'C': 'Option C', 'D': 'Option D', 'E': ''}
        
        first_opt_idx = re.search(r'(?:[\n\s]|\A)(?:[\(\[]?)[A-E](?:[\.\)\]]|\s+)', q_body, re.IGNORECASE)
        actual_question = q_body[:first_opt_idx.start()].strip() if first_opt_idx else q_body.strip()
        
        for letter, content in opts_found:
            cleaned_content = re.sub(r'\s+', ' ', content.strip())
            opts_dict[letter.upper()] = cleaned_content
            
        questions_list.append({
            "question_number": q_num,
            "question": actual_question,
            "A": opts_dict['A'],
            "B": opts_dict['B'],
            "C": opts_dict['C'],
            "D": opts_dict['D'],
            "correct_answer": answer_key.get(q_num, "A"),
            "user_answer": None,
            "review": False
        })
        
    return sorted(questions_list, key=lambda x: x["question_number"])

# ==========================================
# 4. FIXED PALETTE LAYOUT (TABLET DRIVEN)
# ==========================================
def render_exam_palette():
    """Renders the question palette inside a unified layout block container."""
    answered = sum(1 for q in st.session_state.questions if q["user_answer"] is not None and not q["review"])
    marked_review = sum(1 for q in st.session_state.questions if q["review"])
    not_visited = len(st.session_state.questions) - len(st.session_state.visited_questions)
    not_answered = len(st.session_state.questions) - answered - marked_review - not_visited

    st.markdown(f"""
    <div class="profile-box">
        <b>Exam Grid Controls</b>
    </div>
    <table class="status-summary-table">
        <tr>
            <td><span style="background:#28a745;color:white;padding:2px 4px;font-weight:bold;">{answered}</span> Ans</td>
            <td><span style="background:#dc3545;color:white;padding:2px 4px;font-weight:bold;">{not_answered}</span> Unans</td>
        </tr>
        <tr>
            <td><span style="background:#6f42c1;color:white;padding:2px 4px;font-weight:bold;">{marked_review}</span> Review</td>
            <td><span style="background:#e9ecef;color:#495057;padding:2px 4px;font-weight:bold;">{not_visited}</span> Not Visited</td>
        </tr>
    </table>
    """, unsafe_allow_html=True)
    
    total_qs = len(st.session_state.questions)
    grid_cols = 4  # Adjusted grid size for crisp distribution across screens
    
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
                    if st.button(f"{status_symbol}{q_num}", key=f"tbl_pal_{idx}", use_container_width=True):
                        st.session_state.current_question_index = idx
                        st.session_state.visited_questions.add(idx)
                        st.rerun()

# ==========================================
# 5. WORKFLOW PAGES
# ==========================================
def render_home_page():
    st.title("🎯 MockTest Pro — Universal Engine")
    st.markdown("""
    Optimized responsive CBT execution node dashboard interface engine.
    """)
    st.info("Select **Upload PDF** from the navigation controls panel to initialize.")

def render_upload_page():
    st.subheader("📂 Ingest Exam Document Object (PDF)")
    uploaded_file = st.file_uploader("Upload MCQ Exam Sheet Matrix:", type=["pdf"])
    
    if uploaded_file is not None:
        with st.spinner("Analyzing document mapping architectures..."):
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
                st.success(f"Success! {len(parsed_qs)} questions loaded efficiently into memory targets.")
            else:
                st.error("Regex validation format error. Ensure standard numbering formats are used.")

def render_practice_page():
    if not st.session_state.questions:
        st.warning("Please upload a valid data asset stream matrix first.")
        return
        
    q_idx = st.session_state.current_question_index
    q = st.session_state.questions[q_idx]
    
    st.markdown('<div class="section-tab">Workspace Section: Tablet View Practice Suite</div>', unsafe_allow_html=True)
    
    # Render layout sequentially without unsafe horizontal grid splits to prevent tablet breaks
    st.markdown(f"""
    <div class="q-container">
        <div class="q-number-title">Question No. {q['question_number']}</div>
        <p style='font-size:15px;'><b>{q['question']}</b></p>
    </div>
    """, unsafe_allow_html=True)
    
    opts = [f"A. {q['A']}", f"B. {q['B']}", f"C. {q['C']}", f"D. {q['D']}"]
    curr_sel = ["A", "B", "C", "D"].index(q["user_answer"]) if q["user_answer"] else None
    
    selected_option = st.radio("Select Choice Coordinate Node Input:", opts, index=curr_sel, key=f"t_p_rad_{q_idx}")
    
    if selected_option:
        ans_char = selected_option[0]
        st.session_state.questions[q_idx]["user_answer"] = ans_char
        if ans_char == q["correct_answer"]:
            st.markdown('<div class="feedback-box feedback-success">✔ Correct Assessment Node Registered.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="feedback-box feedback-danger">✘ Incorrect choice coordinate. Core target key value is: <b>Option {q["correct_answer"]}</b></div>', unsafe_allow_html=True)
            
    st.write("---")
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("⬅ Previous", disabled=(q_idx == 0), use_container_width=True, key="t_pr_b"):
            st.session_state.current_question_index -= 1
            st.rerun()
    with b2:
        if st.button("🧹 Clear", use_container_width=True, key="t_pr_c"):
            st.session_state.questions[q_idx]["user_answer"] = None
            st.rerun()
    with b3:
        if st.button("Save & Next ➡", disabled=(q_idx == len(st.session_state.questions) - 1), use_container_width=True, key="t_pr_n"):
            st.session_state.current_question_index += 1
            st.session_state.visited_questions.add(st.session_state.current_question_index)
            st.rerun()

    st.write("---")
    render_exam_palette()

def render_mock_page():
    if not st.session_state.questions:
        st.warning("Please upload a valid data asset stream matrix first.")
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
        
    st.markdown(f"""
    <div class="cbt-top-bar">
        <span>📋 Mock Core Mode Workspace</span>
        <span>⏳ Clock Remaining: {str(timedelta(seconds=int(rem_sec)))}</span>
    </div>
    """, unsafe_allow_html=True)
    
    q_idx = st.session_state.current_question_index
    q = st.session_state.questions[q_idx]
    
    st.markdown(f"""
    <div class="q-container">
        <div class="q-number-title">Question No. {q['question_number']}</div>
        <p style='font-size:15px;'><b>{q['question']}</b></p>
    </div>
    """, unsafe_allow_html=True)
    
    opts = [f"A. {q['A']}", f"B. {q['B']}", f"C. {q['C']}", f"D. {q['D']}"]
    curr_sel = ["A", "B", "C", "D"].index(q["user_answer"]) if q["user_answer"] else None
    
    selected_option = st.radio("Choose Option Select Parameters:", opts, index=curr_sel, key=f"t_m_rad_{q_idx}")
    
    st.write("---")
    act_c1, act_c2, act_c3, act_c4 = st.columns(4)
    
    with act_c1:
        if st.button("🟣 Review & Next", use_container_width=True, key="t_m_rev"):
            st.session_state.questions[q_idx]["review"] = True
            if selected_option:
                st.session_state.questions[q_idx]["user_answer"] = selected_option[0]
            if q_idx < len(st.session_state.questions) - 1:
                st.session_state.current_question_index += 1
                st.session_state.visited_questions.add(st.session_state.current_question_index)
            st.rerun()
            
    with act_c2:
        if st.button("🧹 Clear Ans", use_container_width=True, key="t_m_clr"):
            st.session_state.questions[q_idx]["user_answer"] = None
            st.session_state.questions[q_idx]["review"] = False
            st.rerun()
            
    with act_c3:
        if st.button("💾 Save & Next ➡", type="primary", use_container_width=True, key="t_m_nxt"):
            if selected_option:
                st.session_state.questions[q_idx]["user_answer"] = selected_option[0]
            st.session_state.questions[q_idx]["review"] = False
            if q_idx < len(st.session_state.questions) - 1:
                st.session_state.current_question_index += 1
                st.session_state.visited_questions.add(st.session_state.current_question_index)
            st.rerun()
            
    with act_c4:
        if st.button("🛑 End Test Pack", use_container_width=True, key="t_m_sub"):
            st.session_state.test_submitted = True
            st.session_state.time_taken_seconds = elapsed
            st.session_state.current_page = "Result"
            st.rerun()

    st.write("---")
    render_exam_palette()

def render_result_page():
    st.subheader("📊 Performance Diagnostics Summary Studio")
    
    if not st.session_state.questions or not st.session_state.test_submitted:
        st.warning("No submission log database node located to trace profiles.")
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
    
    st.metric("Total Items Ingested", total_q)
    st.metric("Verified True Node Matches", correct)
    st.metric("Calculation Accuracy Metrics Factor", f"{accuracy:.2f}%")
    st.metric("Duration Expended Spans", str(timedelta(seconds=int(st.session_state.time_taken_seconds))))

def render_settings_page():
    st.subheader("⚙️ Global Settings Portal")
    st.session_state.test_duration_minutes = st.number_input(
        "Set Global Duration Limitations Span Bounds (Minutes Scale):",
        min_value=5, max_value=200, value=st.session_state.test_duration_minutes
    )
    st.success("Global config framework states modified securely.")

# ==========================================
# 6. APPLICATION ROUTER ENTRY INITIALIZER
# ==========================================
def main():
    apply_testbook_theme()
    init_session_state()
    
    st.sidebar.markdown("<h2 style='text-align:center; color:#4682B4;'>📝 MockTest Pro</h2>", unsafe_allow_html=True)
    st.sidebar.write("---")
    
    selected_menu_route = st.sidebar.radio(
        "Select Operation Panel Workspace Mode:",
        ["Home", "Upload PDF", "Practice Mode", "Mock Test", "Result", "Settings"]
    )
    
    st.session_state.current_page = selected_menu_route
    
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
