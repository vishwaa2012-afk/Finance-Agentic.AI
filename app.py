import os
import streamlit as st
from rag import load_and_ingest
from agent import ask_agent

# 1. Page Configuration
st.set_page_config(
    page_title="Solo LevelX | Investment Research",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Theme State Management
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

# 3. Clean Theme Palette (Warm Sunset Coral Accent + Green/Red Indicators)
if st.session_state.theme == "dark":
    bg_color = "#0B0F17"
    card_bg = "#1E293B"
    text_primary = "#F8FAFC"
    text_secondary = "#94A3B8"
    border_color = "#334155"
    btn_bg = "#EA580C"       # Deep Coral / Orange Sunset
    btn_hover = "#C2410C"
    accent_green = "#10B981" # Income/Positive
    accent_red = "#EF4444"   # Expense/Warning
else:
    bg_color = "#F8FAFC"
    card_bg = "#FFFFFF"
    text_primary = "#0F172A"
    text_secondary = "#64748B"
    border_color = "#E2E8F0"
    btn_bg = "#EA580C"       # Deep Coral / Orange Sunset
    btn_hover = "#C2410C"
    accent_green = "#059669"
    accent_red = "#DC2626"

# 4. Clean Custom Styling (No Upload Glitch)
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"], .stMarkdown, p, span, label {{
        font-family: 'Inter', -apple-system, sans-serif !important;
    }}

    .stApp {{
        background-color: {bg_color} !important;
        color: {text_primary} !important;
    }}

    .simple-card {{
        background-color: {card_bg};
        border: 1px solid {border_color};
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }}

    /* Main Action Buttons Only */
    div.stButton > button {{
        background-color: {btn_bg} !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 18px !important;
        transition: background-color 0.2s ease;
        width: 100%;
    }}

    div.stButton > button:hover {{
        background-color: {btn_hover} !important;
    }}

    .stTextArea textarea {{
        background-color: {card_bg} !important;
        color: {text_primary} !important;
        border: 1px solid {border_color} !important;
        border-radius: 8px !important;
    }}

    /* Reset File Uploader Internal Styles */
    [data-testid="stFileUploader"] {{
        background: transparent !important;
    }}

    [data-testid="stFileUploader"] button {{
        background-color: transparent !important;
        color: {text_primary} !important;
        border: 1px solid {border_color} !important;
        font-weight: 500 !important;
    }}

    /* Status Tags */
    .tag-green {{
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 600;
        background: rgba(16, 185, 129, 0.15);
        color: {accent_green};
        border: 1px solid rgba(16, 185, 129, 0.3);
    }}

    .tag-red {{
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 600;
        background: rgba(239, 68, 68, 0.15);
        color: {accent_red};
        border: 1px solid rgba(239, 68, 68, 0.3);
    }}
</style>
""", unsafe_allow_html=True)

# 5. Sidebar Controls
with st.sidebar:
    st.markdown("### ⚙️ Control Center")
    st.caption("Team Solo LevelX Engine")

    mode_text = "☀️ Light Mode" if st.session_state.theme == "dark" else "🌙 Dark Mode"
    st.button(mode_text, on_click=toggle_theme)

    st.divider()

    st.markdown("#### 📄 Document Knowledge Base")
    uploaded = st.file_uploader(
        "Upload Financial Reports (PDF)",
        type=["pdf"],
        accept_multiple_files=True,
    )

    if uploaded and st.button("Ingest Documents"):
        os.makedirs("documents", exist_ok=True)
        for file in uploaded:
            with open(f"documents/{file.name}", "wb") as f:
                f.write(file.getbuffer())

        with st.spinner("Processing embeddings..."):
            message = load_and_ingest()

        st.success(message)

    st.divider()
    st.markdown("#### 📊 System Specs")
    st.markdown(f"""
    <small style="color:{text_secondary};">
    • <b>LLM:</b> Llama 3.2 (3B Local)<br/>
    • <b>VectorDB:</b> ChromaDB<br/>
    • <b>Embeddings:</b> MiniLM-L6-v2<br/>
    • <b>Live Feed:</b> Yahoo Finance
    </small>
    """, unsafe_allow_html=True)

# 6. Header Banner
st.markdown(f"""
<div class="simple-card">
    <div style="font-size: 1.5rem; font-weight: 700; color: {text_primary}; margin-bottom: 4px;">
        Solo LevelX Investment Research Agent
    </div>
    <div style="font-size: 0.92rem; color: {text_secondary};">
        Grounded research copilot powered by local RAG and real-time market data
    </div>
    <div style="margin-top: 14px;">
        <span class="tag-green">● LIVE MARKET SYNC ACTIVE</span> &nbsp;
        <span class="tag-green">● RAG ENGINE READY</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Warning Disclaimer Card
st.markdown(f"""
<div style="border-left: 4px solid {accent_red}; background-color: {card_bg}; padding: 12px 16px; border-radius: 8px; margin-bottom: 20px;">
    <span class="tag-red">⚠️ DISCLAIMER</span> &nbsp;
    <span style="font-size: 0.88rem; color: {text_secondary};">
        Educational research tool only. Not personalized financial advice.
    </span>
</div>
""", unsafe_allow_html=True)

# 7. Quick Actions
st.markdown("#### 💡 Quick Actions")
col1, col2, col3 = st.columns(3)

quick_query = ""

if col1.button("📈 RELIANCE Live Price"):
    quick_query = "Get live stock snapshot for RELIANCE.NS"

if col2.button("📊 TCS Stock Snapshot"):
    quick_query = "Get live stock snapshot for TCS.NS"

if col3.button("📰 Recent Market News"):
    quick_query = "Get recent market news for Reliance"

# 8. Query Console
st.markdown("---")
st.markdown("#### 🔍 Research Query Console")

question = st.text_area(
    "Ask a question:",
    value=quick_query,
    placeholder="e.g. What is the current stock snapshot for RELIANCE.NS?",
    height=90
)

if st.button("Run Research Analysis"):
    if not question.strip():
        st.error("Please enter a question.")
    else:
        with st.spinner("Analyzing market data and documents..."):
            try:
                answer = ask_agent(question)
                st.markdown("### 📝 Research Report")
                st.markdown(f"""
                <div class="simple-card">
                    {answer}
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Agent error: {e}")