import os
import uuid
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL") # Default to localhost if not set
AVATAR_PATH='quantiro_animated_avatar_clean.gif'
st.set_page_config(page_title="Assistant", page_icon="quantiro_avatar.png",layout="centered")


# LOADING CSS
with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="assistant-header">
        <img src="{AVATAR_PATH}" class="assistant-avatar">
        <div class="assistant-info">
            <div class="assistant-title">QUANTIRO AI ASSISTANT</div>
            <div class="assistant-status">
                <span class="status-dot"></span>
                Online
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "history" not in st.session_state:
    st.session_state.history = []

for turn in st.session_state.history:
    with st.chat_message(turn["role"]):
        st.markdown(turn["content"])

if prompt := st.chat_input("Ask about our courses, AI automation , marketing service..."):
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant",avatar="quantiro_avatar.png"):
        with st.spinner("Thinking..."):
            try:
                r = requests.post(
                    f"{BACKEND_URL}/chat",
                    json={"session_id": st.session_state.session_id, "message": prompt},
                    timeout=300,
                )
                r.raise_for_status()
                reply = r.json()["reply"]
            except Exception as e:
                print("error : ",e)
                reply = f"Sorry, I’m temporarily unable to respond. Please try again shortly."
            st.markdown(reply)

    st.session_state.history.append({"role": "assistant", "content": reply})