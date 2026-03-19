import streamlit as st
from groq import Groq
import uuid

# ⚙️ CONFIG
st.set_page_config(page_title="Riva AI", layout="wide")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 🧠 MULTI CHAT MEMORY
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat" not in st.session_state:
    chat_id = str(uuid.uuid4())
    st.session_state.current_chat = chat_id
    st.session_state.chats[chat_id] = []

# 🎨 UI STYLE
st.markdown("""
<style>

/* BACKGROUND */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a0f2c, #4c1d95);
    color: white;
}

/* REMOVE HEADER */
[data-testid="stHeader"] {
    background: transparent;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: rgba(10,15,44,0.8);
    backdrop-filter: blur(20px);
}

/* GLOW TEXT */
.glow-title {
    font-size: 42px;
    font-weight: bold;
    color: #7dd3fc;
    text-align: center;
    text-shadow:
        0 0 5px #38bdf8,
        0 0 10px #38bdf8,
        0 0 20px #0ea5e9;
}

/* CHAT BUBBLES */
.user-bubble {
    background: rgba(168,85,247,0.35);
    padding: 12px 16px;
    margin: 10px 0;
    border-radius: 20px;
    text-align: right;
}

.ai-bubble {
    background: rgba(59,130,246,0.25);
    padding: 12px 16px;
    margin: 10px 0;
    border-radius: 20px;
    text-align: left;
}

/* INPUT */
div[data-testid="stChatInput"] {
    background: rgba(255,255,255,0.08) !important;
    backdrop-filter: blur(20px);
    border-radius: 30px !important;
}

textarea {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# 🧩 SIDEBAR (LOGO + CHATS)
with st.sidebar:

    st.image("riva_logo.png", width=120)

    st.markdown(
        '<div class="glow-title">Riva</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ➕ NEW CHAT
    if st.button("➕ New Chat"):
        new_id = str(uuid.uuid4())
        st.session_state.chats[new_id] = []
        st.session_state.current_chat = new_id
        st.rerun()

    st.markdown("### Chats")

    # LIST CHATS
    for chat_id in st.session_state.chats:
        if st.button(f"Chat {chat_id[:5]}", key=chat_id):
            st.session_state.current_chat = chat_id
            st.rerun()

# 🧠 CURRENT CHAT
messages = st.session_state.chats[st.session_state.current_chat]

# 💬 DISPLAY CHAT
for msg in messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

# 💬 INPUT
user_input = st.chat_input("Message Riva...")

if user_input:
    messages.append({"role": "user", "content": user_input})

    # 🌀 CUSTOM THINKING (NO STREAMLIT SPINNER)
    thinking_placeholder = st.empty()

    thinking_placeholder.markdown(
        """
        <div style="text-align:center;">
            <img src="riva_spin.gif" width="100">
            <p style="color:#7dd3fc;">Riva is thinking...</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 🤖 AI RESPONSE
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are Riva, calm, futuristic, slightly witty."}
        ] + messages
    )

    reply = response.choices[0].message.content

    thinking_placeholder.empty()

    messages.append({"role": "assistant", "content": reply})

    st.rerun()
