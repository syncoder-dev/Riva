import streamlit as st
from groq import Groq

# 🔑 API
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 🧠 MEMORY
if "messages" not in st.session_state:
    st.session_state.messages = []

if "sidebar" not in st.session_state:
    st.session_state.sidebar = True

# 🎛 SIDEBAR TOGGLE BUTTON
if st.button("☰"):
    st.session_state.sidebar = not st.session_state.sidebar

if not st.session_state.sidebar:
    st.markdown('<div class="sidebar-collapsed">', unsafe_allow_html=True)

# 🎨 UI CSS
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

/* REMOVE WHITE */
[data-testid="stHeader"] {
    background: transparent !important;
}

/* MAIN */
.block-container {
    position: relative;
    z-index: 1;
    padding: 2rem;
}

/* ROUND EVERYTHING */
* {
    border-radius: 18px !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.08) !important;
    backdrop-filter: blur(20px);
    transition: all 0.3s ease;
}

/* SIDEBAR HIDE */
.sidebar-collapsed section[data-testid="stSidebar"] {
    margin-left: -300px;
}

/* USER BUBBLE */
.user-bubble {
    background: rgba(168, 85, 247, 0.25);
    border: 1px solid rgba(255,255,255,0.2);
    padding: 14px 18px;
    max-width: 70%;
    margin-left: auto;
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
    color: white;
    backdrop-filter: blur(12px);
}

/* INPUT */
textarea {
    background: rgba(255,255,255,0.15) !important;
    border-radius: 30px !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    color: white !important;
    padding: 14px !important;
}

/* BUTTON */
button {
    border-radius: 30px !important;
    background: rgba(255,255,255,0.2) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
}

/* TITLE */
h1 {
    color: white;
    text-align: center;
}

[data-testid="stChatInput"] {
    background: transparent !important;
}

</style>
""", unsafe_allow_html=True)

# 📌 SIDEBAR CONTENT
with st.sidebar:
    st.title("⚙️ Riva Control")
    st.write("Your futuristic assistant")

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# 🏷 TITLE
st.title("🤖 Riva AI")

# 💬 DISPLAY CHAT
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

# 💬 INPUT
user_input = st.chat_input("Message Riva...")

if user_input:
    # save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # display user
    st.markdown(f'<div class="user-bubble">{user_input}</div>', unsafe_allow_html=True)

    # 🤖 AI RESPONSE
    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=st.session_state.messages
    )

    reply = response.choices[0].message.content

    # save AI message
    st.session_state.messages.append({"role": "assistant", "content": reply})

    # display AI
    st.markdown(f'<div class="ai-bubble">{reply}</div>', unsafe_allow_html=True)

# CLOSE SIDEBAR DIV
if not st.session_state.sidebar:
    st.markdown('</div>', unsafe_allow_html=True)
