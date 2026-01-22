import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Analytics - AI Fitness Coach", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    h1 { color: #ff6b35 !important; font-weight: 900 !important; }
    h2 { color: #1a73e8 !important; border-bottom: 3px solid #ff6b35 !important; padding-bottom: 10px !important; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Fitness Analytics & Dashboard")
st.markdown("Comprehensive overview of your fitness journey - Powered by AI")
st.markdown("---")

# File Paths
PROFILE_PATH = "data/user_profile.json"
WEIGHT_PATH = "data/weight_log.json"
WORKOUT_PATH = "data/workout_log.json"
PROGRESS_PATH = "data/progress.json"

# Helpers
def load_json(path):
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                data = json.load(f)
                return data if data else []
        except (json.JSONDecodeError, ValueError):
            return []
    return []

# Load Data
profile = load_json(PROFILE_PATH)
weights = load_json(WEIGHT_PATH)
workouts = load_json(WORKOUT_PATH)
progress = load_json(PROGRESS_PATH)

if not profile:
    st.warning("⚠️ Please complete your profile first.")
    st.info("Go to the Profile page to get started!")
    st.stop()

# Profile Summary
st.subheader("👤 Your Profile Summary")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("📛 Name", profile.get("name", "N/A"))
with col2:
    st.metric("🎂 Age", f"{profile.get('age')} years")
with col3:
    st.metric("⚖️ Weight", f"{profile.get('weight')} kg")
with col4:
    st.metric("🎯 Goal", profile.get("primary_goal", "N/A"))
with col5:
    st.metric("💪 Level", profile.get("fitness_level", "N/A"))

st.markdown("---")

# Progress Data
if progress:
    df_progress = pd.DataFrame(progress)
    df_progress["date"] = pd.to_datetime(df_progress["date"])
    df_progress = df_progress.sort_values("date")

    st.subheader("📈 Body Measurements Progress")

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if len(df_progress) > 1:
            weight_change = df_progress["weight"].iloc[-1] - df_progress["weight"].iloc[0]
            st.metric("Weight Change", f"{weight_change:+.1f} kg", "Current: " + str(df_progress["weight"].iloc[-1]) + " kg")
        else:
            st.metric("Weight", f"{df_progress['weight'].iloc[0]} kg" if len(df_progress) > 0 else "N/A")

    with col2:
        if len(df_progress) > 1 and "waist" in df_progress.columns:
            waist_change = df_progress["waist"].iloc[-1] - df_progress["waist"].iloc[0]
            st.metric("Waist Change", f"{waist_change:+.1f} cm", "Current: " + str(df_progress["waist"].iloc[-1]) + " cm")

    with col3:
        if len(df_progress) > 1 and "chest" in df_progress.columns:
            chest_change = df_progress["chest"].iloc[-1] - df_progress["chest"].iloc[0]
            st.metric("Chest Change", f"{chest_change:+.1f} cm", "Current: " + str(df_progress["chest"].iloc[-1]) + " cm")

    with col4:
        if len(df_progress) > 1 and "arms" in df_progress.columns:
            arms_change = df_progress["arms"].iloc[-1] - df_progress["arms"].iloc[0]
            st.metric("Arms Change", f"{arms_change:+.1f} cm", "Current: " + str(df_progress["arms"].iloc[-1]) + " cm")

    st.markdown("---")

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        fig_weight = px.line(
            df_progress,
            x="date",
            y="weight",
            title="⚖️ Weight Progress Over Time",
            labels={"weight": "Weight (kg)", "date": "Date"},
            markers=True
        )
        fig_weight.update_traces(line=dict(color="#ff6b35", width=3))
        st.plotly_chart(fig_weight, use_container_width=True)

    with col2:
        if "waist" in df_progress.columns:
            fig_waist = px.line(
                df_progress,
                x="date",
                y="waist",
                title="📏 Waist Measurement",
                labels={"waist": "Waist (cm)", "date": "Date"},
                markers=True
            )
            fig_waist.update_traces(line=dict(color="#1a73e8", width=3))
            st.plotly_chart(fig_waist, use_container_width=True)

else:
    st.info("📌 No progress data yet. Start logging your measurements in the 'Tracking' section!")

st.markdown("---")

# Workout Consistency
st.subheader("🏋️ Workout Consistency")

if workouts:
    df_workout = pd.DataFrame(workouts)
    df_workout["date"] = pd.to_datetime(df_workout["date"])
    workout_counts = df_workout["date"].dt.date.value_counts().sort_index()

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🔥 Total Workouts", len(workouts))
    with col2:
        avg_workouts = len(workouts) / ((workout_counts.index[-1] - workout_counts.index[0]).days + 1) if len(workout_counts) > 1 else 0
        st.metric("📊 Avg Workouts/Week", f"{avg_workouts * 7:.1f}")
    with col3:
        st.metric("🏅 Best Streak", "Coming Soon")

    fig_workout = px.bar(
        x=workout_counts.index,
        y=workout_counts.values,
        title="📅 Workouts Per Day",
        labels={"x": "Date", "y": "Number of Workouts"}
    )
    fig_workout.update_traces(marker=dict(color="#2ecc71"))
    st.plotly_chart(fig_workout, use_container_width=True)

    if len(workouts) >= 10:
        st.success("🎉 Excellent consistency! You're crushing your goals! 💪")
    elif len(workouts) >= 5:
        st.info("🚀 Good start! Build on this momentum!")
    else:
        st.warning("📈 Start logging workouts to track your progress!")

else:
    st.info("📌 No workout data yet. Start logging workouts in the 'Tracking' section!")

st.markdown("---")

# Recommendations
st.subheader("🎯 AI-Powered Recommendations")

goal = profile.get("primary_goal", "General Fitness")
level = profile.get("fitness_level", "Beginner")

recommendations = {
    ("Fat Loss", "Beginner"): "Start with 3-4 workouts per week, focus on cardio mixed with light strength training. Increase water intake to 3-4L daily.",
    ("Fat Loss", "Intermediate"): "Aim for 4-5 workouts per week. Combine HIIT cardio with strength training. Create a 500 calorie deficit.",
    ("Fat Loss", "Advanced"): "Perform 5-6 workouts per week with periodized training. Add compound movements and progressive overload.",
    
    ("Muscle Gain", "Beginner"): "Start with 3-4 strength training sessions. Focus on learning proper form. Eat in a calorie surplus.",
    ("Muscle Gain", "Intermediate"): "Do 4-5 strength sessions per week on a split routine. Eat 1.6-1.8g protein per kg. Track macros.",
    ("Muscle Gain", "Advanced"): "Follow an advanced split (PPL/Upper-Lower). Periodize training. Eat 2g protein per kg in surplus.",
    
    ("General Fitness", "Beginner"): "Mix cardio and strength training 3 times per week. Focus on consistency over intensity.",
    ("General Fitness", "Intermediate"): "Train 4 times per week with balanced cardio and strength. Incorporate flexibility work.",
    ("General Fitness", "Advanced"): "Maintain 5 workouts per week. Focus on performance metrics and injury prevention.",
}

recommendation = recommendations.get((goal, level), "Stay consistent with your training and nutrition!")
st.markdown(f"💡 **{recommendation}**")

st.markdown("---")

# Summary
st.subheader("📊 Your Fitness Summary")

summary_data = {
    "Profile Completed": "✅" if profile else "❌",
    "Progress Logged": f"✅ {len(progress)} entries" if progress else "❌",
    "Workouts Recorded": f"✅ {len(workouts)} sessions" if workouts else "❌",
    "Current Goal": profile.get("primary_goal", "N/A"),
    "Fitness Level": profile.get("fitness_level", "N/A"),
}

for key, value in summary_data.items():
    st.markdown(f"**{key}:** {value}")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #888; font-size: 12px;'>Keep pushing! Every day is progress. 💪</p>", unsafe_allow_html=True)
