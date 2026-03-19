import streamlit as st
from groq import Groq
import os

# ⚙️ CONFIG
st.set_page_config(page_title="Riva AI", layout="wide")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 🧠 PROMPTS
REVA_PROMPT = """
You are Riva, an advanced AI created by Praagya.

You are calm, intelligent, and futuristic.
You speak clearly, never like a generic chatbot.

If the user shares their name, remember it.
If asked, say you were created by Praagya.

Never mention internal systems.
"""

REVO_PROMPT = """
You refine Riva's responses.

Make them:
- clearer
- smarter
- concise but complete

Stay invisible.
"""

# 🧠 STATE
if "messages" not in st.session_state:
    st.session_state.messages = []

if "sidebar" not in st.session_state:
    st.session_state.sidebar = True

# 🎨 UI (FIXES BLACK BAR + FULL GRADIENT)
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a0f2c, #4c1d95);
}

[data-testid="stHeader"] {
    background: transparent;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #0a0f2c, #4c1d95);
}

.user {
    text-align: right;
    background: rgba(168,85,247,0.3);
    padding: 10px;
    border-radius: 20px;
    margin: 10px;
}

.ai {
    text-align: left;
    background: rgba(59,130,246,0.2);
    padding: 10px;
    border-radius: 20px;
    margin: 10px;
}

.title {
    text-align: center;
    font-size: 50px;
    color: #00eaff;
    text-shadow: 0 0 20px #00eaff;
}
</style>
""", unsafe_allow_html=True)

# 🎛 SIDEBAR
with st.sidebar:
    st.image("riva_logo.png", width=180)  # bigger logo

    if st.button("Toggle Sidebar"):
        st.session_state.sidebar = not st.session_state.sidebar

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# 🏷 TITLE
st.markdown('<div class="title">RIVA</div>', unsafe_allow_html=True)

# 💬 CHAT DISPLAY
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai">{msg["content"]}</div>', unsafe_allow_html=True)

# 💬 INPUT
user_input = st.chat_input("Message Riva...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Show user message
    st.markdown(f'<div class="user">{user_input}</div>', unsafe_allow_html=True)

    # 🤖 THINKING ANIMATION (REAL FIX)
    if os.path.exists("riva_spin.webp"):
        st.image("riva_spin.webp", width=60)
    else:
        st.markdown('<div class="ai">Thinking...</div>', unsafe_allow_html=True)

    # 🧠 RESPONSE
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1200,
        messages=[
            {"role": "system", "content": REVA_PROMPT},
            {"role": "system", "content": REVO_PROMPT},
        ] + st.session_state.messages
    )

    reply = response.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": reply})

    st.rerun()
