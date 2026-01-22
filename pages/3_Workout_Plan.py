import streamlit as st
import json
import os
from ai.llm import load_llm
from ai.prompts import WORKOUT_PLAN_PROMPT

PROFILE_PATH = "data/user_profile.json"

# Professional page styling
st.set_page_config(page_title="Workout Plan - AI Fitness Coach", page_icon="🏋️", layout="wide")

st.markdown("""
    <style>
    h1 { color: #ff6b35 !important; font-weight: 900 !important; }
    h2 { color: #1a73e8 !important; border-bottom: 3px solid #ff6b35 !important; padding-bottom: 10px !important; }
    .stButton > button { background: linear-gradient(135deg, #ff6b35 0%, #ff8c5a 100%) !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: bold !important; }
    .stButton > button:hover { transform: translateY(-2px) !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🏋️ AI-Powered Workout Plans")
st.markdown("Generate personalized workout routines optimized for your goals - Powered by Groq AI")
st.markdown("---")

# Load user profile
def load_profile():
    if os.path.exists(PROFILE_PATH):
        with open(PROFILE_PATH, "r") as f:
            return json.load(f)
    return None

profile = load_profile()
if not profile:
    st.warning("⚠️ Please complete your profile first to generate personalized workout plans.")
    st.info("Go to the Profile page to get started!")
    st.stop()

# Display profile info
with st.expander("📋 Your Fitness Profile", expanded=False):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Goal", profile.get("primary_goal", "N/A"))
    with col2:
        st.metric("Level", profile.get("fitness_level", "N/A"))
    with col3:
        st.metric("Time/Day", f"{profile.get('time_per_day')} min")
    with col4:
        st.metric("Location", profile.get("workout_place", "N/A"))

st.markdown("---")

# Load Groq LLM
llm = load_llm()

# Chat memory
if "workout_history" not in st.session_state:
    st.session_state.workout_history = []

# Preset workout options
st.subheader("📝 Choose Your Workout Type")
col1, col2, col3 = st.columns(3)

preset_options = {
    "Custom Request": None,
    "Full Body": "Create a full body workout routine",
    "Upper/Lower Split": "Create an upper and lower body split routine",
    "Push/Pull/Legs": "Create a push/pull/legs routine",
    "Strength Focus": "Create a strength-focused routine",
    "Muscle Building": "Create a muscle hypertrophy routine"
}

selected_preset = st.radio(
    "Select preset or customize:",
    options=list(preset_options.keys()),
    horizontal=True
)

# User input
if selected_preset == "Custom Request":
    user_input = st.text_area(
        "📝 Describe your workout request",
        placeholder="e.g., 'Back-focused workout for home with dumbbells', 'Fat loss cardio routine', etc.",
        height=80
    )
else:
    user_input = preset_options[selected_preset]
    st.info(f"✅ Using preset: {selected_preset}")

st.markdown("---")

# Generate button
if st.button("💪 Generate My Workout Plan", use_container_width=True):
    if not user_input or not user_input.strip():
        st.error("❌ Please enter a workout request or select a preset.")
    else:
        st.session_state.workout_history.append({"role": "user", "content": user_input})
        
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
            medical_conditions=", ".join(profile.get("medical_conditions", ["None"])),
            injuries=", ".join(profile.get("injuries", ["None"])),
            question=user_input
        )

        # Get response from Groq
        with st.spinner("🤔 Creating your personalized plan..."):
            response_text = llm(prompt)

        # Display response in a nice format
        st.markdown("---")
        st.subheader("✅ Your Personalized Workout Plan")
        st.markdown(response_text)
        
        # Download option
        st.download_button(
            label="📥 Download Workout Plan",
            data=response_text,
            file_name="my_workout_plan.txt",
            mime="text/plain"
        )

        st.session_state.workout_history.append({"role": "assistant", "content": response_text})

# Display history
if st.session_state.workout_history:
    st.markdown("---")
    with st.expander("📜 Generation History", expanded=False):
        for i, msg in enumerate(st.session_state.workout_history):
            if msg["role"] == "user":
                st.markdown(f"**User:** {msg['content']}")
            else:
                st.markdown(f"**Plan:** {msg['content'][:200]}...")

# Sidebar tips
with st.sidebar:
    st.markdown("## 💡 Workout Tips")
    st.markdown("""
    ✅ **Before Starting:**
    - Warm up for 5-10 minutes
    - Focus on form over weight
    - Listen to your body
    
    ✅ **During Workout:**
    - Control the movement
    - Breathe properly
    - Rest adequately
    
    ✅ **After Workout:**
    - Cool down and stretch
    - Eat protein within 1 hour
    - Stay hydrated
    """)
    
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.workout_history = []
        st.rerun()

