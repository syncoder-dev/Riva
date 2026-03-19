import streamlit as st
from groq import Groq
import time

# ⚙️ CONFIG
st.set_page_config(page_title="Riva AI", layout="wide")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 🧠 MEMORY
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🎨 CSS
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #6d28d9, #0f172a);
    color: white;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding: 2rem;
}

/* CHAT */
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

/* AVATAR */
.avatar {
    display: flex;
    justify-content: center;
    margin-bottom: 10px;
}

.avatar img {
    width: 90px;
}

/* ANIMATION */
.thinking {
    animation: spin 1.5s linear infinite, pulse 1.5s ease-in-out infinite;
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

# 🏷 TITLE
st.title("RIVA")

# 🌀 AVATAR PLACEHOLDER
avatar_placeholder = st.empty()

# default avatar
avatar_placeholder.markdown(
    '<div class="avatar"><img src="riva_avatar.png"></div>',
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
    # add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 🔄 show animation BEFORE API call
    avatar_placeholder.markdown(
        '<div class="avatar"><img src="riva_avatar.png" class="thinking"></div>',
        unsafe_allow_html=True
    )

    # small delay so animation is visible (important!)
    time.sleep(0.3)

    # 🤖 API CALL
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are Riva, calm, futuristic, slightly witty."}
        ] + st.session_state.messages
    )

    reply = response.choices[0].message.content

    # save response
    st.session_state.messages.append({"role": "assistant", "content": reply})

    # rerun to update UI
    st.rerun()
