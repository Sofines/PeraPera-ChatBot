import streamlit as st
import requests


st.set_page_config(page_title="PeraPera ChatBot", page_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/1caff466-079f-47a0-8f11-66bf4234df9d/dghn6g4-b91fd690-4a3e-4dad-9f42-53a0f85a2c4e.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzFjYWZmNDY2LTA3OWYtNDdhMC04ZjExLTY2YmY0MjM0ZGY5ZFwvZGdobjZnNC1iOTFmZDY5MC00YTNlLTRkYWQtOWY0Mi01M2EwZjg1YTJjNGUucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.hcA5CCEFUTOLbRWB-RJlnULWkE_feqpPYpHUG7I-OrU")

BACKEND_URL = "http://127.0.0.1:8000/chat"

# Load external CSS
with open("styles.css", "r") as f:
    css = f.read()
st.markdown(f"""
    <style>{css}</style>
""", unsafe_allow_html=True)


st.title("PeraPera ChatBot")
st.write("こんにちは! I’m your Japanese tutor! Let’s learn together, ne~")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Konnichiwa~! I’m PeraPera, your  Japanese tutor. Ask me anything"}
    ]

# Display messages with custom avatars (with fallback for user icon)
for message in st.session_state.messages:
    try:
        avatar = "assets/moominsmol.png" if message["role"] == "assistant" else "assets/user_icon.jpg"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])
    except FileNotFoundError:
        # Fallback to an emoji for the user if user_icon.png is missing
        avatar = "assets/moominsmol.png" if message["role"] == "assistant" else "👤"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# User input
if user_input := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    try:
        with st.chat_message("user", avatar="assets/user_icon.jpg"):
            st.markdown(user_input)
    except FileNotFoundError:
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
    
    with st.spinner("PeraPera is thinking..."):
        try:
            response = requests.post(BACKEND_URL, json={"message": user_input})
            response.raise_for_status()
            bot_response = response.json()["response"]
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
            with st.chat_message("assistant", avatar="assets/moominsmol.png"):
                st.markdown(bot_response)
        except Exception as e:
            st.error(f"Oops! Something went wrong: {e}")