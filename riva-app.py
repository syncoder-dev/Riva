import streamlit as st
from groq import Groq

# 🔧 CONFIG
st.set_page_config(page_title="Riva AI", layout="wide")

# 🔑 API
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 🧠 MEMORY
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🎨 UI STYLE
st.markdown("""
<style>

/* 🌊 BACKGROUND */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0ea5a4, #60a5fa);
    color: white;
}

/* REMOVE HEADER */
[data-testid="stHeader"] {
    background: transparent;
}

/* MAIN PADDING */
.block-container {
    padding: 2rem;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.08);
}

/* CHAT BUBBLES */
.user {
    background: rgba(168,85,247,0.35);
    padding: 12px;
    margin: 10px 0;
    border-radius: 20px;
    text-align: right;
}

.ai {
    background: rgba(255,255,255,0.25);
    padding: 12px;
    margin: 10px 0;
    border-radius: 20px;
    text-align: left;
}

/* 💥 REMOVE BLACK BAR */
div[data-testid="stChatInputContainer"] {
    background: transparent !important;
}

div[data-testid="stBottom"] {
    background: transparent !important;
}

/* 💎 INPUT BOX */
div[data-testid="stChatInput"] {
    background: rgba(255,255,255,0.08) !important;
    backdrop-filter: blur(20px);
    border-radius: 30px !important;
    padding: 10px !important;
    border: 1px solid rgba(255,255,255,0.2);
}

/* TEXT INPUT */
div[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: white !important;
}

/* PLACEHOLDER TEXT */
textarea::placeholder {
    color: rgba(255,255,255,0.6) !important;
}

</style>
""", unsafe_allow_html=True)

# 📌 SIDEBAR
with st.sidebar:
    st.title("⚙️ Riva")
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# 🏷 TITLE
st.title("🤖 Riva AI")

# 💬 DISPLAY CHAT (NO SYSTEM MESSAGES)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user">{msg["content"]}</div>', unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f'<div class="ai">{msg["content"]}</div>', unsafe_allow_html=True)

# 💬 INPUT
user_input = st.chat_input("Message Riva...")

if user_input:
    # save user msg
    st.session_state.messages.append({"role": "user", "content": user_input})

    # system prompt (hidden)
    messages_for_api = [
        {"role": "system", "content": "You are Riva, a futuristic, calm, slightly witty AI assistant."}
    ] + st.session_state.messages

    # 🤖 API CALL
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages_for_api
        )
        reply = response.choices[0].message.content

    # save AI reply
    st.session_state.messages.append({"role": "assistant", "content": reply})

    st.rerun()
