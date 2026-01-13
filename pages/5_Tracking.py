import streamlit as st
import json
import os
from datetime import date
import pandas as pd

DATA_PATH = "data/progress.json"

st.set_page_config(page_title="Progress Tracker", page_icon="📊")
st.title("📊 Fitness Progress Tracker")
st.write("Track your body and strength progress over time.")

# ---------- Helpers ----------
def load_progress():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    return []

def save_progress(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=4)

progress_data = load_progress()

# ---------- Add Entry ----------
st.header("➕ Add New Entry")

entry_date = st.date_input("Date", date.today())
weight = st.number_input("Body Weight (kg)", 30.0, 200.0, step=0.5)
waist = st.number_input("Waist (cm)", 40.0, 150.0, step=0.5)
strength = st.text_input("Strength Highlight (optional)")

if st.button("Save Progress"):
    progress_data.append({
        "date": str(entry_date),
        "weight": weight,
        "waist": waist,
        "strength": strength
    })
    save_progress(progress_data)
    st.success("✅ Progress saved")

# ---------- Charts ----------
st.divider()
st.header("📈 Progress Charts")

if progress_data:
    df = pd.DataFrame(progress_data)
    df["date"] = pd.to_datetime(df["date"])

    st.subheader("Body Weight Trend")
    st.line_chart(df.set_index("date")["weight"])

    st.subheader("Waist Measurement Trend")
    st.line_chart(df.set_index("date")["waist"])

else:
    st.info("No data yet. Add progress entries to see charts.")

# ---------- History ----------
st.divider()
st.header("📜 History")

for entry in reversed(progress_data):
    st.markdown(
        f"""
**📅 {entry['date']}**  
• Weight: **{entry['weight']} kg**  
• Waist: **{entry['waist']} cm**  
• Strength: {entry['strength'] or '—'}
"""
    )
