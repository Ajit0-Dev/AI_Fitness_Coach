import streamlit as st
import json
import os

from ai.llm import load_llm
from ai.prompts import DIET_PLAN_PROMPT

PROFILE_PATH = "data/user_profile.json"

# Professional page styling
st.set_page_config(page_title="Diet Plan - AI Fitness Coach", page_icon="🥗", layout="wide")

st.markdown("""
    <style>
    h1 { color: #ff6b35 !important; font-weight: 900 !important; }
    h2 { color: #1a73e8 !important; border-bottom: 3px solid #ff6b35 !important; padding-bottom: 10px !important; }
    .stButton > button { background: linear-gradient(135deg, #ff6b35 0%, #ff8c5a 100%) !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: bold !important; }
    .stButton > button:hover { transform: translateY(-2px) !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🥗 AI Nutrition Coach")
st.markdown("Get personalized Indian diet plans for your fitness goals - Powered by Groq AI")
st.markdown("---")

# Load profile
if not os.path.exists(PROFILE_PATH):
    st.warning("⚠️ Please complete your profile first to generate personalized diet plans.")
    st.info("Go to the Profile page to get started!")
    st.stop()

with open(PROFILE_PATH, "r") as f:
    profile = json.load(f)

# Display profile info
with st.expander("📋 Your Fitness Profile", expanded=False):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Name", profile.get("name", "N/A"))
    with col2:
        st.metric("Goal", profile.get("primary_goal", "N/A"))
    with col3:
        st.metric("Diet Type", profile.get("diet_type", "N/A"))
    with col4:
        st.metric("Allergies", profile.get("allergies", "None"))

st.markdown("---")

# Load Groq LLM
llm = load_llm()

# Diet memory
if "diet_history" not in st.session_state:
    st.session_state.diet_history = []

# Preset diet options
st.subheader("🍽️ Choose Your Diet Plan Type")
col1, col2, col3 = st.columns(3)

preset_diets = {
    "Custom Request": None,
    "Muscle Building": "High protein Indian diet for muscle gain with 5-6 meals",
    "Fat Loss": "High protein, calorie deficit Indian diet for weight loss",
    "General Fitness": "Balanced nutrition Indian diet for general fitness",
    "Pre-Workout Focus": "Indian diet plan with pre-workout and post-workout meals",
    "Vegetarian High Protein": "High protein vegetarian Indian diet plan",
}

selected_preset = st.radio(
    "Select a preset diet plan or customize:",
    options=list(preset_diets.keys()),
    horizontal=True
)

# User input
if selected_preset == "Custom Request":
    user_input = st.text_area(
        "📝 Describe your diet request",
        placeholder="e.g., 'Simple 1500 calorie diet', 'High protein for muscle building', 'Budget-friendly options', etc.",
        height=80
    )
else:
    user_input = preset_diets[selected_preset]
    st.info(f"✅ Using preset: {selected_preset}")

st.markdown("---")

# Generate button
if st.button("📋 Generate My Diet Plan", use_container_width=True):
    if not user_input or not user_input.strip():
        st.error("❌ Please enter a diet request or select a preset.")
    else:
        st.session_state.diet_history.append({"role": "user", "content": user_input})

        # Build prompt
        prompt = DIET_PLAN_PROMPT.format(
            age=profile.get("age"),
            weight=profile.get("weight"),
            goal=profile.get("primary_goal"),
            diet=profile.get("diet_type"),
            allergies=profile.get("allergies", "None"),
            question=user_input
        )

        # Get response from Groq
        with st.spinner("🤔 Creating your personalized nutrition plan..."):
            response_text = llm(prompt)

        # Display response in a nice format
        st.markdown("---")
        st.subheader("✅ Your Personalized Diet Plan")
        
        # Format the response nicely
        st.markdown(response_text)
        
        # Download option
        st.download_button(
            label="📥 Download Diet Plan",
            data=response_text,
            file_name="my_diet_plan.txt",
            mime="text/plain"
        )

        st.session_state.diet_history.append({"role": "assistant", "content": response_text})

# Display history
if st.session_state.diet_history:
    st.markdown("---")
    with st.expander("📜 Generation History", expanded=False):
        for i, msg in enumerate(st.session_state.diet_history):
            if msg["role"] == "user":
                st.markdown(f"**Request:** {msg['content']}")
            else:
                st.markdown(f"**Plan:** {msg['content'][:200]}...")

# Sidebar tips
with st.sidebar:
    st.markdown("## 💡 Nutrition Tips")
    st.markdown("""
    ✅ **Macronutrient Balance:**
    - Protein: 25-35% (Muscle growth)
    - Carbs: 40-50% (Energy)
    - Fats: 20-30% (Hormones)
    
    ✅ **Indian Foods High in Protein:**
    - Paneer, Dahi (yogurt)
    - Moong dal, Chickpeas
    - Eggs, Chicken
    - Almonds, Peanuts
    
    ✅ **Hydration:**
    - 2.5-3L water daily
    - More during workouts
    - Herbal teas are great
    
    ✅ **Meal Timing:**
    - Eat every 3-4 hours
    - Post-workout: Within 1 hour
    - Pre-workout: 1-2 hours before
    """)
    
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.diet_history = []
        st.rerun()


