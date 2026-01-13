import streamlit as st
import json
import os

from ai.llm import load_llm
from ai.prompts import FITNESS_COACH_PROMPT

PROFILE_PATH = "data/user_profile.json"

st.set_page_config(page_title="AI Fitness Coach", page_icon="💪")
st.title("🤖 AI Fitness Coach")
st.write("Your personal AI-powered gym trainer (running locally with Ollama)")

# ---------- Load user profile ----------
def load_profile():
    if os.path.exists(PROFILE_PATH):
        with open(PROFILE_PATH, "r") as f:
            return json.load(f)
    return None

profile = load_profile()
if profile is None:
    st.warning("⚠️ Please complete your profile first.")
    st.stop()

# ---------- Load Ollama LLM (streaming) ----------
llm = load_llm()

# ---------- Chat memory ----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous messages
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input(
    "Ask about workouts, diet, calories, recovery, form, motivation..."
)

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Build prompt using profile
    prompt = FITNESS_COACH_PROMPT.format(
        age=profile.get("age"),
        gender=profile.get("gender"),
        height=profile.get("height"),
        weight=profile.get("weight"),
        goal=profile.get("goal"),
        activity_level=profile.get("activity_level"),
        diet=profile.get("diet_preference"),
        medical=profile.get("medical_conditions"),
        injuries=profile.get("injuries"),
        question=user_input
    )

    # ---------- Streaming response from Ollama ----------
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response_text = ""
        with st.spinner("Thinking like a coach..."):
            for chunk in llm(prompt):  # llm now yields chunks
                response_text += chunk
                message_placeholder.markdown(response_text)

    st.session_state.chat_history.append({"role": "assistant", "content": response_text})
