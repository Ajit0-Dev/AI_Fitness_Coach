import streamlit as st
import json
import os
from ai.llm import load_llm
from ai.prompts import WORKOUT_PLAN_PROMPT

PROFILE_PATH = "data/user_profile.json"

st.set_page_config(page_title="Workout Plan Generator", page_icon="🏋️‍♂️")
st.title("🏋️ Personalized Workout Plan")
st.write("Get AI-generated workouts based on your profile and goals.")

# ---------- Load user profile ----------
def load_profile():
    if os.path.exists(PROFILE_PATH):
        with open(PROFILE_PATH, "r") as f:
            return json.load(f)
    return None

profile = load_profile()
if not profile:
    st.warning("⚠️ Please complete your profile first.")
    st.stop()

# ---------- Load Ollama LLM ----------
llm = load_llm()

# ---------- Chat memory ----------
if "workout_history" not in st.session_state:
    st.session_state.workout_history = []

# User input
user_input = st.text_area(
    "Ask for a workout plan or adjustments (e.g., '5-day split', 'back-focused', 'home workout')"
)

if st.button("Generate Workout Plan") and user_input:
    st.session_state.workout_history.append({"role": "user", "content": user_input})
    with st.spinner("Generating your plan..."):
        # Build prompt
        prompt = WORKOUT_PLAN_PROMPT.format(
            name=profile.get("name"),
            age=profile.get("age"),
            gender=profile.get("gender"),
            height=profile.get("height"),
            weight=profile.get("weight"),
            activity_level=profile.get("activity_level"),
            fitness_level=profile.get("fitness_level"),
            primary_goal=profile.get("primary_goal"),
            time_per_day=profile.get("time_per_day"),
            workout_place=profile.get("workout_place"),
            medical_conditions=", ".join(profile.get("medical_conditions", [])),
            injuries=", ".join(profile.get("injuries", [])),
            question=user_input
        )

        # Stream response
        response_text = ""
        for chunk in llm(prompt):
            response_text += chunk
            st.markdown(response_text)

        st.session_state.workout_history.append({"role": "assistant", "content": response_text})
