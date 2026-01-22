import streamlit as st
import json
import os
from datetime import date
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

DATA_PATH = "data/progress.json"

st.set_page_config(page_title="Progress Tracker - AI Fitness Coach", page_icon="📈", layout="wide")

st.markdown("""
    <style>
    h1 { color: #ff6b35 !important; font-weight: 900 !important; }
    h2 { color: #1a73e8 !important; border-bottom: 3px solid #ff6b35 !important; padding-bottom: 10px !important; }
    .stButton > button { background: linear-gradient(135deg, #ff6b35 0%, #ff8c5a 100%) !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: bold !important; }
    .stButton > button:hover { transform: translateY(-2px) !important; }
    </style>
""", unsafe_allow_html=True)

st.title("📈 Fitness Progress Tracker")
st.markdown("Track your body measurements and strength improvements over time")
st.markdown("---")

# Helpers
def load_progress():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    return []

def save_progress(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=4)

progress_data = load_progress()

# Add Entry Section
st.subheader("➕ Log New Progress")

col1, col2, col3, col4 = st.columns(4)

with col1:
    entry_date = st.date_input("📅 Date", date.today())
with col2:
    weight = st.number_input("⚖️ Body Weight (kg)", 30.0, 200.0, step=0.5)
with col3:
    waist = st.number_input("📏 Waist (cm)", 40.0, 150.0, step=0.5)
with col4:
    chest = st.number_input("💪 Chest (cm)", 60.0, 150.0, step=0.5)

arms = st.number_input("🦾 Arms (cm)", 20.0, 50.0, step=0.5)
strength = st.text_area("🏋️ Strength Highlight (optional)", height=50, placeholder="e.g., 'Lifted 100kg bench press'")

if st.button("💾 Save Progress", use_container_width=True):
    progress_data.append({
        "date": str(entry_date),
        "weight": weight,
        "waist": waist,
        "chest": chest,
        "arms": arms,
        "strength": strength
    })
    save_progress(progress_data)
    st.success("✅ Progress logged successfully!")
    st.balloons()

st.markdown("---")

# Charts Section
st.subheader("📊 Progress Charts")

if progress_data:
    df = pd.DataFrame(progress_data)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        latest_weight = df["weight"].iloc[-1]
        weight_change = latest_weight - df["weight"].iloc[0]
        st.metric("Current Weight", f"{latest_weight} kg", f"{weight_change:+.1f} kg")
    
    with col2:
        latest_waist = df["waist"].iloc[-1]
        waist_change = latest_waist - df["waist"].iloc[0]
        st.metric("Current Waist", f"{latest_waist} cm", f"{waist_change:+.1f} cm")
    
    with col3:
        latest_chest = df["chest"].iloc[-1]
        chest_change = latest_chest - df["chest"].iloc[0]
        st.metric("Current Chest", f"{latest_chest} cm", f"{chest_change:+.1f} cm")
    
    with col4:
        latest_arms = df["arms"].iloc[-1]
        arms_change = latest_arms - df["arms"].iloc[0]
        st.metric("Current Arms", f"{latest_arms} cm", f"{arms_change:+.1f} cm")

    st.markdown("---")

    # Weight trend
    col1, col2 = st.columns(2)
    
    with col1:
        fig_weight = px.line(
            df,
            x="date",
            y="weight",
            title="💪 Weight Progression",
            labels={"weight": "Weight (kg)", "date": "Date"},
            markers=True
        )
        fig_weight.update_traces(line=dict(color="#ff6b35", width=3))
        st.plotly_chart(fig_weight, use_container_width=True)

    with col2:
        fig_waist = px.line(
            df,
            x="date",
            y="waist",
            title="📏 Waist Measurement Trend",
            labels={"waist": "Waist (cm)", "date": "Date"},
            markers=True
        )
        fig_waist.update_traces(line=dict(color="#1a73e8", width=3))
        st.plotly_chart(fig_waist, use_container_width=True)

    col1, col2 = st.columns(2)
    
    with col1:
        fig_chest = px.line(
            df,
            x="date",
            y="chest",
            title="🏋️ Chest Measurement Trend",
            labels={"chest": "Chest (cm)", "date": "Date"},
            markers=True
        )
        fig_chest.update_traces(line=dict(color="#2ecc71", width=3))
        st.plotly_chart(fig_chest, use_container_width=True)

    with col2:
        fig_arms = px.line(
            df,
            x="date",
            y="arms",
            title="🦾 Arms Measurement Trend",
            labels={"arms": "Arms (cm)", "date": "Date"},
            markers=True
        )
        fig_arms.update_traces(line=dict(color="#e74c3c", width=3))
        st.plotly_chart(fig_arms, use_container_width=True)

    st.markdown("---")

    # History
    st.subheader("📜 Progress History")
    
    for entry in reversed(progress_data):
        with st.container():
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"**📅 {entry['date']}**")
            with col2:
                st.markdown(f"⚖️ Weight: **{entry['weight']} kg**")
            with col3:
                st.markdown(f"📏 Waist: **{entry['waist']} cm**")
            with col4:
                st.markdown(f"🏋️ Chest: **{entry['chest']} cm**")
            
            if entry.get('strength'):
                st.markdown(f"💪 *{entry['strength']}*")
            st.divider()

else:
    st.info("📌 No progress data yet. Start logging your measurements to see charts!")
    st.markdown("""
    ### Why track progress?
    - 📊 Visualize your fitness journey
    - 🎯 Stay motivated with data
    - 📈 Identify trends and patterns
    - 💪 Celebrate your achievements
    """)

