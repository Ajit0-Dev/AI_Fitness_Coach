import streamlit as st
import json
import os

PROFILE_PATH = "data/user_profile.json"

st.title("👤 User Profile & Personalization")
st.write("This information helps the AI create safe and personalized fitness plans.")

# Helper_Function----------->

def load_profile():
    if os.path.exists(PROFILE_PATH):
        with open(PROFILE_PATH, "r") as f:
            return json.load(f)
    return {}

def save_profile(data):
    with open(PROFILE_PATH, "w") as f:
        json.dump(data, f, indent=4)

profile = load_profile()

st.header("1️⃣ Basic Personal Details")

name = st.text_input("Full Name ", profile.get("name", ""))

age = st.number_input("Age", 10, 100, profile.get("age", 25))

gender = st.selectbox(
    "Gender",
    ["Male", "Female", "Other"],
    index = ["Male", "Female", "Others"].index(profile.get("gender", "Male"))
)

height = st.number_input("Height (cm)", 100, 250, profile.get("height", 170))

weight = st.number_input("weight (kg)", 30, 200, profile.get("weight", 70))

activity_level = st.selectbox(
    "Daily Activity Level",
    ["Sedentary", "Moderately Active", "Highly Active"],
    index=["Sedentary", "Moderately Active", "Highly Active"].index(
        profile.get("activity_level", "Sedentary")
    )
)


#-----------FIteness_Detials--------------->

st.header("2️⃣ Fitness & Body Information")

fitness_level = st.selectbox(
    "Fitness Level",
    ["Beginner", "Intermediate", "Advanced"],
    index=["Beginner", "Intermediate", "Advanced"].index(profile.get("fitness_level", "Beginner")
    )
)

training_experience = st.number_input(
    "Training Experience (months)",
    0, 240,
    profile.get("training_experience", 0)
)

#---------Goals------------->

st.header("3️⃣ Goals & Preferences")

primary_goal = st.selectbox(
    "Primary Goal",
    ["Fat Loss", "Muscle Gain", "Strength", "Recomposition", "General Fitness"],
    index=["Fat Loss", "Muscle Gain", "Strength", "Recomposition", "General Fitness"].index(
        profile.get("primary_goal", "Fat Loss")
    )
)

time_per_day = st.slider(
    "Time Available Per Day (minutes)",
    15, 120,
    profile.get("time_per_day", 45)
)

workout_place = st.selectbox(
    "Workout Preference",
    ["Gym", "Home", "Mixed"],
    index=["Gym", "Home", "Mixed"].index(
        profile.get("workout_place", "Gym")
    )
)

#------------Diet and LifeStyle------------>

diet_type = st.selectbox(
    "Diet Type",
    ["Vegetarian", "Non-Vegetarian", "Vegan", "Eggetarian", "Jain"],
    index=["Vegetarian", "Non-Vegetarian", "Vegan", "Eggetarian", "Jain"].index(
        profile.get("diet_type", "Vegetarian")
    )
)

allergies = st.text_input(
    "Food Allergies (comma separated)",
    profile.get("allergies", "")
)

sleep_hours = st.slider(
    "Average Sleep Hours",
    3, 10,
    profile.get("sleep_hours", 7)
)

st.header(" 5️⃣ Medical & Injury Information ⚠️")


medical_conditions = st.multiselect(
    "Medical Conditions",
    ["Diabetes", "Thyroid", "Blood Pressure", "PCOS/PCOD", "Heart Issues", "Asthma", "None"],
    profile.get("medical_conditions", ["None"])
)


injuries = st.multiselect(
    "Injuries / Physical Issues",
    ["Knee Pain", "Back Pain", "Shoulder Pain", "Neck Pain", "Recent Surgery", "None"],
    profile.get("injuries", ["None"])
)


medications = st.text_area(
    "Current Medications (optional)",
    profile.get("medications", "")
)

st.header("6️⃣ Consent")

# User must accept disclaimer
consent = st.checkbox(
    "I understand this is not medical advice",
    profile.get("consent", False)
)

if st.button("💾 Save Profile"):

    if not consent:
         st.error("You must accept the disclaimer to continue.")

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

         st.success("✅ Profile saved successfully!")
         
 
