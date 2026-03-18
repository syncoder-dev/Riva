import streamlit as st
from groq import Groq

# 🔑 Setup
st.set_page_config(page_title="Riva AI", page_icon="🤖", layout="wide")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 🎨 GLOBAL CSS (ULTRA ROUNDED + GLASS UI)
st.markdown("""
<style>

/* Background Gradient */
body {
    background: linear-gradient(135deg, #14b8a6, #020617);
}

/* Main container */
.block-container {
    padding: 2rem;
}

/* EVERYTHING ROUNDED */
* {
    border-radius: 18px !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(2, 6, 23, 0.75);
    backdrop-filter: blur(20px);
    border-radius: 20px !important;
}

/* Header */
h1 {
    text-align: center;
    color: white;
}

/* USER BUBBLE */
.user-bubble {
    background: rgba(168, 85, 247, 0.25);
    border: 1px solid rgba(168, 85, 247, 0.4);
    padding: 14px 18px;
    margin: 10px 0;
    max-width: 70%;
    margin-left: auto;
    color: white;
    backdrop-filter: blur(12px);
}

/* AI BUBBLE */
.ai-bubble {
    background: linear-gradient(135deg, rgba(20, 184, 166, 0.3), rgba(2, 6, 23, 0.85));
    border: 1px solid rgba(20, 184, 166, 0.4);
    padding: 14px 18px;
    margin: 10px 0;
    max-width: 70%;
    margin-right: auto;
    color: white;
    backdrop-filter: blur(12px);
}

/* Chat input container */
div[data-testid="stChatInput"] {
    background: transparent !important;
    border-radius: 30px !important;
    padding: 10px;
}

/* Text input box */
textarea {
    background: rgba(2, 6, 23, 0.8) !important;
    color: white !important;
    border-radius: 30px !important;
    border: 1px solid rgba(20, 184, 166, 0.4) !important;
    padding: 14px !important;
}

/* Button styling */
button {
    border-radius: 30px !important;
    background: linear-gradient(135deg, #14b8a6, #1e3a8a) !important;
    color: white !important;
    border: none !important;
}

/* Remove ugly default borders */
.css-1d391kg, .css-1cpxqw2 {
    border: none !important;
}

/* Smooth scroll feel */
html {
    scroll-behavior: smooth;
}

</style>
""", unsafe_allow_html=True)

# 🧠 Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Riva Control")
    st.write("Your futuristic assistant")

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# 🧠 Memory
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Riva, a futuristic, calm, slightly witty AI assistant."}
    ]

# 🏷 Title
st.title("🤖 Riva AI")

# 💬 Chat Display
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f'<div class="ai-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

# 🧾 Input
user_input = st.chat_input("Message Riva...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.messages
        )

        reply = response.choices[0].message.content

    except Exception as e:
        reply = f"⚠️ {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": reply})

    st.rerun()
