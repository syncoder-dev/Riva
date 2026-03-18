import streamlit as st
from groq import Groq

# 🧠 SIDEBAR STATE
if "sidebar" not in st.session_state:
    st.session_state.sidebar = True

# ⚙️ PAGE CONFIG (ONLY ONCE, TOP)
st.set_page_config(
    page_title="Riva AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded" if st.session_state.sidebar else "collapsed"
)

# 🔑 GROQ CLIENT
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 💬 CHAT MEMORY
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🎛 TOP BAR (ALWAYS VISIBLE)
col1, col2 = st.columns([1, 10])

with col1:
    if st.button("☰"):
        st.session_state.sidebar = not st.session_state.sidebar
        st.rerun()

with col2:
    st.markdown("<h1 style='margin:0;'>🤖 Riva AI</h1>", unsafe_allow_html=True)

# 🎨 CLEAN GLASS UI
st.markdown("""
<style>

/* 🌊 BACKGROUND */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0ea5a4, #60a5fa) !important;
}

/* 🧊 GLASS OVERLAY */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    inset: 0;
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(40px);
    z-index: 0;
}

/* MAIN */
.block-container {
    position: relative;
    z-index: 1;
    padding: 2rem;
}

/* REMOVE DEFAULT WHITE */
[data-testid="stHeader"] {
    background: transparent !important;
}

/* ROUND EVERYTHING */
* {
    border-radius: 18px !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.08) !important;
    backdrop-filter: blur(20px);
}

/* USER BUBBLE */
.user-bubble {
    background: rgba(168, 85, 247, 0.25);
    border: 1px solid rgba(255,255,255,0.2);
    padding: 14px 18px;
    max-width: 70%;
    margin-left: auto;
    margin-top: 10px;
    color: white;
    backdrop-filter: blur(12px);
}

/* AI BUBBLE */
.ai-bubble {
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.2);
    padding: 14px 18px;
    max-width: 70%;
    margin-right: auto;
    margin-top: 10px;
    color: white;
    backdrop-filter: blur(12px);
}

/* 💬 CHAT INPUT FULL FIX */
[data-testid="stChatInput"] {
    background: rgba(255,255,255,0.12) !important;
    backdrop-filter: blur(20px);
    border-radius: 30px !important;
    padding: 10px !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
}

/* INNER */
[data-testid="stChatInput"] > div {
    background: transparent !important;
}

/* TEXTAREA */
[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: white !important;
    border: none !important;
    outline: none !important;
}

/* REMOVE SHADOW */
[data-testid="stChatInput"] * {
    box-shadow: none !important;
}

/* BUTTON */
button {
    border-radius: 30px !important;
    background: rgba(255,255,255,0.2) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
}

</style>
""", unsafe_allow_html=True)

# 📌 SIDEBAR CONTENT
with st.sidebar:
    st.title("⚙️ Riva Control")
    st.write("Your AI assistant")

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# 💬 DISPLAY CHAT
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

# 💬 INPUT
user_input = st.chat_input("Message Riva...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Riva is thinking..."):
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=st.session_state.messages
        )

        reply = response.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": reply})

    st.rerun(),
