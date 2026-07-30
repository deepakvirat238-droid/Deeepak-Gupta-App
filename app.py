import streamlit as st
import pdfplumber
import re
import time
from datetime import timedelta

# Set page layout configuration immediately as the entry point execution criteria
st.set_page_config(
    page_title="Testbook Engine — MockTest Pro Premium Suite",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 1. PIXEL-PERFECT PREMIUM TESTBOOK CBT CSS & JAVASCRIPT
# ==========================================
def apply_premium_testbook_css():
    st.markdown("""
    <style>
        /* Force App Base background match */
        .main { background-color: #f1f3f5 !important; padding: 0px !important; }
        
        /* TCS iON Rigid Top Header Bar Component Blueprint */
        .testbook-top-bar {
            background-color: #005682;
            color: #ffffff;
            padding: 12px 20px;
            font-size: 15px;
            font-weight: bold;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 3px solid #2a5d84;
            font-family: sans-serif;
        }

        .timer-badge {
            background-color: #ffeeb5;
            color: #856404;
            padding: 6px 14px;
            border-radius: 4px;
            font-family: monospace;
            font-size: 16px;
            border: 1px solid #ffe8a1;
            font-weight: bold;
        }
        
        /* Section Tabs Header Segment Row */
        .tb-sections-bar {
            background-color: #ffffff;
            border-bottom: 1px solid #e2e8f0;
            padding: 0px 20px;
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .tb-section-lbl { font-size: 11px; font-weight: bold; color: #64748b; text-transform: uppercase; }
        .tb-tab-active {
            color: #ffffff !important;
            background-color: #005682 !important;
            padding: 8px 16px;
            font-size: 13px;
            font-weight: 500;
            border-radius: 4px 4px 0 0;
            display: inline-block;
        }

        /* Question Display Container Panel - Padding optimized */
        .tcs-question-slate {
            background: #ffffff;
            border: 1px solid #dcdcdc;
            padding: 20px 20px 10px 20px;
            min-height: auto;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            margin-bottom: 5px;
            margin-top: 15px;
        }
        
        .tcs-meta-row {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }
        
        .tcs-q-idx {
            font-size: 15px;
            font-weight: bold;
            color: #1e293b;
        }
        
        .badge-status-cbt {
            background-color: #e0f2fe; 
            color: #0369a1; 
            padding: 2px 6px; 
            font-size: 11px; 
            border-radius: 3px; 
            font-weight: 500;
        }
        
        .tcs-q-text { font-size: 16px; color: #222222; font-weight: 500; line-height: 1.4; margin-bottom: 10px; }
        
        /* CSS Hack to reduce space between question container and streamlit radio buttons */
        div[data-testid="stRadio"] {
            margin-top: -8px !important;
            padding-top: 0px !important;
        }
        div[data-testid="stRadio"] label p {
            font-size: 15px !important;
            color: #334155 !important;
        }
        
        /* Bottom Gray Frame Box inside core view matrix container */
        .tb-reattempt-box {
            background-color: #fff7ed;
            border: 1px solid #ffedd5;
            padding: 12px 15px;
            border-radius: 4px;
            margin-top: 20px;
        }

        /* Candidate Context Profile Card */
        .tcs-profile-card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            padding: 12px;
            text-align: center;
            margin-bottom: 15px;
            border-radius: 4px;
            margin-top: 15px;
        }
        
        /* Numeric Matrix Counter Table System */
        .tcs-stats-table {
            width: 100%;
            font-size: 12px;
            margin-bottom: 15px;
            border-collapse: collapse;
        }
        .tcs-stats-table td { padding: 6px; border: 1px solid #e2e8f0; text-align: left; }
        .tcs-indicator-dot {
            display: inline-block;
            width: 14px;
            height: 14px;
            border-radius: 3px;
            margin-right: 6px;
            vertical-align: middle;
        }
        
        /* Streamlit Native Widget Box Constraints Overrides */
        div.stButton > button {
            border-radius: 3px !important;
            font-size: 13px !important;
            font-weight: 500 !important;
        }
        
        /* Response Status Banner Blocks */
        .status-banner {
            border-radius: 4px;
            padding: 10px 15px;
            margin: 10px 0;
            font-weight: 600;
            font-size: 14px;
        }
        .status-ok { background-color: #d4edda; color: #155724; border-left: 5px solid #28a745; }
        .status-err { background-color: #f8d7da; color: #721c24; border-left: 5px solid #dc3545; }
    </style>
    """, unsafe_allow_html=True)

def inject_cbt_security_script():
    """Injects JavaScript to handle automatic strict fullscreen and detect tab switching / minimization triggers."""
    st.markdown("""
    <script>
        // Automatic Request Fullscreen Functionality Matrix
        function launchFullscreen() {
            var element = document.documentElement;
            if(element.requestFullscreen) { element.requestFullscreen(); }
            else if(element.mozRequestFullScreen) { element.mozRequestFullScreen(); }
            else if(element.webkitRequestFullscreen) { element.webkitRequestFullscreen(); }
            else if(element.msRequestFullscreen) { element.msRequestFullscreen(); }
        }
        
        // Trigger fullscreen ingestion seamlessly
        setTimeout(launchFullscreen, 1000);

        // Window Tab/Application Switch Ingestion Monitor
        document.addEventListener("visibilitychange", function() {
            if (document.hidden) {
                alert("🚨 WINDOW SWITCH DETECTION ALERT!\\n\\nYou attempted to switch applications or browser tabs. This action violates strict CBT environment regulations. Further violations will log an automatic submission.");
            }
        });
    </script>
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
        opts_dict = {'A': 'Option A Content', 'B': 'Option B Content', 'C': 'Option C Content', 'D': 'Option D Content'}
        
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
# 4. COMPACT PALETTE METRICS GRID SIDEBAR
# ==========================================
def draw_testbook_palette_slate():
    answered = sum(1 for q in st.session_state.questions if q["user_answer"] is not None and not q["review"])
    marked_review = sum(1 for q in st.session_state.questions if q["review"])
    not_visited = len(st.session_state.questions) - len(st.session_state.visited_questions)
    not_answered = len(st.session_state.questions) - answered - marked_review - not_visited

    st.markdown(f"""
    <div class="tcs-profile-card">
        <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" width="55" style="border-radius:50%; margin-bottom:5px;"><br/>
        <span style="font-size:13px; font-weight:bold; color:#2c3e50;">Kanchan Kumari</span><br/>
        <span style="font-size:11px; color:#7f8c8d;">ID: Testbook-2026</span>
    </div>
    <table class="tcs-stats-table">
        <tr>
            <td><span class="tcs-indicator-dot" style="background:#28a745;"></span> Answered: <b>{answered}</b></td>
            <td><span class="tcs-indicator-dot" style="background:#dc3545;"></span> Unanswered: <b>{not_answered}</b></td>
        </tr>
        <tr>
            <td><span class="tcs-indicator-dot" style="background:#6f42c1;"></span> Review: <b>{marked_review}</b></td>
            <td><span class="tcs-indicator-dot" style="background:#e9ecef; border:1px solid #ccc;"></span> Not Visited: <b>{not_visited}</b></td>
        </tr>
    </table>
    <div style="font-size:12px; font-weight:bold; margin-bottom:8px; color:#34495e;">Question Navigation Palette:</div>
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
# 5. CORE WORKFLOW INTEGRATION ROUTERS
# ==========================================
def render_home_page():
    st.title("🎯 MockTest Pro — Premium CBT Examination Desk")
    st.markdown("""
    Welcome to India's premium structural standard assessment simulator panel engine.
    
    ### 🛡️ CBT Security Notice:
    Entering the **Mock Test** space forces your engine viewport into a hardware-level **Fullscreen Mode**. Switching applications or moving away from the active tab displays a violation override alert.
    """)
    st.info("Select **Upload PDF** from the sidebar route matrix to get started.")

def render_upload_page():
    st.subheader("📂 Ingest Exam Document Object (PDF)")
    uploaded_file = st.file_uploader("Upload MCQ Exam Sheet Matrix Blueprint Asset:", type=["pdf"])
    
    if uploaded_file is not None:
        with st.spinner("Decoding layout structures..."):
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
                st.success(f"Ingestion successful! Loaded {len(parsed_qs)} questions effectively into active data channels.")
            else:
                st.error("Text alignment parsing error anomaly detected. Ensure your asset matches standard layouts.")

def render_practice_page():
    if not st.session_state.questions:
        st.warning("No operational evaluation contexts found. Upload an active database blueprint structure first.")
        return
        
    q_idx = st.session_state.current_question_index
    q = st.session_state.questions[q_idx]
    
    st.markdown("""
    <div class="testbook-top-bar">
        <span>📋 Interactive Self-Practice Mode Console Panel</span>
        <span style="font-size:12px; font-weight:normal; background:rgba(255,255,255,0.2); padding:4px 10px; border-radius:3px;">Practice Sandbox</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="tb-sections-bar"><span class="tb-section-lbl">Sections</span><span class="tb-tab-active">General Science</span></div>', unsafe_allow_html=True)
    
    col_slate, col_control = st.columns([2.8, 1.2])
    
    with col_slate:
        st.markdown(f"""
        <div class="tcs-question-slate">
            <div class="tcs-q-box">
                <div class="tcs-meta-row">
                    <span class="tcs-q-idx">Question No. {q['question_number']}</span>
                    <span class="badge-status-cbt">Marks 1</span>
                    <span class="badge-status-cbt" style="background-color:#f0fdf4; color:#166534;">Practice Sandbox</span>
                </div>
                <div class="tcs-q-text">{q['question']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        opts = [f"A. {q['A']}", f"B. {q['B']}", f"C. {q['C']}", f"D. {q['D']}"]
        curr_sel = ["A", "B", "C", "D"].index(q["user_answer"]) if q["user_answer"] else None
        
        selected_option = st.radio("Options Hidden Label:", opts, index=curr_sel, key=f"scr_pr_{q_idx}")
        
        if selected_option:
            ans_char = selected_option[0]
            st.session_state.questions[q_idx]["user_answer"] = ans_char
            if ans_char == q["correct_answer"]:
                st.markdown('<div class="status-banner status-ok">✔ Correct Mapping Confirmed!</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="status-banner status-err">✘ Wrong Choice. Target verified configuration coordinate key is: <b>Option {q["correct_answer"]}</b></div>', unsafe_allow_html=True)
                
        st.write("---")
        nav_c1, nav_c2, nav_c3 = st.columns(3)
        with nav_c1:
            if st.button("⬅ Previous Question", disabled=(q_idx == 0), use_container_width=True, key="pr_p_b"):
                st.session_state.current_question_index -= 1
                st.rerun()
        with nav_c2:
            if st.button("🧹 Clear Response Node", use_container_width=True, key="pr_c_b"):
                st.session_state.questions[q_idx]["user_answer"] = None
                st.rerun()
        with nav_c3:
            if st.button("Save & Next Question ➡", disabled=(q_idx == len(st.session_state.questions) - 1), use_container_width=True, key="pr_n_b"):
                st.session_state.current_question_index += 1
                st.session_state.visited_questions.add(st.session_state.current_question_index)
                st.rerun()

    with col_control:
        draw_testbook_palette_slate()

def render_mock_page():
    if not st.session_state.questions:
        st.warning("No operational evaluation contexts found. Upload an active database blueprint structure first.")
        return
        
    # Ingest strict fullscreen rules and anti tab-switching monitoring script parameters
    inject_cbt_security_script()
        
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
        <span>📋 Online Computer Based Test (🔐 STRICT FULL-SCREEN LOCK ON)</span>
        <div>⏳ Time Remaining: <span class="timer-badge">{str(timedelta(seconds=int(remaining_secs)))}</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="tb-sections-bar"><span class="tb-section-lbl">Sections</span><span class="tb-tab-active">General Science</span></div>', unsafe_allow_html=True)
    
    if st.session_state.test_submitted:
        st.info("Your response sheet profile has closed execution loops. View report cards via the **Result** dashboard page.")
        return

    q_idx = st.session_state.current_question_index
    q = st.session_state.questions[q_idx]
    
    col_slate, col_control = st.columns([2.8, 1.2])
    
    with col_slate:
        st.markdown(f"""
        <div class="tcs-question-slate">
            <div class="tcs-q-box">
                <div class="tcs-meta-row">
                    <span class="tcs-q-idx">Question No. {q['question_number']}</span>
                    <span class="badge-status-cbt">Marks 1</span>
                    <span class="badge-status-cbt" style="background-color:#fee2e2; color:#991b1b;">Exam Context Active</span>
                </div>
                <div class="tcs-q-text"><b>{q['question']}</b></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        opts = [f"A. {q['A']}", f"B. {q['B']}", f"C. {q['C']}", f"D. {q['D']}"]
        curr_sel = ["A", "B", "C", "D"].index(q["user_answer"]) if q["user_answer"] else None
        
        selected_option = st.radio("Options Hidden Label:", opts, index=curr_sel, key=f"scr_mk_{q_idx}")
        
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
            if st.button("🛑 Submit Examination", use_container_width=True, key="mk_sub_b"):
                st.session_state.test_submitted = True
                st.session_state.time_taken_seconds = elapsed
                st.session_state.current_page = "Result"
                st.rerun()

    with col_control:
        draw_testbook_palette_slate()

    if not st.session_state.test_submitted:
        time.sleep(1.0)
        st.rerun()

def render_result_page():
    st.markdown("<div class='testbook-top-bar'><span>📊 Test Diagnostics & Performance Analytics Studio</span></div>", unsafe_allow_html=True)
    
    if not st.session_state.questions or not st.session_state.test_submitted:
        st.warning("No comprehensive test submission log contexts located to process scoring graphs.")
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
    final_pct = (correct / total_q) * 100
    
    st.write("---")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Extracted Assessment Items", total_q)
    m2.metric("Verified Valid Core Hits", correct)
    m3.metric("Error Variance Misses", wrong)
    m4.metric("Skipped/Bypassed Nodes", skipped)
    
    m5, m6, m7 = st.columns(3)
    m5.metric("Precision Accuracy Index", f"{accuracy:.2f}%")
    m6.metric("Weighted Score Percentage", f"{final_pct:.2f}%")
    m7.metric("Total Processing Runtime", str(timedelta(seconds=int(st.session_state.time_taken_seconds))))
    
    st.markdown("### 🏆 Estimated Platform Percentile Rank")
    st.info("Estimated Global Performance Index Tier: **Rank #1 / Mock Calibration Sandbox Leaderboard Baseline**")
    
    st.write("---")
    st.markdown("### 🔍 Granular Structural Question & Solution Matrix Breakdown")
    for idx, q in enumerate(st.session_state.questions):
        with st.expander(f"Question Number Record Item Analysis #{q['question_number']}"):
            st.markdown(f"**Question Text Node Context Content:** {q['question']}")
            st.write(f"A. {q['A']}")
            st.write(f"B. {q['B']}")
            st.write(f"C. {q['C']}")
            st.write(f"D. {q['D']}")
            
            is_correct = q["user_answer"] == q["correct_answer"]
            if q["user_answer"] is None:
                st.warning("Skipped Item: No selection matrix log input discovered.")
            elif is_correct:
                st.success("Result State: Correct Answer Node Match!")
            else:
                st.error(f"Result State: Mismatch. Correct Target Key is Option: {q['correct_answer']}")
            st.info(f"Verified Reference Sheet Target: Option {q['correct_answer']} | Registered Selection Log Node: {q['user_answer']}")

def render_settings_page():
    st.subheader("⚙️ Global Framework Architecture Settings")
    st.session_state.test_duration_minutes = st.number_input(
        "Modify Default Session Countdown limits span parameter (Minutes Allocation Bound Loop):",
        min_value=5, max_value=200, value=st.session_state.test_duration_minutes
    )
    st.success("Global config framework states modified securely.")

# ==========================================
# 6. APPLICATION ROUTER DESK INITIALIZER
# ==========================================
def main():
    apply_premium_testbook_css()
    init_session_state()
    
    st.sidebar.markdown("<h2 style='text-align:center; color:#005682; margin-top:0px;'>📝 Testbook Pro</h2>", unsafe_allow_html=True)
    st.sidebar.write("---")
    
    selected_portal_route = st.sidebar.radio(
        "Application Navigation Panel Selector Panel Matrix Route:",
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



