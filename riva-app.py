import streamlit as st
from groq import Groq
import base64
PROMPTS
REVA_PROMPT = "You are Riva, a calm, futuristic AI assistant. You are clear, slightly witty, and helpful."

REVO_PROMPT = "You are Revo, the hidden intelligence layer. You refine responses to be smarter, sharper, and more structured."

# 🧠 SESSION STATE
# ⚙️ CONFIG
st.set_page_config(page_title="Riva AI", layout="wide")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 🧠 SYSTEM 
if "chats" not in st.session_state:
    st.session_state.chats = {"New Chat": []}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "New Chat"

# 🎨 BACKGROUND + FONT + GLOW
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500&display=swap');

/* 🌌 Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a0f2c, #4c1d95);
    color: white;
}

/* Remove header */
[data-testid="stHeader"] {
    background: transparent;
}

/* Title */
.title {
    font-family: 'Orbitron', sans-serif;
    font-size: 48px;
    text-align: center;
    color: #00eaff;
    text-shadow: 0 0 10px #00eaff, 0 0 25px #00eaff;
    margin-bottom: 10px;
}

/* Chat bubbles */
.user-bubble {
    background: rgba(168,85,247,0.35);
    padding: 12px;
    border-radius: 20px;
    margin: 10px 0;
    text-align: right;
}

.ai-bubble {
    background: rgba(59,130,246,0.25);
    padding: 12px;
    border-radius: 20px;
    margin: 10px 0;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)

# 🖼 FUNCTION TO LOAD IMAGE AS BASE64 (FIXES GIF ISSUES)
def load_image(path):
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return data

# 🏷️ HEADER (LOGO + TITLE)
col1, col2, col3 = st.columns([1,2,1])

with col2:
    try:
        logo = load_image("riva_logo.png")
        st.markdown(f'<img src="data:image/png;base64,{logo}" width="160" style="display:block;margin:auto;">', unsafe_allow_html=True)
    except:
        pass

    st.markdown('<div class="title">RIVA</div>', unsafe_allow_html=True)

# 📂 SIDEBAR (AVATAR + CHAT CONTROL)
with st.sidebar:
    st.markdown("### ⚙️ Riva Control")

    # 🔄 SPINNING AVATAR (REAL FIX)
    try:
        gif = load_image("riva_spin.gif")
        st.markdown(
            f'<img src="data:image/gif;base64,{gif}" width="120">',
            unsafe_allow_html=True
        )
    except:
        st.write("⚠️ GIF not found")

    st.divider()

    # 🧾 CHAT LIST
    chat_names = list(st.session_state.chats.keys())
    selected = st.selectbox("Chats", chat_names, index=chat_names.index(st.session_state.current_chat))
    st.session_state.current_chat = selected

    # ➕ NEW CHAT
    if st.button("➕ New Chat"):
        new_name = f"Chat {len(chat_names)+1}"
        st.session_state.chats[new_name] = []
        st.session_state.current_chat = new_name
        st.rerun()

    # ✏️ RENAME
    new_title = st.text_input("Rename chat")
    if st.button("Rename"):
        if new_title:
            st.session_state.chats[new_title] = st.session_state.chats.pop(st.session_state.current_chat)
            st.session_state.current_chat = new_title
            st.rerun()

    # 🧹 CLEAR
    if st.button("🧹 Clear Chat"):
        st.session_state.chats[st.session_state.current_chat] = []
        st.rerun()

# 💬 DISPLAY CHAT
messages = st.session_state.chats[st.session_state.current_chat]

for msg in messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

# 💬 INPUT
user_input = st.chat_input("Message Riva...")

if user_input:
    messages.append({"role": "user", "content": user_input})

    # 🔥 REVA + REVO COMBINED FLOW
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": REVA_PROMPT},
            {"role": "system", "content": REVO_PROMPT},
        ] + messages
    )

    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})

    st.rerun()
