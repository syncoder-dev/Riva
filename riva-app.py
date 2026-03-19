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
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a0f2c, #4c1d95);
    color: white;
}

[data-testid="stHeader"] {
    background: transparent;
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

/* INPUT BOX */
div[data-testid="stChatInput"] {
    background: rgba(255,255,255,0.08) !important;
    backdrop-filter: blur(20px);
    border-radius: 30px !important;
    border: 1px solid rgba(255,255,255,0.2);
}

textarea {
    color: white !important;
}

/* CENTER ELEMENTS */
.center {
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# 🏷 HEADER (LOGO + TITLE)
st.markdown('<div class="center">', unsafe_allow_html=True)

st.image("riva_logo.png", width=120)

st.markdown("<h1>Riva</h1>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 💬 CHAT DISPLAY
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

# 💬 INPUT
user_input = st.chat_input("Message Riva...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 🌀 SHOW SPINNING AVATAR WHILE THINKING
    with st.spinner("Riva is thinking..."):
        st.markdown(
            """
            <div style="text-align:center;">
                <img src="riva_spin.gif" width="100">
            </div>
            """,
            unsafe_allow_html=True
        )

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are Riva, calm, futuristic, slightly witty."}
            ] + st.session_state.messages
        )

        reply = response.choices[0].message.content

    # Add AI response
    st.session_state.messages.append({"role": "assistant", "content": reply})

    st.rerun()

# ⚙️ SIDEBAR
with st.sidebar:
    st.title("⚙️ Riva")

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()
