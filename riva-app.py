import streamlit as st
from groq import Groq

# ⚙️ CONFIG
st.set_page_config(page_title="Riva AI", layout="wide")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 🧠 MEMORY
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🎨 UI + ANIMATION CSS
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #6d28d9, #0f172a);
    color: white;
}

[data-testid="stHeader"] {
    background: transparent;
}

section[data-testid="stSidebar"] {
    background: rgba(15,23,42,0.6);
    backdrop-filter: blur(20px);
}

.block-container {
    padding: 2rem;
}

/* 💬 CHAT */
.user-bubble {
    background: rgba(168,85,247,0.35);
    padding: 12px 16px;
    margin: 10px 0;
    border-radius: 20px;
    text-align: right;
    animation: fadeIn 0.3s ease;
}

.ai-bubble {
    background: rgba(59,130,246,0.25);
    padding: 12px 16px;
    margin: 10px 0;
    border-radius: 20px;
    text-align: left;
    animation: fadeIn 0.3s ease;
}

/* INPUT */
div[data-testid="stChatInputContainer"] {
    background: transparent !important;
}

div[data-testid="stChatInput"] {
    background: rgba(255,255,255,0.08) !important;
    backdrop-filter: blur(20px);
    border-radius: 30px !important;
    border: 1px solid rgba(255,255,255,0.2);
    padding: 10px !important;
}

div[data-testid="stChatInput"] textarea {
    color: white !important;
    background: transparent !important;
}

textarea::placeholder {
    color: rgba(255,255,255,0.5) !important;
}

/* ✨ ANIMATION */
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}

/* 🌀 AVATAR */
.riva-avatar {
    display: flex;
    justify-content: center;
    margin-bottom: 10px;
}

.riva-avatar img {
    width: 90px;
}

/* 🔄 THINKING */
.thinking {
    animation: spin 2s linear infinite, pulse 2s ease-in-out infinite;
}

@keyframes spin {
    from {transform: rotate(0deg);}
    to {transform: rotate(360deg);}
}

@keyframes pulse {
    0% {transform: scale(1);}
    50% {transform: scale(1.1);}
    100% {transform: scale(1);}
}
</style>
""", unsafe_allow_html=True)

# 🎛 SIDEBAR
with st.sidebar:
    st.title("⚙️ Riva")
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# 🏷 TITLE + AVATAR
st.title("RIVA")

avatar_placeholder = st.empty()
avatar_placeholder.markdown(
    '<div class="riva-avatar"><img src="riva_avatar.png"></div>',
    unsafe_allow_html=True
)

# 💬 CHAT DISPLAY
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

# 💬 INPUT
user_input = st.chat_input("Message Riva...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 🔄 START ANIMATION
    avatar_placeholder.markdown(
        '<div class="riva-avatar"><img src="riva_avatar.png" class="thinking"></div>',
        unsafe_allow_html=True
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are Riva, calm, futuristic, slightly witty."}
        ] + st.session_state.messages
    )

    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})

    # 🧠 STOP ANIMATION
    avatar_placeholder.markdown(
        '<div class="riva-avatar"><img src="riva_avatar.png"></div>',
        unsafe_allow_html=True
    )

    st.rerun()
