import streamlit as st
from groq import Groq

# ⚙️ PAGE CONFIG
st.set_page_config(page_title="Riva AI", layout="wide")

# 🔑 API
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 🧠 MEMORY
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🎨 CLEAN UI
st.markdown("""
<style>

/* 🌊 BACKGROUND */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0ea5a4, #60a5fa);
}

/* REMOVE HEADER */
[data-testid="stHeader"] {
    background: transparent;
}

/* MAIN */
.block-container {
    padding: 2rem;
}

/* CHAT BUBBLES */
.user {
    background: rgba(168,85,247,0.25);
    padding: 12px;
    margin: 10px 0;
    border-radius: 18px;
    text-align: right;
    color: white;
}

.ai {
    background: rgba(255,255,255,0.2);
    padding: 12px;
    margin: 10px 0;
    border-radius: 18px;
    text-align: left;
    color: white;
}

/* INPUT FIX */
[data-testid="stChatInput"] {
    background: rgba(255,255,255,0.15) !important;
    border-radius: 25px !important;
    padding: 8px !important;
}

/* TEXTAREA */
[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: white !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.1);
}

</style>
""", unsafe_allow_html=True)

# 📌 SIDEBAR (simple, no hacks)
with st.sidebar:
    st.title("⚙️ Riva")
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# 🏷 TITLE
st.title("🤖 Riva AI")

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

    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
