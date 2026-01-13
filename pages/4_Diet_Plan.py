import streamlit as st
import json
import os

from ai.llm import load_llm
from ai.prompts import DIET_PLAN_PROMPT

PROFILE_PATH = "data/user_profile.json"

st.set_page_config(page_title="Diet Plan", page_icon="🥗")
st.title("🥗 Personalized Diet Plan")
st.write("Simple Indian diet plans based on your fitness goal.")

# Load profile
if not os.path.exists(PROFILE_PATH):
    st.warning("Please complete your profile first.")
    st.stop()

with open(PROFILE_PATH, "r") as f:
    profile = json.load(f)

llm = load_llm()

user_input = st.text_input(
    "Ask for a diet plan",
    placeholder="Example: simple diet for fat loss"
)

if st.button("Generate Diet Plan"):
    if not user_input.strip():
        st.warning("Please enter a request.")
    else:
        prompt = DIET_PLAN_PROMPT.format(
            age=profile.get("age"),
            weight=profile.get("weight"),
            goal=profile.get("primary_goal"),
            diet=profile.get("diet_type"),
            allergies=profile.get("allergies"),
            question=user_input
        )

        with st.spinner("Generating diet plan..."):
            response = llm(prompt)

        st.success("Diet Plan Ready")
        st.markdown(response)

