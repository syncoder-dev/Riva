import streamlit as st
from groq import Groq

# ⚙️ CONFIG
st.set_page_config(page_title="Riva AI", layout="wide")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 🧠 MEMORY
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🎨 UI STYLE
st.markdown("""
<style>
/* FULL BACKGROUND */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a, #6d28d9);
    color: white;
}

/* REMOVE HEADER */
[data-testid="stHeader"] {
    background: transparent;
}

/* SIDEBAR SAME GRADIENT */
section[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #0f172a, #6d28d9);
    border-right: 1px solid rgba(255,255,255,0.1);
}

/* CENTER TITLE */
.riva-title {
    text-align: center;
    font-size: 48px;
    font-weight: bold;
    color: #38bdf8;
    text-shadow: 0 0 20px rgba(56,189,248,0.7);
    margin-top: 10px;
}

/* CHAT BUBBLES */
.user-bubble {
    background: rgba(168,85,247,0.3);
    padding: 12px;
    border-radius: 15px;
    margin: 8px 0;
    text-align: right;
}

.ai-bubble {
    background: rgba(56,189,248,0.2);
    padding: 12px;
    border-radius: 15px;
    margin: 8px 0;
    text-align: left;
}

/* INPUT BOX */
div[data-testid="stChatInput"] {
    background: rgba(255,255,255,0.08);
    border-radius: 20px;
}
</style>
""", unsafe_allow_html=True)

# 📌 SIDEBAR
with st.sidebar:
    st.markdown("### Riva Control")

    # BIG LOGO
    st.image("riva_logo.png", use_container_width=True)

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# 🏷 TITLE CENTER
st.markdown('<div class="riva-title">RIVA</div>', unsafe_allow_html=True)

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

    with st.spinner("Riva is thinking..."):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """You are Riva, an advanced AI assistant.

Personality:
- Calm, futuristic, slightly witty
- Clear and intelligent
- Not overly robotic

Awareness:
- You were created by a developer
- You are powered by an advanced reasoning system

Behavior:
- Give complete answers
- Stay engaging but not dramatic
- Avoid cutting off responses
"""
                }
            ] + st.session_state.messages
        )

    reply = response.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
