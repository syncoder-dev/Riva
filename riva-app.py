import streamlit as st
from groq import Groq

# 🔑 Setup
st.set_page_config(page_title="Riva AI", page_icon="🤖", layout="wide")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 🎨 GLOBAL CSS (ULTRA ROUNDED + GLASS UI)
st.markdown("""
<style>

/* 🌊 SOFT BACKGROUND (TEAL → LIGHT BLUE) */
html, body, [data-testid="stAppViewContainer"] {
    height: 100%;
    margin: 0;
    background: linear-gradient(to bottom right, #0ea5a4, #60a5fa) !important;
}

/* REMOVE DEFAULT WHITE AREAS */
[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stToolbar"] {
    display: none;
}

/* MAIN LAYOUT */
.block-container {
    padding: 2rem;
}

/* 🌟 GLOBAL ROUNDNESS */
* {
    border-radius: 18px !important;
}

/* 🧊 SIDEBAR (GLASS) */
section[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(15px);
}

/* 🟣 USER BUBBLE (SOFT PURPLE GLASS) */
.user-bubble {
    background: rgba(168, 85, 247, 0.25);
    border: 1px solid rgba(168, 85, 247, 0.35);
    padding: 14px 18px;
    margin: 10px 0;
    max-width: 70%;
    margin-left: auto;
    color: white;
    backdrop-filter: blur(10px);
}

/* 🔵 AI BUBBLE (TEAL → LIGHT BLUE GLASS) */
.ai-bubble {
    background: linear-gradient(to right, rgba(14, 165, 164, 0.35), rgba(96, 165, 250, 0.35));
    border: 1px solid rgba(255,255,255,0.2);
    padding: 14px 18px;
    margin: 10px 0;
    max-width: 70%;
    margin-right: auto;
    color: white;
    backdrop-filter: blur(10px);
}

/* 💬 INPUT BOX (CLEAN GLASS) */
textarea {
    background: rgba(255, 255, 255, 0.1) !important;
    color: white !important;
    border-radius: 30px !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    padding: 14px !important;
}

/* 🔘 BUTTON */
button {
    border-radius: 30px !important;
    background: linear-gradient(to right, #0ea5a4, #60a5fa) !important;
    color: white !important;
    border: none !important;
}

/* 🏷 TITLE */
h1 {
    color: white;
    text-align: center;
    font-weight: 600;
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
