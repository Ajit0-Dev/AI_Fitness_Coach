import streamlit as st
import json
import os

from ai.llm import load_llm
from ai.prompts import FITNESS_COACH_PROMPT

PROFILE_PATH = "data/user_profile.json"

# Professional page styling
st.set_page_config(page_title="AI Fitness Coach - Chatbot", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
    h1 { color: #ff6b35 !important; font-weight: 900 !important; }
    h2 { color: #1a73e8 !important; border-bottom: 3px solid #ff6b35 !important; padding-bottom: 10px !important; }
    .stButton > button { background: linear-gradient(135deg, #ff6b35 0%, #ff8c5a 100%) !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: bold !important; }
    .stButton > button:hover { transform: translateY(-2px) !important; }
    .stChatMessage { background-color: #1a1f2e !important; border-radius: 8px !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 AI Fitness Coach")
st.markdown("Your personal AI-powered fitness expert - Powered by Groq AI")
st.markdown("---")

# Load user profile
def load_profile():
    if os.path.exists(PROFILE_PATH):
        with open(PROFILE_PATH, "r") as f:
            return json.load(f)
    return None

profile = load_profile()
if profile is None:
    st.warning("⚠️ Please complete your profile first to unlock personalized coaching.")
    st.info("Go to the Profile page to get started!")
    st.stop()

# Display profile summary
with st.expander("📋 Your Profile Summary", expanded=False):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Name", profile.get("name", "N/A"))
    with col2:
        st.metric("Age", f"{profile.get('age')} years")
    with col3:
        st.metric("Goal", profile.get("primary_goal", "N/A"))
    with col4:
        st.metric("Level", profile.get("fitness_level", "N/A"))

st.markdown("---")

# Load Groq LLM
llm = load_llm()

# Chat memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous messages
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input(
    "Ask about workouts, diet, form, recovery, motivation..."
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
        goal=profile.get("primary_goal"),
        activity_level=profile.get("activity_level"),
        diet=profile.get("diet_type"),
        medical=profile.get("medical_conditions", []),
        injuries=profile.get("injuries", []),
        question=user_input
    )

    # Get response from Groq
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("🤔 Thinking..."):
            response_text = llm(prompt)
        message_placeholder.markdown(response_text)

    st.session_state.chat_history.append({"role": "assistant", "content": response_text})

# Sidebar suggestions
with st.sidebar:
    st.markdown("## 💡 Quick Questions")
    st.markdown("*Try asking me:*")
    suggestions = [
        "📋 Create a workout routine",
        "🍽️ Suggest a diet plan",
        "💪 How to improve form?",
        "🏃 Best exercises for my goal?",
        "⏰ How long should I rest?",
        "🥗 What should I eat post-workout?",
        "📈 How to track progress?",
    ]
    for suggestion in suggestions:
        if st.button(suggestion, key=suggestion, use_container_width=True):
            st.session_state.chat_input = suggestion

    st.markdown("---")
    
    # Clear chat
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

