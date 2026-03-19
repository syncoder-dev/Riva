import streamlit as st
from groq import Groq
import uuid
import base64

# ⚙️ CONFIG
st.set_page_config(page_title="Riva AI", layout="wide")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 🔐 SIMPLE LOGIN SYSTEM
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login to Riva")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()

# 🧠 PROMPTS
REVO_PROMPT = """
You are Revo, the core intelligence behind Riva.

You control reasoning, clarity, and usefulness.
You ensure:
- Responses are accurate and structured
- No unnecessary complexity
- You silently optimize answers

You never speak directly.
"""

RIVA_PROMPT = """
You are Riva, a futuristic AI assistant.

- Calm, intelligent, slightly witty
- Clear and simple language
- Helpful and engaging

You are the voice. Revo is the brain.
"""

# 🔁 LOAD GIF
def load_gif(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

gif_base64 = load_gif("riva_spin.gif")

# 🧠 MULTI CHAT WITH NAMES
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "chat_names" not in st.session_state:
    st.session_state.chat_names = {}

if "current_chat" not in st.session_state:
    chat_id = str(uuid.uuid4())
    st.session_state.current_chat = chat_id
    st.session_state.chats[chat_id] = []
    st.session_state.chat_names[chat_id] = "New Chat"

# 🎨 UI
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a0f2c, #4c1d95);
    color: white;
}
.glow-title {
    font-size: 50px;
    text-align: center;
    color: #7dd3fc;
    text-shadow: 0 0 10px #38bdf8, 0 0 20px #0ea5e9;
}
</style>
""", unsafe_allow_html=True)

# 🧩 SIDEBAR
with st.sidebar:

    if st.button("➕ New Chat"):
        new_id = str(uuid.uuid4())
        st.session_state.chats[new_id] = []
        st.session_state.chat_names[new_id] = "New Chat"
        st.session_state.current_chat = new_id
        st.rerun()

    st.markdown("### Chats")

    for chat_id in st.session_state.chats:
        name = st.session_state.chat_names[chat_id]
        if st.button(name, key=chat_id):
            st.session_state.current_chat = chat_id
            st.rerun()

    st.markdown("---")

    # ✏️ RENAME CHAT
    new_name = st.text_input("Rename chat")

    if st.button("Rename"):
        st.session_state.chat_names[st.session_state.current_chat] = new_name
        st.rerun()

# 🏷 HEADER
st.image("riva_logo.png", width=200)
st.markdown('<div class="glow-title">Riva</div>', unsafe_allow_html=True)

# 💬 CHAT
messages = st.session_state.chats[st.session_state.current_chat]

for msg in messages:
    role = msg["role"]
    if role == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Riva:** {msg['content']}")

# 💬 INPUT
user_input = st.chat_input("Message Riva...")

if user_input:
    messages.append({"role": "user", "content": user_input})

    thinking = st.empty()
    thinking.markdown(f"""
    <div style="text-align:center;">
        <img src="data:image/gif;base64,{gif_base64}" width="120">
        <p>Thinking...</p>
    </div>
    """, unsafe_allow_html=True)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": REVO_PROMPT},
            {"role": "system", "content": RIVA_PROMPT}
        ] + messages
    )

    reply = response.choices[0].message.content

    thinking.empty()

    messages.append({"role": "assistant", "content": reply})

    st.rerun()
