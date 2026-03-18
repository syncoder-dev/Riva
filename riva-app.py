import streamlit as st
from groq import Groq

# 🔑 Setup
st.set_page_config(page_title="Riva AI", page_icon="🤖", layout="wide")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 🎨 CUSTOM CSS (THIS IS THE MAGIC)
st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.8);
    backdrop-filter: blur(10px);
}

/* Chat container spacing */
.block-container {
    padding-top: 2rem;
}

/* USER MESSAGE */
.user-bubble {
    background: rgba(168, 85, 247, 0.2);
    border: 1px solid rgba(168, 85, 247, 0.4);
    padding: 12px 16px;
    border-radius: 15px;
    margin: 8px 0;
    color: white;
    backdrop-filter: blur(10px);
}

/* AI MESSAGE */
.ai-bubble {
    background: linear-gradient(135deg, rgba(30, 64, 175, 0.4), rgba(15, 23, 42, 0.8));
    border: 1px solid rgba(59, 130, 246, 0.3);
    padding: 12px 16px;
    border-radius: 15px;
    margin: 8px 0;
    color: white;
    backdrop-filter: blur(10px);
}

/* Input box */
div[data-testid="stChatInput"] textarea {
    background: rgba(15, 23, 42, 0.8) !important;
    color: white !important;
    border-radius: 12px !important;
    border: 1px solid rgba(99, 102, 241, 0.4) !important;
}

/* Title */
h1 {
    color: white;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# 🧠 Sidebar
with st.sidebar:
    st.title("⚙️ Riva Control")
    st.write("Your AI assistant")
    if st.button("Clear Chat"):
        st.session_state.messages = []

# 🧠 Memory
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Riva, a futuristic, witty AI assistant."}
    ]

st.title("🤖 Riva AI")

# 💬 Display messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f'<div class="ai-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

# 🧾 Input
user_input = st.chat_input("Talk to Riva...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.messages
        )

        reply = response.choices[0].message.content

    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": reply})

    st.rerun()
