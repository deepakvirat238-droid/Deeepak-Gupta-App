import streamlit as st
import pdfplumber
import re
import time
from datetime import timedelta

# Set premium responsive layout rules
st.set_page_config(
    page_title="Testbook Engine Panel",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 1. PIXEL-PERFECT TESTBOOK SOLUTIONS CSS
# ==========================================
def apply_testbook_solution_theme():
    st.markdown("""
    <style>
        /* Main canvas container reset */
        .main { background-color: #f8fafc !important; padding: 0px !important; }
        
        /* Top Navigation Header Banner */
        .tb-header {
            background-color: #005682;
            color: #ffffff;
            padding: 10px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-family: sans-serif;
        }
        .tb-header-title { font-size: 15px; font-weight: 600; }
        .tb-analytics-btn {
            background-color: transparent;
            color: #ffffff;
            border: 1px solid #ffffff;
            padding: 4px 12px;
            font-size: 12px;
            font-weight: bold;
            border-radius: 3px;
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
        }
        .tb-tab-inactive {
            color: #334155;
            padding: 8px 16px;
            font-size: 13px;
            cursor: pointer;
        }

        /* CBT Core Question Paper View Box Area */
        .tb-q-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 4px;
            padding: 20px;
            margin-top: 15px;
        }
        
        /* Question Information Ribbon Row (Badges Line) */
        .tb-meta-row {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }
        .tb-q-num { font-size: 15px; font-weight: bold; color: #1e293b; }
        .badge-correct { background-color: #22c55e; color: white; padding: 2px 8px; font-size: 11px; font-weight: bold; border-radius: 3px; }
        .badge-wrong { background-color: #ef4444; color: white; padding: 2px 8px; font-size: 11px; font-weight: bold; border-radius: 3px; }
        .tb-timer-info { font-size: 12px; color: #64748b; }
        .badge-stat { background-color: #dcfce7; color: #15803d; padding: 2px 6px; font-size: 11px; border-radius: 3px; font-weight: 500; }

        /* Exact Question Text Content configuration */
        .tb-question-text {
            font-size: 15px;
            color: #1e293b;
            font-weight: 500;
            line-height: 1.5;
            margin-bottom: 5px; /* Extremely small margin underneath question block */
        }

        /* Tight Radio Option padding framework adjustment */
        div[data-testid="stRadio"] {
            margin-top: -8px !important;
            padding-top: 0px !important;
        }
        div[data-testid="stRadio"] label p {
            font-size: 14px !important;
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

        /* Right Hand Analysis Sidebar Framework */
        .sb-user-card {
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 12px;
            margin-bottom: 12px;
        }
        .sb-stat-pill {
            display: inline-block;
            font-size: 11px;
            padding: 3px 6px;
            border-radius: 3px;
            margin-right: 5px;
            margin-bottom: 5px;
            color: #ffffff;
            font-weight: bold;
        }
        
        /* Bottom Sticky Execution Controls Footer Placement */
        .tb-footer-bar {
            background-color: #ffffff;
            border-top: 1px solid #e2e8f0;
            padding: 12px 20px;
            margin-top: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
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
    if 'test_submitted' not in st.session_state:
        st.session_state.test_submitted = False
    if 'visited_questions' not in st.session_state:
        st.session_state.visited_questions = set()

# ==========================================
# 3. HIGH ACCURACY PARSING SYSTEM
# ==========================================
def extract_pdf_data(uploaded_file):
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            if len(pdf.pages) < 2:
                return None, None, "PDF requires at least two sheets."
            q_text = ""
            for page in pdf.pages[:-1]:
                text = page.extract_text()
                if text:
                    q_text += text + "\n"
            last_page_text = pdf.pages[-1].extract_text()
            return q_text, last_page_text, None
    except Exception as e:
        return None, None, str(e)

def parse_answer_key(text):
    answers = {}
    if not text:
        return answers
    clean_text = re.sub(r'(ANSWER\s*KEY|Ans[:\s]*)', '', text, flags=re.IGNORECASE)
    pattern = re.compile(r'(\d+)\s*[\.\-\)\:\s]*\s*([A-E])', re.IGNORECASE)
    for num, option in pattern.findall(clean_text):
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
        opts_dict = {'A': 'Option Content A', 'B': 'Option Content B', 'C': 'Option Content C', 'D': 'Option Content D'}
        
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
            "user_answer": None
        })
    return sorted(questions_list, key=lambda x: x["question_number"])

# ==========================================
# 4. MOCK TEST PLATFORM COMPONENTS
# ==========================================
def draw_right_side_analytics_panel():
    # Performance status count logic
    correct_cnt = sum(1 for q in st.session_state.questions if q["user_answer"] == q["correct_answer"])
    unattempted_cnt = sum(1 for q in st.session_state.questions if q["user_answer"] is None)
    incorrect_cnt = len(st.session_state.questions) - correct_cnt - unattempted_cnt

    st.markdown(f"""
    <div class="sb-user-card">
        <span style="font-size:14px; font-weight:600; color:#334155;">👤 Kanchan Kumari</span>
    </div>
    <div style="margin-bottom:10px;">
        <span class="sb-stat-pill" style="background-color:#22c55e;">{correct_cnt} Correct</span>
        <span class="sb-stat-pill" style="background-color:#64748b;">{unattempted_cnt} Unattempted</span>
        <span class="sb-stat-pill" style="background-color:#ef4444;">{incorrect_cnt} Incorrect</span>
    </div>
    <div style="font-size:12px; font-weight:bold; margin-bottom:10px; color:#475569; border-top:1px solid #f1f5f9; padding-top:8px;">SECTION : General Science</div>
    """, unsafe_allow_html=True)
    
    total_qs = len(st.session_state.questions)
    grid_cols = 4
    
    for i in range(0, total_qs, grid_cols):
        cols = st.columns(grid_cols)
        for j in range(grid_cols):
            idx = i + j
            if idx < total_qs:
                q = st.session_state.questions[idx]
                q_num = q["question_number"]
                
                # Dynamic coloration setup mirroring active status grids
                badge_icon = "⬜"
                if idx == st.session_state.current_question_index:
                    badge_icon = "🔵"
                elif q["user_answer"] is None:
                    badge_icon = "⬜"
                elif q["user_answer"] == q["correct_answer"]:
                    badge_icon = "🟢"
                else:
                    badge_icon = "🔴"
                    
                with cols[j]:
                    if st.button(f"{badge_icon}{q_num}", key=f"tcs_pal_key_{idx}", use_container_width=True):
                        st.session_state.current_question_index = idx
                        st.session_state.visited_questions.add(idx)
                        st.rerun()

def render_exam_sandbox():
    if not st.session_state.questions:
        st.warning("No active configurations found. Load data sets using the **Upload PDF** section link.")
        return

    # 1. Exact Top Header Mockup Component Injected
    st.markdown("""
    <div class="tb-header">
        <div class="tb-header-title">⬅ Tests &nbsp;&nbsp;|&nbsp;&nbsp; <span style='font-size:13px; font-weight:normal;'>RRB Group D: Morning Practice Mock</span></div>
        <button class="tb-analytics-btn">ANALYTICS</button>
    </div>
    """, unsafe_allow_html=True)

    # 2. Section Segment Tabs Row Mockup Injected
    st.markdown("""
    <div class="tb-sections-bar">
        <span class="tb-section-lbl">Sections</span>
        <span class="tb-tab-active">General Science</span>
        <span class="tb-tab-inactive">Mathematics</span>
        <span class="tb-tab-inactive">General Intelligence</span>
    </div>
    """, unsafe_allow_html=True)

    q_idx = st.session_state.current_question_index
    q = st.session_state.questions[q_idx]

    # Split-Screen layout forced configuration wrapper
    col_slate, col_analytics = st.columns([3.0, 1.0])

    with col_slate:
        # Dynamic calculation metrics parameters
        is_correct = q["user_answer"] == q["correct_answer"] if q["user_answer"] else False
        badge_style = '<span class="badge-correct">Correct</span>' if is_correct else '<span class="badge-wrong">Incorrect / Review</span>'
        
        st.markdown(f"""
        <div class="tb-q-card">
            <div class="tb-meta-row">
                <span class="tb-q-num">Question No. {q['question_number']}</span>
                {badge_style}
                <span class="tb-timer-info">⏱ You: 00:16 Avg: 00:22</span>
                <span class="badge-stat">Marks 1</span>
                <span class="badge-stat" style="background-color:#e0f2fe; color:#0369a1;">72% answered correctly</span>
            </div>
            <div class="tb-question-text">{q['question']}</div>
        </div>
        """, unsafe_allow_html=True)

        opts = [f"A. {q['A']}", f"B. {q['B']}", f"C. {q['C']}", f"D. {q['D']}"]
        curr_selection = ["A", "B", "C", "D"].index(q["user_answer"]) if q["user_answer"] else None
        
        selected_option = st.radio("Options Slate Wrapper Hidden Label", opts, index=curr_selection, key=f"tb_r_{q_idx}")

        if selected_option:
            st.session_state.questions[q_idx]["user_answer"] = selected_option[0]

        # Ingestion of the lower grey "Re-attempt Mode" panel component inside workspace card
        st.markdown(f"""
        <div class="tb-reattempt-box">
            <span style="color:#c2410c; font-weight:bold; font-size:13px;">Re-attempt mode: ON</span><br/>
            <span style="color:#7c2d12; font-size:12px;">Now You can re-attempt the question dynamically. Verified Reference Sheet Target Coordinate Key is <b>Option {q['correct_answer']}</b></span>
        </div>
        """, unsafe_allow_html=True)

        # Bottom Core Execution Action Button Blocks Matrix Controls Footer Placement Container Node
        st.write("---")
        foot_prev, foot_mid, foot_nxt = st.columns([1, 2, 1])
        with foot_prev:
            if st.button("Previous Question", disabled=(q_idx == 0), use_container_width=True, key="tb_ft_prev"):
                st.session_state.current_question_index -= 1
                st.rerun()
        with foot_mid:
            st.toggle("Re-attempt Questions Options Filter Scope Matrix Mode", value=True, key="tb_toggle_reattempt")
        with foot_nxt:
            if st.button("Next Question", disabled=(q_idx == len(st.session_state.questions) - 1), use_container_width=True, key="tb_ft_nxt"):
                st.session_state.current_question_index += 1
                st.session_state.visited_questions.add(st.session_state.current_question_index)
                st.rerun()

    with col_analytics:
        draw_right_side_analytics_panel()

# ==========================================
# 5. WORKFLOW INGESTION PAGES ROUTER
# ==========================================
def render_home_page():
    st.title("🎯 MockTest Pro — Premium Ingestion Framework")
    st.markdown("Select **Upload PDF** from the sidebar controls panel menu matrix to load files.")

def render_upload_page():
    st.subheader("📂 Ingest Exam Sheets Matrix Data (PDF Document Object Asset Format)")
    uploaded_file = st.file_uploader("Choose File Target Blueprint:", type=["pdf"])
    
    if uploaded_file is not None:
        with st.spinner("Decoding internal page data lines..."):
            q_text, ans_text, error = extract_pdf_data(uploaded_file)
            if error:
                st.error(error)
                return
            ans_key = parse_answer_key(ans_text)
            parsed_qs = parse_questions(q_text, ans_key)
            
            if parsed_qs:
                st.session_state.questions = parsed_qs
                st.session_state.answer_key = ans_key
                st.session_state.visited_questions = {0}
                st.session_state.current_question_index = 0
                st.session_state.test_submitted = True
                st.success(f"Ingestion successful! Loaded {len(parsed_qs)} questions inside computational matrices.")
            else:
                st.error("Regex capture fault sequence identifier mismatch.")

# ==========================================
# 6. ROUTER ENTRY Initializer
# ==========================================
def main():
    apply_testbook_solution_theme()
    init_session_state()
    
    st.sidebar.markdown("<h3 style='text-align:center; color:#005682;'>📝 Dashboard</h3>", unsafe_allow_html=True)
    navigation_panel_selection = st.sidebar.radio("Routes Hub Selector:", ["Home", "Upload PDF", "Exam Board View Engine"])
    
    if navigation_panel_selection == "Home":
        render_home_page()
    elif navigation_panel_selection == "Upload PDF":
        render_upload_page()
    elif navigation_panel_selection == "Exam Board View Engine":
        render_exam_sandbox()

if __name__ == "__main__":
    main()

