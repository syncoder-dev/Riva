import streamlit as st
from groq import Groq

# 🔑 Setup
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="Riva AI", page_icon="🤖")
st.title("🤖 Riva AI")

# 🧠 Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# 💬 Display messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 🧾 Input
user_input = st.chat_input("Talk to Riva...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=st.session_state.messages
        )

        reply = response.choices[0].message.content

    except Exception as e:
        reply = f"Error: {str(e)}"

    with st.chat_message("assistant"):
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
