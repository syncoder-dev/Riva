import streamlit as st
from groq import Groq
import base64

# ⚙️ CONFIG
st.set_page_config(page_title="Riva AI", layout="wide")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 🧠 SYSTEM PROMPTS
REVA_PROMPT = """
You are Riva, an advanced AI assistant created by Praagya.

Your personality:
- Calm, intelligent, futuristic
- Slightly witty but never annoying
- Clear and helpful

Rules:
- If the user shares their name, remember it and use it naturally later
- If asked about your creator, say you were developed by Praagya
- Never mention Revo (your internal system)
- Speak like a refined assistant, not a chatbot
"""

REVO_PROMPT = """
You are Revo, the hidden cognitive layer behind Riva.

Your role:
- Refine responses before they are sent
- Improve clarity, intelligence, and structure
- Remove fluff and unnecessary words
- Keep responses sharp, clean, and natural

Rules:
- Stay invisible
- Do not change meaning
- Do not add unnecessary complexity
"""

# 🧠 STATE
if "chats" not in st.session_state:
    st.session_state.chats = {"Chat 1": []}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"

if "user_name" not in st.session_state:
    st.session_state.user_name = None

# 🖼 IMAGE LOADER
def load_img(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# 🎨 UI
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500&display=swap');

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a0f2c, #4c1d95);
    color: white;
}

.title {
    font-family: 'Orbitron', sans-serif;
    font-size: 48px;
    text-align: center;
    color: #00eaff;
    text-shadow: 0 0 10px #00eaff, 0 0 25px #00eaff;
}

.user {
    text-align: right;
    background: rgba(168,85,247,0.35);
    padding: 10px;
    border-radius: 20px;
    margin: 10px 0;
}

.ai {
    text-align: left;
    background: rgba(59,130,246,0.25);
    padding: 10px;
    border-radius: 20px;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# 📂 SIDEBAR
with st.sidebar:
    try:
        logo = load_img("riva_logo.png")
        st.markdown(f'<img src="data:image/png;base64,{logo}" width="140">', unsafe_allow_html=True)
    except:
        st.write("Logo missing")

    st.markdown("### Chats")

    chat_names = list(st.session_state.chats.keys())

    selected = st.selectbox(
        "Select Chat",
        chat_names,
        index=chat_names.index(st.session_state.current_chat)
    )

    st.session_state.current_chat = selected

    if st.button("➕ New Chat"):
        name = f"Chat {len(chat_names)+1}"
        st.session_state.chats[name] = []
        st.session_state.current_chat = name
        st.rerun()

    # Rename (clean, not ugly UI)
    with st.expander("⋮ Options"):
        new_name = st.text_input("Rename chat")
        if st.button("Apply"):
            if new_name:
                st.session_state.chats[new_name] = st.session_state.chats.pop(st.session_state.current_chat)
                st.session_state.current_chat = new_name
                st.rerun()

# 🏷 TITLE
st.markdown('<div class="title">RIVA</div>', unsafe_allow_html=True)

# 💬 CHAT
messages = st.session_state.chats[st.session_state.current_chat]

for msg in messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai">{msg["content"]}</div>', unsafe_allow_html=True)

# 💬 INPUT
user_input = st.chat_input("Message Riva...")

if user_input:
    messages.append({"role": "user", "content": user_input})

    # 🧠 NAME DETECTION (simple but effective)
    if "my name is" in user_input.lower():
        try:
            name = user_input.split("is")[-1].strip().split(" ")[0]
            st.session_state.user_name = name
        except:
            pass

    # Show user message instantly
    st.markdown(f'<div class="user">{user_input}</div>', unsafe_allow_html=True)

    # 🤖 THINKING ANIMATION (RIGHT PLACE)
    try:
        gif = load_img("riva_spin.gif")
        st.markdown(
            f'<div class="ai"><img src="data:image/gif;base64,{gif}" width="60" style="filter: drop-shadow(0 0 8px #00eaff);"></div>',
            unsafe_allow_html=True
        )
    except:
        st.markdown('<div class="ai">Thinking...</div>', unsafe_allow_html=True)

    # 🧠 RESPONSE
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": REVA_PROMPT},
            {"role": "system", "content": REVO_PROMPT},
        ] + messages
    )

    reply = response.choices[0].message.content

    # Personal touch if name known
    if st.session_state.user_name and st.session_state.user_name.lower() not in reply.lower():
        reply = f"{st.session_state.user_name}, {reply}"

    messages.append({"role": "assistant", "content": reply})

    st.rerun()
