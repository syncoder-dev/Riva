import streamlit as st
from groq import Groq

# ⚙️ CONFIG
st.set_page_config(page_title="RIVA", layout="wide")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 🧠 STATE
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thinking" not in st.session_state:
    st.session_state.thinking = False

# 🎨 BACKGROUND + UI
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a192f, #6d28d9);
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
    background: rgba(168,85,247,0.3);
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
</style>
""", unsafe_allow_html=True)

# 🏷 LOGO
st.image("riva_logo.png", width=180)

# 🌀 AVATAR
if st.session_state.thinking:
    st.image("riva_spin.gif", width=100)
else:
    st.image("riva_avatar.png", width=100)

# 💬 CHAT DISPLAY
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

# 💬 INPUT
user_input = st.chat_input("Message RIVA...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 🔄 start animation
    st.session_state.thinking = True
    st.rerun()

# 🤖 RESPONSE
if st.session_state.thinking:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are Riva, calm, futuristic, slightly witty."}
        ] + st.session_state.messages
    )

    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})

    # 🧠 stop animation
    st.session_state.thinking = False
    st.rerun()
