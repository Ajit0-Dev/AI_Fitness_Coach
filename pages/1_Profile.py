import streamlit as st
import json
import os

PROFILE_PATH = "data/user_profile.json"

# Professional page styling
st.set_page_config(page_title="Profile - AI Fitness Coach", page_icon="👤", layout="wide")

st.markdown("""
    <style>
    h1 { color: #ff6b35 !important; font-weight: 900 !important; }
    h2 { color: #1a73e8 !important; border-bottom: 3px solid #ff6b35 !important; padding-bottom: 10px !important; }
    .stButton > button { background: linear-gradient(135deg, #ff6b35 0%, #ff8c5a 100%) !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: bold !important; }
    .stButton > button:hover { transform: translateY(-2px) !important; }
    </style>
""", unsafe_allow_html=True)

st.title("👤 Your Fitness Profile")
st.markdown("Complete your profile for personalized AI fitness recommendations")
st.markdown("---")

# Helper Functions
def load_profile():
    if os.path.exists(PROFILE_PATH):
        with open(PROFILE_PATH, "r") as f:
            return json.load(f)
    return {}

def save_profile(data):
    with open(PROFILE_PATH, "w") as f:
        json.dump(data, f, indent=4)

profile = load_profile()

# Section 1: Basic Personal Details
with st.container():
    st.subheader("1️⃣ Basic Personal Details")
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        name = st.text_input("📝 Full Name", profile.get("name", ""), placeholder="Enter your full name")
    with col2:
        age = st.number_input("🎂 Age", 10, 100, profile.get("age", 25))
    with col3:
        gender = st.selectbox(
            "♀️♂️ Gender",
            ["Male", "Female", "Other"],
            index=["Male", "Female", "Other"].index(profile.get("gender", "Male"))
        )
    with col4:
        st.write("")

    col1, col2, col3 = st.columns(3)
    with col1:
        height = st.number_input("📏 Height (cm)", 100, 250, profile.get("height", 170))
    with col2:
        weight = st.number_input("⚖️ Weight (kg)", 30, 200, profile.get("weight", 70))
    with col3:
        activity_level = st.selectbox(
            "🏃 Daily Activity Level",
            ["Sedentary", "Moderately Active", "Highly Active"],
            index=["Sedentary", "Moderately Active", "Highly Active"].index(
                profile.get("activity_level", "Sedentary")
            )
        )

st.markdown("---")

# Section 2: Fitness Details
with st.container():
    st.subheader("2️⃣ Fitness & Body Information")
    col1, col2 = st.columns(2)
    
    with col1:
        fitness_level = st.selectbox(
            "💪 Current Fitness Level",
            ["Beginner", "Intermediate", "Advanced"],
            index=["Beginner", "Intermediate", "Advanced"].index(profile.get("fitness_level", "Beginner"))
        )
    with col2:
        training_experience = st.number_input(
            "📅 Training Experience (months)",
            0, 240,
            profile.get("training_experience", 0)
        )

st.markdown("---")

# Section 3: Goals & Preferences
with st.container():
    st.subheader("3️⃣ Fitness Goals & Preferences")
    
    col1, col2 = st.columns(2)
    with col1:
        primary_goal = st.selectbox(
            "🎯 Primary Goal",
            ["Fat Loss", "Muscle Gain", "Strength", "Recomposition", "General Fitness"],
            index=["Fat Loss", "Muscle Gain", "Strength", "Recomposition", "General Fitness"].index(
                profile.get("primary_goal", "Fat Loss")
            )
        )
    with col2:
        workout_place = st.selectbox(
            "🏢 Workout Location",
            ["Gym", "Home", "Mixed"],
            index=["Gym", "Home", "Mixed"].index(
                profile.get("workout_place", "Gym")
            )
        )

    time_per_day = st.slider(
        "⏱️ Time Available Per Day (minutes)",
        15, 120,
        profile.get("time_per_day", 45)
    )
    sleep_hours = st.slider(
        "😴 Average Sleep Hours Per Night",
        3, 10,
        profile.get("sleep_hours", 7)
    )

st.markdown("---")

# Section 4: Diet & Lifestyle
with st.container():
    st.subheader("4️⃣ Diet & Lifestyle")
    col1, col2 = st.columns(2)
    
    with col1:
        diet_type = st.selectbox(
            "🥗 Diet Type",
            ["Vegetarian", "Non-Vegetarian", "Vegan", "Eggetarian", "Jain"],
            index=["Vegetarian", "Non-Vegetarian", "Vegan", "Eggetarian", "Jain"].index(
                profile.get("diet_type", "Vegetarian")
            )
        )
    with col2:
        allergies = st.text_input(
            "🚫 Food Allergies (comma separated)",
            profile.get("allergies", ""),
            placeholder="e.g., peanuts, shellfish, dairy"
        )

st.markdown("---")

# Section 5: Medical Information
with st.container():
    st.subheader("5️⃣ Medical & Injury Information ⚠️")
    st.markdown("*This helps us ensure your safety and create appropriate modifications*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        medical_conditions = st.multiselect(
            "🏥 Medical Conditions",
            ["Diabetes", "Thyroid", "Blood Pressure", "PCOS/PCOD", "Heart Issues", "Asthma", "None"],
            profile.get("medical_conditions", ["None"])
        )
    with col2:
        injuries = st.multiselect(
            "🤕 Injuries / Physical Issues",
            ["Knee Pain", "Back Pain", "Shoulder Pain", "Neck Pain", "Recent Surgery", "None"],
            profile.get("injuries", ["None"])
        )

    medications = st.text_area(
        "💊 Current Medications (optional)",
        profile.get("medications", ""),
        placeholder="List any medications you're taking"
    )

st.markdown("---")

# Section 6: Consent & Save
with st.container():
    st.subheader("6️⃣ Agreement & Consent")
    
    consent = st.checkbox(
        "✅ I understand that this AI assistant provides general fitness guidance only and is NOT a substitute for professional medical advice. I will consult healthcare professionals for medical concerns.",
        profile.get("consent", False)
    )

    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("💾 Save My Profile", use_container_width=True):
            if not consent:
                st.error("❌ You must accept the disclaimer to save your profile.")
            elif not name.strip():
                st.error("❌ Please enter your name.")
            else:
                user_profile = {
                    "name": name,
                    "age": age,
                    "gender": gender,
                    "height": height,
                    "weight": weight,
                    "activity_level": activity_level,
                    "fitness_level": fitness_level,
                    "training_experience": training_experience,
                    "primary_goal": primary_goal,
                    "time_per_day": time_per_day,
                    "workout_place": workout_place,
                    "diet_type": diet_type,
                    "allergies": allergies,
                    "sleep_hours": sleep_hours,
                    "medical_conditions": medical_conditions,
                    "injuries": injuries,
                    "medications": medications,
                    "consent": consent
                }
                save_profile(user_profile)
                st.success("✅ Profile saved successfully! You can now use all features.")
                st.balloons()

st.markdown("---")
st.markdown("<p style='text-align: center; color: #888; font-size: 12px;'>Your data is stored locally. Never share medical information with others.</p>", unsafe_allow_html=True)
