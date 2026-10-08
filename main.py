import os
import uuid
import base64
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")
AVATAR_PATH = "quantiro_animated_avatar_clean.gif"
STATIC_AVATAR = "quantiro_avatar.png"

st.set_page_config(page_title="Assistant", page_icon=STATIC_AVATAR, layout="centered")

with open("styles/style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if not os.path.exists(AVATAR_PATH):
    st.error(f"Avatar file not found: {AVATAR_PATH}")
    st.stop()

with open(AVATAR_PATH, "rb") as f:
    avatar_base64 = base64.b64encode(f.read()).decode()

st.markdown(f"""
<div class="assistant-header">
    <div class="assistant-avatar-container">
        <img src="data:image/gif;base64,{avatar_base64}" class="assistant-avatar">
    </div>
    <div class="assistant-info">
        <div class="assistant-title">QUANTIRO AI ASSISTANT</div>
        <div class="assistant-status"><span class="status-dot"></span><span>Online</span></div>
    </div>
</div>
""", unsafe_allow_html=True)


# ==================chat handling=====================================

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "history" not in st.session_state:
    st.session_state.history = []

for turn in st.session_state.history:
    avatar = STATIC_AVATAR if turn["role"] == "assistant" else None
    with st.chat_message(turn["role"], avatar=avatar):
        st.markdown(turn["content"])

if prompt := st.chat_input("Ask about our courses, AI automation, marketing service..."):
    st.session_state.history.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=STATIC_AVATAR):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/chat",
                    json={"session_id": st.session_state.session_id, "message": prompt},
                    timeout=300
                )
                response.raise_for_status()
                reply = response.json().get(
                    "reply", "Sorry, I couldn't generate a response."
                )
            except requests.RequestException as e:
                print(f"Backend error: {e}")
                reply = "Sorry, I’m temporarily unable to respond. Please try again shortly."
            except (ValueError, KeyError) as e:
                print(f"Response error: {e}")
                reply = "Sorry, I’m temporarily unable to respond. Please try again shortly."
            except Exception as e:
                print(f"Unexpected error: {e}")
                reply = "Sorry, I’m temporarily unable to respond. Please try again shortly."

        st.markdown(reply)

    st.session_state.history.append({"role": "assistant", "content": reply})