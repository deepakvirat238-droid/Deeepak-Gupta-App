import streamlit as st
import pdfplumber
import re
import time
from datetime import timedelta

# Injecting root page structure configuration rules
st.set_page_config(
    page_title="Testbook Engine — MockTest Pro Premium",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 1. PREMIUM EXACT TESTBOOK CBT SIMULATOR CSS
# ==========================================
def apply_premium_testbook_css():
    st.markdown("""
    <style>
        /* Force App Base background match */
        .main { background-color: #f1f3f5 !important; padding: 0px !important; }
        
        /* TCS iON Rigid Dual-Pane Container Architecture for Tablets */
        .tcs-cbt-wrapper {
            display: flex;
            flex-direction: row;
            gap: 15px;
            width: 100%;
            margin-top: 10px;
        }
        
        /* Left Pane - Pure Question Display Slate */
        .tcs-question-slate {
            flex: 3;
            background: #ffffff;
            border: 1px solid #dcdcdc;
            padding: 20px;
            min-height: 400px;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        
        /* Right Pane - Strict Sticky Exam Sidebar Controls Matrix */
        .tcs-palette-slate {
            flex: 1;
            background: #ffffff;
            border: 1px solid #dcdcdc;
            padding: 15px;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            min-width: 260px;
        }
        
        /* TCS Top Header Bar Component Blueprint */
        .testbook-top-bar {
            background-color: #4682B4;
            color: #ffffff;
            padding: 12px 20px;
            font-size: 15px;
            font-weight: bold;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 3px solid #2a5d84;
        }
        
        /* Segment Title Header Tab */
        .tcs-section-badge {
            background-color: #e7f1f9;
            color: #1e4f75;
            padding: 8px 16px;
            font-weight: bold;
            font-size: 13px;
            border-top: 3px solid #4682B4;
            display: inline-block;
            border-radius: 3px 3px 0 0;
            margin-bottom: 5px;
        }

        /* Question Frame Styling Specifications */
        .tcs-q-box {
            border-bottom: 1px solid #f0f0f0;
            padding-bottom: 15px;
            margin-bottom: 20px;
        }
        .tcs-q-idx {
            font-size: 14px;
            font-weight: bold;
            color: #333333;
            margin-bottom: 8px;
        }
        .tcs-q-text { font-size: 15px; color: #222222; font-weight: 500; }
        
        /* Candidate Context Profile Card */
        .tcs-profile-card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            padding: 12px;
            text-align: center;
            margin-bottom: 15px;
            border-radius: 4px;
        }
        
        /* Numeric Matrix Counter Table System */
        .tcs-stats-table {
            width: 100%;
            font-size: 12px;
            margin-bottom: 15px;
            border-collapse: collapse;
        }
        .tcs-stats-table td { padding: 4px; border: 1px solid #f0f0f0; text-align: left; }
        .tcs-indicator-dot {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 2px;
            margin-right: 5px;
            vertical-align: middle;
        }
        
        /* Streamlit Native Widget Box Constraints Overrides */
        div.stButton > button {
            border-radius: 3px !important;
            font-size: 13px !important;
            font-weight: 500 !important;
            transition: all 0.2s;
        }
        
        /* Response Status Banner Blocks */
        .status-banner {
            border-radius: 4px;
            padding: 12px 15px;
            margin: 15px 0;
            font-weight: 600;
            font-size: 14px;
        }
        .status-ok { background-color: #d4edda; color: #155724; border-left: 5px solid #28a745; }
        .status-err { background-color: #f8d7da; color: #721c24; border-left: 5px solid #dc3545; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. SESSION STATE PIPELINES INITIALIZATION
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
# 3. ADVANCED HIGH-ACCURACY PARSING PIPELINE
# ==========================================
def extract_pdf_data(uploaded_file):
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            total_pages = len(pdf.pages)
            if total_pages < 2:
                return None, None, "PDF layout requires at least 2 structural sheets to evaluate patterns."
            
            question_text = ""
            for page in pdf.pages[:-1]:
                text = page.extract_text()
                if text:
                    question_text += text + "\n"
            
            last_page_text = pdf.pages[-1].extract_text()
            return question_text, last_page_text, None
    except Exception as e:
        return None, None, f"Asset stream reading failure exception: {str(e)}"

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

    # Normalized structural parsing hook splitting questions
    q_split_pattern = r'(?:\n|\A)(?:Q(?:uestion)?\s*\.?\s*)?(\d+)[\.\)]\s+'
    parts = re.split(q_split_pattern, text)
    
    if len(parts) < 3:
        return questions_list

    for i in range(1, len(parts), 2):
        q_num = int(parts[i])
        q_body = parts[i+1]
        
        # Highly precise inline capture for loose option blocks (like A Mars B venus)
        opt_pattern = re.compile(
            r'(?:[\n\s]|\A)(?:[\(\[]?)([A-E])(?:[\.\)\]]|\s+)\s*([\s\S]*?)(?=(?:[\n\s]|\A)(?:[\(\[]?)[B-E](?:[\.\)\]]|\s+)|$)',
            re.IGNORECASE
        )
        
        opts_found = opt_pattern.findall(q_body)
        opts_dict = {'A': 'Option A Content Template', 'B': 'Option B Content Template', 'C': 'Option C Content Template', 'D': 'Option D Content Template'}
        
        first_opt_idx = re.search(r'(?:[\n\s]|\A)(?:[\(\[]?)[A-E](?:[\.\)\]]|\s+)', q_body, re.IGNORECASE)
        actual_question = q_body[:first_opt_idx.start()].strip() if first_opt_idx else q_body.strip()
        actual_question = re.sub(r'\s+', ' ', actual_question)
        
        for letter, content in opts_found:
            opts_dict[letter.upper()] = re.sub(r'\s+', ' ', content.strip())
            
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
# 4. FIXED SIDEBAR SLATE ARCHITECTURE COMPONENT
# ==========================================
def draw_testbook_palette_slate():
    """Compiles the actual Right Palette view box metrics cleanly."""
    answered = sum(1 for q in st.session_state.questions if q["user_answer"] is not None and not q["review"])
    marked_review = sum(1 for q in st.session_state.questions if q["review"])
    not_visited = len(st.session_state.questions) - len(st.session_state.visited_questions)
    not_answered = len(st.session_state.questions) - answered - marked_review - not_visited

    st.markdown(f"""
    <div class="tcs-profile-card">
        <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" width="50" style="border-radius:50%; margin-bottom:5px;"><br/>
        <span style="font-size:13px; font-weight:bold; color:#2c3e50;">Kanchan Kumari</span><br/>
        <span style="font-size:11px; color:#7f8c8d;">ID: 2026-CBT</span>
    </div>
    <table class="tcs-stats-table">
        <tr>
            <td><span class="tcs-indicator-dot" style="background:#28a745;"></span> Answered: <b>{answered}</b></td>
            <td><span class="tcs-indicator-dot" style="background:#dc3545;"></span> Unanswered: <b>{not_answered}</b></td>
        </tr>
        <tr>
            <td><span class="tcs-indicator-dot" style="background:#6f42c1;"></span> Review: <b>{marked_review}</b></td>
            <td><span class="tcs-indicator-dot" style="background:#e9ecef; border:1px solid #ccc;"></span> Visited: <b>{len(st.session_state.visited_questions)}</b></td>
        </tr>
    </table>
    <div style="font-size:12px; font-weight:bold; margin-bottom:8px; color:#34495e;">Question Navigation Matrix:</div>
    """, unsafe_allow_html=True)
    
    total_qs = len(st.session_state.questions)
    grid_columns_limit = 4
    
    for i in range(0, total_qs, grid_columns_limit):
        cols = st.columns(grid_columns_limit)
        for j in range(grid_columns_limit):
            idx = i + j
            if idx < total_qs:
                q = st.session_state.questions[idx]
                q_num = q["question_number"]
                
                # Dynamic indicator symbols matching exact CBT state profiles
                badge = "⬜"
                if idx == st.session_state.current_question_index:
                    badge = "🔵"
                elif q["review"]:
                    badge = "🟣"
                elif q["user_answer"] is not None:
                    badge = "🟢"
                elif idx in st.session_state.visited_questions:
                    badge = "🔴"
                    
                with cols[j]:
                    if st.button(f"{badge}{q_num}", key=f"tcs_lnk_{idx}", use_container_width=True):
                        st.session_state.current_question_index = idx
                        st.session_state.visited_questions.add(idx)
                        st.rerun()

# ==========================================
# 5. WORKFLOW BOARD LAYOUT PAGES ROUTER
# ==========================================
def render_home_page():
    st.title("🎯 MockTest Pro — Elite Platform Panel")
    st.markdown("""
    ### 💻 Production Matrix Overview:
    * **Rigid Split Layout Matrix**: Blocks automatic scaling failures across widescreen tablet models.
    * **High Efficiency Engine**: Instant tracking configuration parsing maps.
    """)
    st.info("Choose **Upload PDF** inside your dashboard portal sidebar route matrix to open files.")

def render_upload_page():
    st.subheader("📂 Ingest MCQ Core Blueprint Sheets")
    uploaded_file = st.file_uploader("Select Exam Asset Stream Document Target (PDF Spec):", type=["pdf"])
    
    if uploaded_file is not None:
        with st.spinner("Decoding internal page objects..."):
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
                st.success(f"Portfolios initialized. Successfully cataloged {len(parsed_qs)} questions inside active session layers.")
            else:
                st.error("Text alignment scanning boundary breakdown. Check data delimiters formatting structure configuration rules.")

def render_practice_page():
    if not st.session_state.questions:
        st.warning("No operational evaluation contexts found. Upload an active database blueprint structure first.")
        return
        
    q_idx = st.session_state.current_question_index
    q = st.session_state.questions[q_idx]
    
    st.markdown('<div class="tcs-section-badge">Active Section: Real-time Practice Engine</div>', unsafe_allow_html=True)
    
    # Unified horizontal row constraint wrapper to force layout matching across tablet bounds
    col_slate, col_control = st.columns([2.8, 1.2])
    
    with col_slate:
        st.markdown(f"""
        <div class="tcs-question-slate">
            <div class="tcs-q-box">
                <div class="tcs-q-idx">Question ID Node #{q['question_number']}</div>
                <div class="tcs-q-text">{q['question']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        opts = [f"A. {q['A']}", f"B. {q['B']}", f"C. {q['C']}", f"D. {q['D']}"]
        curr_sel = ["A", "B", "C", "D"].index(q["user_answer"]) if q["user_answer"] else None
        
        selected_option = st.radio("Choose the correct choice vector node:", opts, index=curr_sel, key=f"scr_pr_{q_idx}")
        
        if selected_option:
            ans_char = selected_option[0]
            st.session_state.questions[q_idx]["user_answer"] = ans_char
            if ans_char == q["correct_answer"]:
                st.markdown('<div class="status-banner status-ok">✔ Choice Confirmed Against Reference Sheet Key Target!</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="status-banner status-err">✘ Wrong Choice Coordinate. Verified System target Key is: <b>Option {q["correct_answer"]}</b></div>', unsafe_allow_html=True)
                
        st.write("---")
        nav_c1, nav_c2, nav_c3 = st.columns(3)
        with nav_c1:
            if st.button("⬅ Previous", disabled=(q_idx == 0), use_container_width=True, key="pr_p_b"):
                st.session_state.current_question_index -= 1
                st.rerun()
        with nav_c2:
            if st.button("Clear Choice", use_container_width=True, key="pr_c_b"):
                st.session_state.questions[q_idx]["user_answer"] = None
                st.rerun()
        with nav_c3:
            if st.button("Save & Next ➡", disabled=(q_idx == len(st.session_state.questions) - 1), use_container_width=True, key="pr_n_b"):
                st.session_state.current_question_index += 1
                st.session_state.visited_questions.add(st.session_state.current_question_index)
                st.rerun()

    with col_control:
        draw_testbook_palette_slate()

def render_mock_page():
    if not st.session_state.questions:
        st.warning("No operational evaluation contexts found. Upload an active database blueprint structure first.")
        return
        
    if st.session_state.test_start_time is None:
        st.session_state.test_start_time = time.time()
        
    elapsed = time.time() - st.session_state.test_start_time
    total_allowed = st.session_state.test_duration_minutes * 60
    remaining_secs = max(0, total_allowed - elapsed)
    
    if remaining_secs == 0 and not st.session_state.test_submitted:
        st.session_state.test_submitted = True
        st.session_state.time_taken_seconds = total_allowed
        st.session_state.current_page = "Result"
        st.rerun()
        
    st.markdown(f"""
    <div class="testbook-top-bar">
        <span>📋 Mock CBT Exam Center Pane Workspace Terminal</span>
        <span>⏳ Time Remaining Check: {str(timedelta(seconds=int(remaining_secs)))}</span>
    </div>
    """, unsafe_allow_html=True)
    
    q_idx = st.session_state.current_question_index
    q = st.session_state.questions[q_idx]
    
    col_slate, col_control = st.columns([2.8, 1.2])
    
    with col_slate:
        st.markdown(f"""
        <div class="tcs-question-slate">
            <div class="tcs-q-box">
                <div class="tcs-q-idx">Question Reference Index Node #{q['question_number']}</div>
                <div class="tcs-q-text"><b>{q['question']}</b></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        opts = [f"A. {q['A']}", f"B. {q['B']}", f"C. {q['C']}", f"D. {q['D']}"]
        curr_sel = ["A", "B", "C", "D"].index(q["user_answer"]) if q["user_answer"] else None
        
        selected_option = st.radio("Choose Option Select Parameters:", opts, index=curr_sel, key=f"scr_mk_{q_idx}")
        
        st.write("---")
        act_1, act_2, act_3, act_4 = st.columns(4)
        
        with act_1:
            if st.button("🟣 Mark for Review & Next", use_container_width=True, key="mk_rev_b"):
                st.session_state.questions[q_idx]["review"] = True
                if selected_option:
                    st.session_state.questions[q_idx]["user_answer"] = selected_option[0]
                if q_idx < len(st.session_state.questions) - 1:
                    st.session_state.current_question_index += 1
                    st.session_state.visited_questions.add(st.session_state.current_question_index)
                st.rerun()
                
        with act_2:
            if st.button("🧹 Clear Response", use_container_width=True, key="mk_clr_b"):
                st.session_state.questions[q_idx]["user_answer"] = None
                st.session_state.questions[q_idx]["review"] = False
                st.rerun()
                
        with act_3:
            if st.button("💾 Save & Next ➡", type="primary", use_container_width=True, key="mk_nxt_b"):
                if selected_option:
                    st.session_state.questions[q_idx]["user_answer"] = selected_option[0]
                st.session_state.questions[q_idx]["review"] = False
                if q_idx < len(st.session_state.questions) - 1:
                    st.session_state.current_question_index += 1
                    st.session_state.visited_questions.add(st.session_state.current_question_index)
                st.rerun()
                
        with act_4:
            if st.button("🛑 Submit Portfolio", use_container_width=True, key="mk_sub_b"):
                st.session_state.test_submitted = True
                st.session_state.time_taken_seconds = elapsed
                st.session_state.current_page = "Result"
                st.rerun()

    with col_control:
        draw_testbook_palette_slate()

def render_result_page():
    st.subheader("📊 Performance Diagnostic Summary Matrix Studio")
    
    if not st.session_state.questions or not st.session_state.test_submitted:
        st.warning("No comprehensive test submission log contexts located.")
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
    
    st.metric("Total Extracted Assessment Nodes", total_q)
    st.metric("Verified Valid Core Hits", correct)
    st.metric("Engine Precision Accuracy Index Factor", f"{accuracy:.2f}%")
    st.metric("Total Operational Test Session Runtime", str(timedelta(seconds=int(st.session_state.time_taken_seconds))))

def render_settings_page():
    st.subheader("⚙️ Global Framework Architecture Settings")
    st.session_state.test_duration_minutes = st.number_input(
        "Modify Default Session Countdown limits span parameter (Minutes Allocation Bound Loop):",
        min_value=5, max_value=200, value=st.session_state.test_duration_minutes
    )
    st.success("Global config framework states modified securely down localized channels.")

# ==========================================
# 6. APPLICATION ROUTER DESK INITIALIZER
# ==========================================
def main():
    apply_premium_testbook_css()
    init_session_state()
    
    st.sidebar.markdown("<h2 style='text-align:center; color:#4682B4; margin-top:0px;'>📝 Testbook Pro</h2>", unsafe_allow_html=True)
    st.sidebar.write("---")
    
    selected_portal_route = st.sidebar.radio(
        "Application Navigation Panel Link Selector Panel Matrix Route:",
        ["Home", "Upload PDF", "Practice Mode", "Mock Test", "Result", "Settings"]
    )
    
    st.session_state.current_page = selected_portal_route
    
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

