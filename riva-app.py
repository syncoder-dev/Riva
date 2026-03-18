import streamlit as st
from groq import Groq

# 🔑 Setup
st.set_page_config(page_title="Riva AI", page_icon="🤖")
st.title("🤖 Riva AI")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 🧠 Memory (chat history)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Riva, a smart, helpful and slightly witty AI assistant."}
    ]

# 💬 Show chat
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 🧾 User input
user_input = st.chat_input("Talk to Riva...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        # 🤖 AI response
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # safe model
            messages=st.session_state.messages
        )

        reply = response.choices[0].message.content

    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"

    # Show assistant message
    with st.chat_message("assistant"):
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
