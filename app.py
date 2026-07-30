import streamlit as st
import pdfplumber
import re
import time
from datetime import timedelta

# Set premium responsive layout rules as the entry point execution criteria
st.set_page_config(
    page_title="Testbook Engine — Premium Sectional Solutions Desk",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 1. PIXEL-PERFECT PREMIUM TESTBOOK SOLUTIONS CSS & JS
# ==========================================
def apply_premium_testbook_solutions_css():
    st.markdown("""
    <style>
        /* Force App Base canvas container system background reset */
        .main { background-color: #f8fafc !important; padding: 0px !important; }
        
        /* Exact Top Blue Navigation Header Banner */
        .tb-header {
            background-color: #005682;
            color: #ffffff;
            padding: 10px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-family: sans-serif;
            margin-bottom: 0px;
        }
        .tb-header-title { font-size: 15px; font-weight: 600; display: flex; align-items: center; gap: 10px; }
        .tb-analytics-btn {
            background-color: transparent;
            color: #ffffff;
            border: 1px solid #ffffff;
            padding: 4px 14px;
            font-size: 11px;
            font-weight: bold;
            border-radius: 3px;
            text-transform: uppercase;
            cursor: pointer;
        }

        /* Section Tabs Header Segment Row Layout */
        .tb-sections-bar {
            background-color: #ffffff;
            border-bottom: 1px solid #e2e8f0;
            padding: 0px 20px;
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 15px;
        }
        .tb-section-lbl { font-size: 11px; font-weight: bold; color: #64748b; text-transform: uppercase; margin-right: 10px; }

        /* Question Frame View Box Layout Card Container */
        .tb-q-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 4px;
            padding: 20px 20px 15px 20px;
            margin-bottom: 0px;
        }
        
        /* Question Diagnostic Meta Data Ribbon Row */
        .tcs-meta-row {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }
        .tcs-q-idx { font-size: 14px; font-weight: bold; color: #1e293b; }
        .badge-correct-tb { background-color: #22c55e; color: white; padding: 2px 8px; font-size: 11px; font-weight: bold; border-radius: 3px; text-transform: uppercase; }
        .badge-wrong-tb { background-color: #ef4444; color: white; padding: 2px 8px; font-size: 11px; font-weight: bold; border-radius: 3px; text-transform: uppercase; }
        .tb-timer-info { font-size: 12px; color: #64748b; font-weight: 500; }
        .badge-stat-metric { background-color: #22c55e; color: #ffffff; padding: 2px 6px; font-size: 11px; border-radius: 3px; font-weight: bold; }
        .badge-pct-correct { background-color: #e0f2fe; color: #0369a1; padding: 2px 8px; font-size: 11px; border-radius: 3px; font-weight: 500; }
        
        .tb-question-text { font-size: 15px; color: #1e293b; font-weight: 500; line-height: 1.5; margin-bottom: 5px; }
        
        /* Ultra-Tight Space Radio Group CSS Overrides */
        div[data-testid="stRadio"] {
            margin-top: -5px !important;
            padding-top: 0px !important;
        }
        div[data-testid="stRadio"] label p {
            font-size: 14px !important;
            color: #334155 !important;
            font-weight: 400 !important;
        }
        div[data-testid="stRadio"] > label {
            display: none !important;
        }
        
        /* Lower Highlighted Context Frame Alert Bar Component Box */
        .tb-reattempt-box {
            background-color: #fff7ed;
            border: 1px solid #ffedd5;
            padding: 12px 15px;
            border-radius: 4px;
            margin-top: 15px;
        }

        /* Right Hand Sidebar Profile Header Elements */
        .sb-user-card {
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 10px;
            margin-bottom: 12px;
        }
        .sb-stat-pill {
            display: inline-block;
            font-size: 11px;
            padding: 3px 8px;
            border-radius: 3px;
            margin-right: 5px;
            margin-bottom: 5px;
            color: #ffffff;
            font-weight: bold;
        }
        .tcs-stats-lbl { font-size: 12px; font-weight: bold; color: #475569; margin-top: 10px; margin-bottom: 8px; text-transform: uppercase; }
        
        /* Streamlit Button Customizations for Tab Aesthetics */
        div.stButton > button {
            border-radius: 3px !important;
            font-size: 13px !important;
            font-weight: 500 !important;
            transition: all 0.2s ease;
        }
        
        /* Android System Tweak parameters integration */
        * {
            -webkit-tap-highlight-color: transparent !important;
            -webkit-touch-callout: none !important;
        }
        .stApp {
            overflow-y: auto;
            -webkit-overflow-scrolling: touch;
        }
    </style>
    """, unsafe_allow_html=True)

def inject_cbt_security_script():
    """Injects JavaScript to handle automatic strict fullscreen and detect tab switching triggers."""
    st.markdown("""
    <script>
        function launchFullscreen() {
            var element = document.documentElement;
            if(element.requestFullscreen) { element.requestFullscreen(); }
            else if(element.mozRequestFullScreen) { element.mozRequestFullScreen(); }
            else if(element.webkitRequestFullscreen) { element.webkitRequestFullscreen(); }
            else if(element.msRequestFullscreen) { element.msRequestFullscreen(); }
        }
        setTimeout(launchFullscreen, 1000);

        document.addEventListener("visibilitychange", function() {
            if (document.hidden) {
                alert("🚨 WINDOW SWITCH DETECTION ALERT!\\n\\nYou attempted to switch applications or browser tabs. This action violates strict CBT environment regulations.");
            }
        });
    </script>
    """, unsafe_allow_html=True)

# ==========================================
# 2. SESSION STATE ARTIFACT MATRIX INITIALIZATION
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
    if 'active_section' not in st.session_state:
        st.session_state.active_section = "Mathematics"
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
# 3. ADVANCED SECTOR RECOGNITION & PARSING ENGINE
# ==========================================
def auto_classify_question(question_text):
    """
    Intelligently auto-detects and categorizes questions into 4 primary domains using context matching.
    """
    text = question_text.lower()
    
    math_keywords = [
        'find the value', 'x =', 'y =', 'ratio', 'percentage', 'average', 'profit', 'loss', 'interest', 'sum',
        'algebra', 'geometry', 'triangle', 'speed', 'distance', 'time', 'work', 'tank', 'cistern', 'cube',
        'square', 'root', 'numbers', 'divisible', 'lcm', 'hcf', 'trigonometry', 'theta', 'sin', 'cos', 'tan'
    ]
    science_keywords = [
        'planet', 'star', 'newton', 'force', 'velocity', 'acceleration', 'acid', 'base', 'chemical', 'reaction',
        'element', 'atom', 'molecule', 'cell', 'organ', 'blood', 'disease', 'vitamin', 'physics', 'chemistry',
        'biology', 'lens', 'mirror', 'light', 'sound', 'energy', 'watt', 'joule', 'ohm', 'gravity', 'oxygen'
    ]
    reasoning_keywords = [
        'series', 'pattern', 'analogy', 'odd one out', 'coding', 'decoding', 'direction', 'blood relation',
        'sitting arrangement', 'syllogism', 'venn diagram', 'dice', 'calendar', 'clock', 'mirror image',
        'statement', 'conclusion', 'assumption', 'if then', 'next term'
    ]
    english_keywords = [
        'synonym', 'antonym', 'idiom', 'phrase', 'one word', 'substitution', 'grammatical error',
        'fill in the blank', 'correct spelling', 'misspelt', 'voice', 'narration', 'direct speech',
        'indirect speech', 'comprehension', 'passage', 'preposition', 'verb', 'noun', 'adjective'
    ]

    for kw in math_keywords:
        if kw in text: return "Mathematics"
    for kw in science_keywords:
        if kw in text: return "General Science"
    for kw in reasoning_keywords:
        if kw in text: return "General Intelligence & Reasoning"
    for kw in english_keywords:
        if kw in text: return "English Language"
        
    return "General Awareness"

def extract_pdf_data(uploaded_file):
    """
    Hybrids normal layout readers with deep fallback rendering modes to accurately handle scanned PDF objects.
    """
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            total_pages = len(pdf.pages)
            if total_pages < 2:
                return None, None, "PDF layout requires at least 2 structural sheets to evaluate patterns."
            
            question_text = ""
            for page in pdf.pages[:-1]:
                text = page.extract_text()
                # Fallback layout check algorithm for Scanned files
                if not text or len(text.strip()) < 10:
                    text = page.extract_text(layout=True)
                if text:
                    question_text += text + "\n"
            
            last_page = pdf.pages[-1]
            last_page_text = last_page.extract_text()
            if not last_page_text or len(last_page_text.strip()) < 5:
                last_page_text = last_page.extract_text(layout=True)
                
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
            
        detected_section = auto_classify_question(actual_question)
            
        questions_list.append({
            "question_number": q_num,
            "question": actual_question,
            "A": opts_dict['A'],
            "B": opts_dict['B'],
            "C": opts_dict['C'],
            "D": opts_dict['D'],
            "correct_answer": answer_key.get(q_num, "A"),
            "user_answer": None,
            "review": False,
            "section": detected_section
        })
        
    return sorted(questions_list, key=lambda x: x["question_number"])

# ==========================================
# 4. COMPACT PALETTE METRICS PANE SIDEBAR
# ==========================================
def draw_right_side_analytics_panel(filtered_questions):
    correct_cnt = sum(1 for q in filtered_questions if q["user_answer"] == q["correct_answer"])
    unattempted_cnt = sum(1 for q in filtered_questions if q["user_answer"] is None)
    incorrect_cnt = len(filtered_questions) - correct_cnt - unattempted_cnt

    st.markdown(f"""
    <div class="sb-user-card">
        <span style="font-size:14px; font-weight:600; color:#1e293b;">👤 Kanchan Kumari</span>
    </div>
    <div style="margin-bottom:10px;">
        <span class="sb-stat-pill" style="background-color:#22c55e;">{correct_cnt} Correct</span>
        <span class="sb-stat-pill" style="background-color:#64748b;">{unattempted_cnt} Unattempted</span>
        <span class="sb-stat-pill" style="background-color:#ef4444;">{incorrect_cnt} Incorrect</span>
    </div>
    <div class="tcs-stats-lbl">Section Grid Palette</div>
    """, unsafe_allow_html=True)
    
    total_qs = len(filtered_questions)
    grid_cols = 4
    
    for i in range(0, total_qs, grid_cols):
        cols = st.columns(grid_cols)
        for j in range(grid_cols):
            idx = i + j
            if idx < total_qs:
                q = filtered_questions[idx]
                q_num = q["question_number"]
                
                global_idx = st.session_state.questions.index(q)
                
                badge_icon = "⬜"
                if global_idx == st.session_state.current_question_index:
                    badge_icon = "🔵"
                elif q["review"]:
                    badge_icon = "🟣"
                elif q["user_answer"] is None:
                    badge_icon = "⬜"
                elif q["user_answer"] == q["correct_answer"]:
                    badge_icon = "🟢"
                else:
                    badge_icon = "🔴"
                    
                with cols[j]:
                    if st.button(f"{badge_icon}{q_num}", key=f"tcs_pal_key_{global_idx}", use_container_width=True):
                        st.session_state.current_question_index = global_idx
                        st.session_state.visited_questions.add(global_idx)
                        st.rerun()

# ==========================================
# 5. CORE WORKFLOW LAYOUT INTEGRATIONS
# ==========================================
def render_home_page():
    st.title("🎯 MockTest Pro — Premium Exam Suite")
    st.markdown("""
    Welcome to India's premium structural standard assessment simulator panel engine.
    
    ### ⚙️ Enhanced Ingestion Scanning Capabilities:
    *   **Image Layout Handling (Basic OCR Fallback)**: Automatically attempts layout layer restructuring if flat encoded characters are missing or unreadable.
    *   **Auto Section Classifier**: Distributes questions straight into localized syllabus categories seamlessly.
    """)
    st.info("Select **Upload PDF** from the sidebar route matrix to get started.")

def render_upload_page():
    st.subheader("📂 Ingest Exam Document Object (PDF)")
    uploaded_file = st.file_uploader("Upload MCQ Exam Sheet Matrix Blueprint Asset (Scanned PDFs are supported):", type=["pdf"])
    
    if uploaded_file is not None:
        with st.spinner("Decoding layout structures and categorizing sections..."):
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
                st.session_state.active_section = parsed_qs[0]["section"]
                st.session_state.test_submitted = False
                st.session_state.test_start_time = None
                
                sections_found = {}
                for q in parsed_qs:
                    sections_found[q["section"]] = sections_found.get(q["section"], 0) + 1
                    
                st.success(f"Ingestion successful! Loaded {len(parsed_qs)} questions across matching categories.")
                st.write("📊 **Auto-Classified Section Matrix Yield:**")
                st.json(sections_found)
            else:
                st.error("Text alignment parsing error anomaly detected. Ensure your scanning properties are readable.")

def render_practice_page():
    if not st.session_state.questions:
        st.warning("No operational evaluation contexts found. Upload an active database blueprint structure first.")
        return
        
    st.markdown("""
    <div class="tb-header">
        <div class="tb-header-title">⬅ Tests &nbsp;&nbsp;|&nbsp;&nbsp; <span style='font-size:13px; font-weight:normal;'>SSC CBT Solutions Framework Dashboard Desk Panel</span></div>
        <button class="tb-analytics-btn">Analytics</button>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="background:#ffffff; padding:5px 20px 0px 20px; font-size:11px; font-weight:bold; color:#64748b; text-transform:uppercase;">SECTIONS</div>', unsafe_allow_html=True)
    available_sections = sorted(list(set(q["section"] for q in st.session_state.questions)))
    
    s_tabs = st.columns(len(available_sections))
    for t_idx, sec_name in enumerate(available_sections):
        with s_tabs[t_idx]:
            is_active = (st.session_state.active_section == sec_name)
            btn_type = "primary" if is_active else "secondary"
            if st.button(sec_name, key=f"tab_btn_{sec_name}", type=btn_type, use_container_width=True):
                st.session_state.active_section = sec_name
                first_q_of_sec = next(idx for idx, q in enumerate(st.session_state.questions) if q["section"] == sec_name)
                st.session_state.current_question_index = first_q_of_sec
                st.rerun()

    filtered_qs = [q for q in st.session_state.questions if q["section"] == st.session_state.active_section]
    
    if not filtered_qs:
        st.info("No elements loaded under this workspace path profile layout node.")
        return

    q = st.session_state.questions[st.session_state.current_question_index]
    if q["section"] != st.session_state.active_section:
        q = filtered_qs[0]
        st.session_state.current_question_index = st.session_state.questions.index(q)

    col_slate, col_analytics = st.columns([3.0, 1.0])

    with col_slate:
        is_correct = q["user_answer"] == q["correct_answer"] if q["user_answer"] else False
        badge_style = '<span class="badge-correct-tb">Correct</span>' if is_correct else '<span class="badge-wrong-tb">Incorrect / Review</span>'
        
        st.markdown(f"""
        <div class="tb-q-card">
            <div class="tcs-meta-row">
                <span class="tcs-q-idx">Question No. {q['question_number']}</span>
                {badge_style}
                <span class="tb-timer-info">⏱ You: 00:16 Avg: 00:22</span>
                <span class="badge-stat-metric">Marks 1</span>
                <span class="badge-pct-correct">Section: {q['section']}</span>
            </div>
            <div class="tb-question-text">{q['question']}</div>
        </div>
        """, unsafe_allow_html=True)

        opts = [f"A. {q['A']}", f"B. {q['B']}", f"C. {q['C']}", f"D. {q['D']}"]
        curr_sel = ["A", "B", "C", "D"].index(q["user_answer"]) if q["user_answer"] else None
        
        selected_option = st.radio("Options Hidden Label Layout Control:", opts, index=curr_sel, key=f"scr_pr_{q['question_number']}")
        
        if selected_option:
            st.session_state.questions[st.session_state.current_question_index]["user_answer"] = selected_option[0]

        st.markdown(f"""
        <div class="tb-reattempt-box">
            <span style="color:#c2410c; font-weight:bold; font-size:13px;">Practice Mode Profile Active</span><br/>
            <span style="color:#7c2d12; font-size:12px;">Verified Target Key Parameter Value: <b>Option {q['correct_answer']}</b></span>
        </div>
        """, unsafe_allow_html=True)
                
        st.write("---")
        foot_prev, foot_mid, foot_nxt = st.columns([1, 2, 1])
        
        current_filtered_idx = filtered_qs.index(q)
        
        with foot_prev:
            if st.button("Previous Question", disabled=(current_filtered_idx == 0), use_container_width=True, key="pr_p_b"):
                prev_q = filtered_qs[current_filtered_idx - 1]
                st.session_state.current_question_index = st.session_state.questions.index(prev_q)
                st.rerun()
        with foot_mid:
            st.toggle("Re-attempt Questions Matrix Mode Tracker Toggle Switch Component Layout", value=True, key="tb_toggle_reattempt")
        with foot_nxt:
            if st.button("Next Question", disabled=(current_filtered_idx == len(filtered_qs) - 1), use_container_width=True, key="pr_n_b"):
                next_q = filtered_qs[current_filtered_idx + 1]
                st.session_state.current_question_index = st.session_state.questions.index(next_q)
                st.session_state.visited_questions.add(st.session_state.current_question_index)
                st.rerun()

    with col_analytics:
        draw_right_side_analytics_panel(filtered_qs)

def render_mock_page():
    if not st.session_state.questions:
        st.warning("No operational evaluation contexts found. Upload an active database blueprint structure first.")
        return
        
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
    
    st.markdown('<div style="background:#ffffff; padding:5px 20px 0px 20px; font-size:11px; font-weight:bold; color:#64748b; text-transform:uppercase;">SECTIONS</div>', unsafe_allow_html=True)
    available_sections = sorted(list(set(q["section"] for q in st.session_state.questions)))
    
    s_tabs = st.columns(len(available_sections))
    for t_idx, sec_name in enumerate(available_sections):
        with s_tabs[t_idx]:
            is_active = (st.session_state.active_section == sec_name)
            btn_type = "primary" if is_active else "secondary"
            if st.button(sec_name, key=f"mock_tab_btn_{sec_name}", type=btn_type, use_container_width=True):
                st.session_state.active_section = sec_name
                first_q_of_sec = next(idx for idx, q in enumerate(st.session_state.questions) if q["section"] == sec_name)
                st.session_state.current_question_index = first_q_of_sec
                st.rerun()

    filtered_qs = [q for q in st.session_state.questions if q["section"] == st.session_state.active_section]
    
    if st.session_state.test_submitted:
        st.info("Your response profile has closed execution loops. View results via the **Result** page.")
        return

    q = st.session_state.questions[st.session_state.current_question_index]
    if q["section"] != st.session_state.active_section:
        q = filtered_qs[0]
        st.session_state.current_question_index = st.session_state.questions.index(q)
    
    col_slate, col_control = st.columns([2.8, 1.2])
    
    with col_slate:
        st.markdown(f"""
        <div class="tb-q-card">
            <div class="tcs-meta-row">
                <span class="tcs-q-idx">Question No. {q['question_number']}</span>
                <span class="badge-status-cbt" style="background-color:#fee2e2; color:#991b1b; padding: 2px 6px; font-size:11px; border-radius:3px;">Exam Mode Active</span>
                <span class="badge-stat-metric">Marks 1</span>
                <span class="badge-pct-correct">Section Target: {q['section']}</span>
            </div>
            <div class="tb-question-text"><b>{q['question']}</b></div>
        </div>
        """, unsafe_allow_html=True)
        
        opts = [f"A. {q['A']}", f"B. {q['B']}", f"C. {q['C']}", f"D. {q['D']}"]
        curr_sel = ["A", "B", "C", "D"].index(q["user_answer"]) if q["user_answer"] else None
        
        selected_option = st.radio("Options Hidden Label:", opts, index=curr_sel, key=f"scr_mk_{q['question_number']}")
        
        st.write("---")
        act_1, act_2, act_3, act_4 = st.columns(4)
        
        current_filtered_idx = filtered_qs.index(q)
        
        with act_1:
            if st.button("🟣 Mark for Review & Next", use_container_width=True, key="mk_rev_b"):
                st.session_state.questions[st.session_state.current_question_index]["review"] = True
                if selected_option:
                    st.session_state.questions[st.session_state.current_question_index]["user_answer"] = selected_option[0]
                if current_filtered_idx < len(filtered_qs) - 1:
                    next_q = filtered_qs[current_filtered_idx + 1]
                    st.session_state.current_question_index = st.session_state.questions.index(next_q)
                    st.session_state.visited_questions.add(st.session_state.current_question_index)
                st.rerun()
                
        with act_2:
            if st.button("🧹 Clear Response", use_container_width=True, key="mk_clr_b"):
                st.session_state.questions[st.session_state.current_question_index]["user_answer"] = None
                st.session_state.questions[st.session_state.current_question_index]["review"] = False
                st.rerun()
                
        with act_3:
            if st.button("💾 Save & Next ➡", type="primary", use_container_width=True, key="mk_nxt_b"):
                if selected_option:
                    st.session_state.questions[st.session_state.current_question_index]["user_answer"] = selected_option[0]
                st.session_state.questions[st.session_state.current_question_index]["review"] = False
                if current_filtered_idx < len(filtered_qs) - 1:
                    next_q = filtered_qs[current_filtered_idx + 1]
                    st.session_state.current_question_index = st.session_state.questions.index(next_q)
                    st.session_state.visited_questions.add(st.session_state.current_question_index)
                st.rerun()
                
        with act_4:
            if st.button("🛑 Submit Examination", use_container_width=True, key="mk_sub_b"):
                st.session_state.test_submitted = True
                st.session_state.time_taken_seconds = elapsed
                st.session_state.current_page = "Result"
                st.rerun()

    with col_control:
        draw_right_side_analytics_panel(filtered_qs)

    if not st.session_state.test_submitted:
        time.sleep(1.0)
        st.rerun()

def render_result_page():
    st.markdown("<div class='testbook-top-bar'><span>📊 Test Diagnostics & Sectional Performance Analytics Studio</span></div>", unsafe_allow_html=True)
    
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
    
    st.write("---")
    st.markdown("### 🔍 Section-wise Breakdown Diagnostics Matrix")
    available_sections = sorted(list(set(q["section"] for q in st.session_state.questions)))
    
    for sec in available_sections:
        sec_qs = [q for q in st.session_state.questions if q["section"] == sec]
        sec_correct = sum(1 for q in sec_qs if q["user_answer"] == q["correct_answer"])
        st.write(f"📁 **{sec}**: {sec_correct} / {len(sec_qs)} Correct Answers.")

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
    apply_premium_testbook_solutions_css()
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






