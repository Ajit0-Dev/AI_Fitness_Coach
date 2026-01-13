import streamlit as st
import json
import os
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analytics", page_icon="📊")
st.title("📊 Fitness Analytics & Progress")

# ---------- File Paths ----------
PROFILE_PATH = "data/user_profile.json"
WEIGHT_PATH = "data/weight_log.json"
WORKOUT_PATH = "data/workout_log.json"

# ---------- Helpers ----------
def load_json(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

# ---------- Load Data ----------
profile = load_json(PROFILE_PATH)
weights = load_json(WEIGHT_PATH)
workouts = load_json(WORKOUT_PATH)

if not profile:
    st.warning("⚠️ Please complete your profile first.")
    st.stop()

# ---------- Profile Summary ----------
st.header("👤 Profile Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Age", profile.get("age"))
col2.metric("Weight (kg)", profile.get("weight"))
col3.metric("Goal", profile.get("primary_goal"))

st.divider()

# ---------- Weight Progress ----------
st.header("📉 Weight Progress")

if weights:
    df_weight = pd.DataFrame(weights)
    df_weight["date"] = pd.to_datetime(df_weight["date"])

    fig, ax = plt.subplots()
    ax.plot(df_weight["date"], df_weight["weight"], marker="o")
    ax.set_xlabel("Date")
    ax.set_ylabel("Weight (kg)")
    ax.set_title("Weight Over Time")

    st.pyplot(fig)
else:
    st.info("No weight data recorded yet.")

st.divider()

# ---------- Workout Consistency ----------
st.header("🏋️ Workout Consistency")

if workouts:
    df_workout = pd.DataFrame(workouts)
    workout_counts = df_workout["date"].value_counts().sort_index()

    fig, ax = plt.subplots()
    ax.bar(workout_counts.index, workout_counts.values)
    ax.set_xlabel("Date")
    ax.set_ylabel("Workouts")
    ax.set_title("Workouts Per Day")

    st.pyplot(fig)

    st.success(f"🔥 Total Workouts Completed: {len(workouts)}")
else:
    st.info("No workouts logged yet.")

st.divider()

# ---------- Motivation ----------
st.header("💡 Motivation")

if len(workouts) >= 10:
    st.success("Excellent consistency! Keep going 💪")
elif len(workouts) >= 5:
    st.info("Good start — build momentum 🚀")
else:
    st.warning("Start logging workouts to see progress 📈")
