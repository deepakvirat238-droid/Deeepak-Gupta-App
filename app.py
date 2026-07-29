import streamlit as st

st.set_page_config(
    page_title="MockTest Pro",
    page_icon="📝",
    layout="wide"
)

st.sidebar.title("📝 MockTest Pro")

page = st.sidebar.radio(
    "Navigation",
    [
        "📂 Upload PDF",
        "🎯 Practice Mode",
        "📝 Mock Test",
        "📊 Result",
        "⚙ Settings"
    ]
)

if page == "📂 Upload PDF":
    st.title("📂 Upload PDF")
    st.write("Upload your MCQ PDF to create a test.")

elif page == "🎯 Practice Mode":
    st.title("🎯 Practice Mode")
    st.info("No PDF loaded.")

elif page == "📝 Mock Test":
    st.title("📝 Mock Test")
    st.info("No PDF loaded.")

elif page == "📊 Result":
    st.title("📊 Result")
    st.info("No result available.")

elif page == "⚙ Settings":
    st.title("⚙ Settings")
    st.info("Settings page.")
