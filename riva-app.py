# venora_core.py
import os
import json
from datetime import datetime
from groq import Groq

# ⚙️ CONFIG
API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=API_KEY)

# 🧠 MEMORY HANDLING
def load_memory(user_id, thread_id):
    """Load a user's specific chat thread from JSON storage."""
    mem_file = f"memory_{user_id}_{thread_id}.json"
    if os.path.exists(mem_file):
        with open(mem_file, "r") as f:
            return json.load(f)
    return []

def save_memory(user_id, thread_id, messages):
    mem_file = f"memory_{user_id}_{thread_id}.json"
    with open(mem_file, "w") as f:
        json.dump(messages, f, indent=2)

# ✨ DYNAMIC SYSTEM PROMPT GENERATOR
def generate_system_prompt(user_profile):
    """Creates a system prompt based on user style and use case."""
    style = user_profile.get("chat_style", "balanced")
    use_case = user_profile.get("use_case", "general")

    personality_map = {
        "casual": "friendly, witty, informal",
        "professional": "clear, precise, formal",
        "educational": "informative, explanatory, patient",
        "balanced": "intelligent, adaptive, helpful"
    }

    return {
        "role": "system",
        "content": f"""
You are Venora, an advanced AI assistant.
Personality:
- {personality_map.get(style)}
- Adapts to the user's style dynamically
Use Case:
- {use_case}
- Provide accurate, reliable, and relevant responses
Behavior:
- Give complete answers without filler
- Correct misconceptions politely
- Avoid hallucinations and lazy responses
- Prioritize privacy and data security
"""
    }

# 💬 RESPONSE HANDLER
def venora_respond(user_id, thread_id, user_input, user_profile):
    messages = load_memory(user_id, thread_id)

    # Append user input
    messages.append({"role": "user", "content": user_input, "timestamp": str(datetime.now())})

    # Build messages for API
    system_prompt = generate_system_prompt(user_profile)
    api_messages = [system_prompt] + messages

    # Call Groq API
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=api_messages
    )

    reply = response.choices[0].message.content

    # Save reply to memory
    messages.append({"role": "assistant", "content": reply, "timestamp": str(datetime.now())})
    save_memory(user_id, thread_id, messages)

    return reply
