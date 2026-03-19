import streamlit as st
from groq import Groq
import base64

st.set_page_config(page_title="Riva AI", layout="wide")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 🧠 PROMPTS
REVA_PROMPT = "You are Riva, calm, futuristic, slightly witty."
REVO_PROMPT = "You refine responses to be sharper and more intelligent."

# 🧠 STATE
if "chats" not in st.session_state:
    st.session_state.chats = {"Chat 1": []}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"

if "thinking" not in st.session_state:
    st.session_state.thinking = False

# 🖼 LOAD IMAGE
def load_img(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# 🎨 UI STYLE
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

# 📂 SIDEBAR (LOGO ONLY + CHAT LIST)
with st.sidebar:
    try:
        logo = load_img("riva_logo.png")
        st.markdown(f'<img src="data:image/png;base64,{logo}" width="120">', unsafe_allow_html=True)
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

    # ➕ NEW CHAT
    if st.button("➕ New Chat"):
        name = f"Chat {len(chat_names)+1}"
        st.session_state.chats[name] = []
        st.session_state.current_chat = name
        st.rerun()

    # ⚡ RENAME (SIMULATED RIGHT CLICK)
    with st.expander("⋮ Chat Options"):
        new_name = st.text_input("Rename chat")
        if st.button("Apply Rename"):
            if new_name:
                st.session_state.chats[new_name] = st.session_state.chats.pop(st.session_state.current_chat)
                st.session_state.current_chat = new_name
                st.rerun()

# 🏷️ TITLE
st.markdown('<div class="title">RIVA</div>', unsafe_allow_html=True)

# 🤖 AVATAR (ONLY SHOW SPIN WHEN THINKING)
try:
    if st.session_state.thinking:
        gif = load_img("riva_spin.gif")
        st.markdown(f'<img src="data:image/gif;base64,{gif}" width="80">', unsafe_allow_html=True)
    else:
        avatar = load_img("riva_avatar.png")
        st.markdown(f'<img src="data:image/png;base64,{avatar}" width="80">', unsafe_allow_html=True)
except:
    st.write("Avatar missing")

# 💬 CHAT DISPLAY
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

    st.session_state.thinking = True
    st.rerun()

# 🤖 RESPONSE
if st.session_state.thinking:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": REVA_PROMPT},
            {"role": "system", "content": REVO_PROMPT},
        ] + messages
    )

    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})

    st.session_state.thinking = False
    st.rerun()
