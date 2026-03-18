import streamlit as st
from groq import Groq

# 🔑 Setup
st.set_page_config(page_title="Riva AI", page_icon="🤖", layout="wide")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 🎨 GLOBAL CSS (ULTRA ROUNDED + GLASS UI)
st.markdown("""
<style>

/* FORCE FULL BACKGROUND */
html, body, [data-testid="stAppViewContainer"] {
    height: 100%;
    margin: 0;
    background: linear-gradient(to bottom right, #14b8a6, #020617) !important;
}

/* REMOVE STREAMLIT WHITE LAYERS */
[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stToolbar"] {
    display: none;
}

/* MAIN CONTAINER */
.block-container {
    padding: 2rem;
}

/* EVERYTHING ROUNDED */
* {
    border-radius: 20px !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #020617 !important;
}

/* USER BUBBLE */
.user-bubble {
    background: #7c3aed;
    padding: 14px 18px;
    margin: 10px 0;
    max-width: 70%;
    margin-left: auto;
    color: white;
}

/* AI BUBBLE */
.ai-bubble {
    background: linear-gradient(to right, #14b8a6, #1e3a8a);
    padding: 14px 18px;
    margin: 10px 0;
    max-width: 70%;
    margin-right: auto;
    color: white;
}

/* INPUT BOX */
textarea {
    background: #020617 !important;
    color: white !important;
    border-radius: 30px !important;
    border: 1px solid #14b8a6 !important;
    padding: 14px !important;
}

/* BUTTON */
button {
    border-radius: 30px !important;
    background: linear-gradient(to right, #14b8a6, #1e3a8a) !important;
    color: white !important;
    border: none !important;
}

/* TITLE */
h1 {
    color: white;
    text-align: center;
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
