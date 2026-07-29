import streamlit as st
import pdfplumber
import re
import time
from datetime import timedelta

# Streamlit configurations for matching structural dashboard metrics
st.set_page_config(
    page_title="MockTest Pro — Online Assessment Framework",
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
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. SESSION STATE STATE MATRIX
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
# 3. HIGH-FIDELITY PDF PARSING ENGINE
# ==========================================
def extract_pdf_data(uploaded_file):
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            total_pages = len(pdf.pages)
            if total_pages < 2:
                return None, None, "PDF requires multiple pages to process structurally."
            
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
    clean_text = re.sub(r'(ANSWER\s*KEY|Ans[:\s]*)', '', text, flags=re.IGNORECASE)
    pattern = re.compile(r'(?:Q(?:uestion)?\s*)?(\d+)\s*[\.\-\)\:\s]*\s*([A-E])', re.IGNORECASE)
    matches = pattern.findall(clean_text)
    for num, option in matches:
        answers[int(num)] = option.upper().strip()
    return answers

def parse_questions(text, answer_key):
    questions_list = []
    q_split_pattern = r'(?:\n|\A)(?:Q(?:uestion)?\s*\.?\s*)?(\d+)[\.\)]\s+'
    parts = re.split(q_split_pattern, text)
    if len(parts) < 3:
        return []

    for i in range(1, len(parts), 2):
        q_num = int(parts[i])
        q_body = parts[i+1]
        
        opt_pattern = re.compile(
            r'(?:[\n\s]|\A)(?:[\(\[]?)([A-E])(?:[\.\)\]]|\s+)\s*([\s\S]*?)(?=(?:[\n\s]|\A)(?:[\(\[]?)[B-E](?:[\.\)\]]|\s+)|$)',
            re.IGNORECASE
        )
        
        opts_found = opt_pattern.findall(q_body)
        opts_dict = {'A': '', 'B': '', 'C': '', 'D': '', 'E': ''}
        
        first_opt_idx = re.search(r'(?:[\n\s]|\A)(?:[\(\[]?)[A-E](?:[\.\)\]]|\s+)', q_body, re.IGNORECASE)
        actual_question = q_body[:first_opt_idx.start()].strip() if first_opt_idx else q_body.strip()
        
        for letter, content in opts_found:
            opts_dict[letter.upper()] = content.strip()
            
        questions_list.append({
            "question_number": q_num,
            "question": actual_question,
            "A": opts_dict['A'],
            "B": opts_dict['B'],
            "C": opts_dict['C'],
            "D": opts_dict['D'],
            "correct_answer": answer_key.get(q_num, ""),
            "user_answer": None,
            "review": False
        })
        
    return sorted(questions_list, key=lambda x: x["question_number"])

# ==========================================
# 4. COMPACT NAV PALETTE ENGINE
# ==========================================
def render_sidebar_palette():
    # Performance status count logic
    answered = sum(1 for q in st.session_state.questions if q["user_answer"] is not None and not q["review"])
    marked_review = sum(1 for q in st.session_state.questions if q["review"])
    not_visited = len(st.session_state.questions) - len(st.session_state.visited_questions)
    not_answered = len(st.session_state.questions) - answered - marked_review - not_visited

    st.markdown(f"""
    <div class="profile-box">
        <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" width="60" style="margin-bottom:5px;"><br/>
        <b>Candidate Name</b><br/><span style="font-size:12px;color:grey;">Roll No: 4096238</span>
    </div>
    <table class="status-summary-table">
        <tr>
            <td><span style="background:#28a745;color:white;padding:2px 6px;font-weight:bold;">{answered}</span> Answered</td>
            <td><span style="background:#dc3545;color:white;padding:2px 6px;font-weight:bold;">{not_answered}</span> Not Answered</td>
        </tr>
        <tr>
            <td><span style="background:#6f42c1;color:white;padding:2px 6px;font-weight:bold;">{marked_review}</span> Marked Review</td>
            <td><span style="background:#e9ecef;color:#495057;padding:2px 6px;font-weight:bold;">{not_visited}</span> Not Visited</td>
        </tr>
    </table>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.write("🎰 **Choose Question Grid:**")
    
    total_qs = len(st.session_state.questions)
    grid_cols = 4
    for i in range(0, total_qs, grid_cols):
        cols = st.columns(grid_cols)
        for j in range(grid_cols):
            idx = i + j
            if idx < total_qs:
                q = st.session_state.questions[idx]
                q_num = q["question_number"]
                
                # Determine precise prefix marker parameters
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
# 5. WORKFLOW ROUTING RUNTIME PAGES
# ==========================================
def render_home_page():
    st.title("🎯 MockTest Pro — Elite Exam Desk")
    st.markdown("""
    Welcome to India's premium structural standard assessment simulator panel engine.
    
    ### 🏆 Real Exam Panel Features:
    * **TCS iON CBT Architecture Mapping Layout**
    * **One-Click Automated Dynamic Document parsing**
    * **State Isolation controls (Practice / Mock)**
    """)
    st.info("Select the **Upload PDF** menu navigation option inside the left sidebar panel to initialize your dataset profile.")

def render_upload_page():
    st.subheader("📂 Exam Sheet Data Core Upload Ingestion")
    uploaded_file = st.file_uploader("Upload MCQ Exam Sheet Matrix (PDF Asset Document)", type=["pdf"])
    
    if uploaded_file is not None:
        with st.spinner("Extracting token string layouts dynamically..."):
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
                st.success("Target document framework fully loaded into memory spaces successfully.")
            else:
                st.error("Regex validation exception structural map mismatch alert.")

def render_practice_page():
    if not st.session_state.questions:
        st.warning("No active structural data assets discovered inside active session pipelines.")
        return
        
    q_idx = st.session_state.current_question_index
    q = st.session_state.questions[q_idx]
    
    st.markdown('<div class="section-tab">Section: General Intelligence & Mock Practice</div>', unsafe_allow_html=True)
    
    col_left, col_right = st.columns([3, 1])
    
    with col_left:
        st.markdown(f"""
        <div class="q-container">
            <div class="q-number-title">Question No. {q['question_number']}</div>
            <p>{q['question']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        opts = [f"A. {q['A']}", f"B. {q['B']}", f"C. {q['C']}", f"D. {q['D']}"]
        curr_sel = ["A", "B", "C", "D"].index(q["user_answer"]) if q["user_answer"] else None
        
        selected_option = st.radio("Choose option field input vector:", opts, index=curr_sel, key=f"p_rad_{q_idx}")
        
        if selected_option:
            ans_char = selected_option[0]
            st.session_state.questions[q_idx]["user_answer"] = ans_char
            if ans_char == q["correct_answer"]:
                st.markdown('<div class="feedback-box feedback-success">✔ Correct Mapping Confirmed!</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="feedback-box feedback-danger">✘ Wrong. Target verified configuration coordinate key is: <b>{q["correct_answer"]}</b></div>', unsafe_allow_html=True)
                
        st.write("---")
        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("⬅ Back Target", disabled=(q_idx == 0), use_container_width=True):
                st.session_state.current_question_index -= 1
                st.rerun()
        with b2:
            if st.button("🧹 Flush Choice", use_container_width=True):
                st.session_state.questions[q_idx]["user_answer"] = None
                st.rerun()
        with b3:
            if st.button("Forward ➡", disabled=(q_idx == len(st.session_state.questions) - 1), use_container_width=True):
                st.session_state.current_question_index += 1
                st.session_state.visited_questions.add(st.session_state.current_question_index)
                st.rerun()

    with col_right:
        render_sidebar_palette()

def render_mock_page():
    if not st.session_state.questions:
        st.warning("No active evaluation schema loaded. Please process a valid file first via the **Upload PDF** engine.")
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
        <span>📋 Examination Window Engine Panel</span>
        <span>⏳ Time Remaining Check: {str(timedelta(seconds=int(rem_sec)))}</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-tab">Core Focus Major Paper Framework Section</div>', unsafe_allow_html=True)
    
    q_idx = st.session_state.current_question_index
    q = st.session_state.questions[q_idx]
    
    col_left, col_right = st.columns([3, 1])
    
    with col_left:
        st.markdown(f"""
        <div class="q-container">
            <div class="q-number-title">Question No. {q['question_number']}</div>
            <p><b>{q['question']}</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        opts = [f"A. {q['A']}", f"B. {q['B']}", f"C. {q['C']}", f"D. {q['D']}"]
        curr_sel = ["A", "B", "C", "D"].index(q["user_answer"]) if q["user_answer"] else None
        
        selected_option = st.radio("Choose Option Select:", opts, index=curr_sel, key=f"m_rad_{q_idx}")
        
        st.write("---")
        # Standard Action Configuration Matrix Row Placement Layout
        act_c1, act_c2, act_c3, act_c4 = st.columns(4)
        
        with act_c1:
            if st.button("🟣 Mark for Review & Next", use_container_width=True):
                st.session_state.questions[q_idx]["review"] = True
                if selected_option:
                    st.session_state.questions[q_idx]["user_answer"] = selected_option[0]
                if q_idx < len(st.session_state.questions) - 1:
                    st.session_state.current_question_index += 1
                    st.session_state.visited_questions.add(st.session_state.current_question_index)
                st.rerun()
                
        with act_c2:
            if st.button("🧹 Clear Response", use_container_width=True):
                st.session_state.questions[q_idx]["user_answer"] = None
                st.session_state.questions[q_idx]["review"] = False
                st.rerun()
                
        with act_c3:
            if st.button("💾 Save & Next ➡", type="primary", use_container_width=True):
                if selected_option:
                    st.session_state.questions[q_idx]["user_answer"] = selected_option[0]
                st.session_state.questions[q_idx]["review"] = False
                if q_idx < len(st.session_state.questions) - 1:
                    st.session_state.current_question_index += 1
                    st.session_state.visited_questions.add(st.session_state.current_question_index)
                st.rerun()
                
        with act_c4:
            if st.button("🛑 Submit Exam Model", use_container_width=True):
                st.session_state.test_submitted = True
                st.session_state.time_taken_seconds = elapsed
                st.session_state.current_page = "Result"
                st.rerun()

    with col_right:
        render_sidebar_palette()

def render_result_page():
    st.subheader("📊 Performance Analytics & System Diagnostics Report")
    
    if not st.session_state.questions or not st.session_state.test_submitted:
        st.warning("No dynamic evaluation sequence discovered to catalog analytical processing logs.")
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
    r_c1.metric("Total Ingested Matrix Items", total_q)
    r_c2.metric("Hit Scores Target Metric", correct)
    r_c3.metric("Miss Calculations Logged", wrong)
    
    r_c4, r_c5 = st.columns(2)
    r_c4.metric("Precision Index Factor Accuracy", f"{accuracy:.2f}%")
    r_c5.metric("System Operational Active Window Time", str(timedelta(seconds=int(st.session_state.time_taken_seconds))))
    
    st.write("---")
    st.markdown("### 🔍 Granular Structural Question & Solution Matrix Breakdown")
    for idx, q in enumerate(st.session_state.questions):
        with st.expander(f"Question Number Record Item Analysis #{q['question_number']}"):
            st.markdown(f"**Question Text Node Context Content:** {q['question']}")
            st.write(f"A. {q['A']}")
            st.write(f"B. {q['B']}")
            st.write(f"C. {q['C']}")
            st.write(f"D. {q['D']}")
            st.info(f"Verified System Reference Core Target: {q['correct_answer']} | Registered Vector Log Target Value: {q['user_answer']}")

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

