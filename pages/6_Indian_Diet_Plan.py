import streamlit as st
import json
import os

PROFILE_PATH = "data/user_profile.json"

st.set_page_config(page_title="Diet Planner", page_icon="🥗")
st.title("🥗 Personalized Indian Diet Plan")
st.write("Simple, realistic Indian meals based on your goal & diet preference.")

# ---------- Load Profile ----------
def load_profile():
    if os.path.exists(PROFILE_PATH):
        with open(PROFILE_PATH, "r") as f:
            return json.load(f)
    return None

profile = load_profile()
if profile is None:
    st.warning("⚠️ Please complete your profile first.")
    st.stop()

goal = profile.get("primary_goal")
diet = profile.get("diet_type")

st.subheader(f"🎯 Goal: {goal}")
st.subheader(f"🍽 Diet Type: {diet}")

st.divider()

# ---------- Diet Logic ----------
def get_diet_plan(goal, diet):
    if diet == "Vegetarian":
        base = {
            "Breakfast": "Oats + milk + fruits",
            "Lunch": "Dal, roti, sabzi, salad",
            "Snack": "Roasted chana / fruit",
            "Dinner": "Paneer or tofu + vegetables"
        }
    elif diet == "Non-Vegetarian":
        base = {
            "Breakfast": "Egg omelette + toast",
            "Lunch": "Chicken curry + rice/roti",
            "Snack": "Boiled eggs / peanuts",
            "Dinner": "Grilled chicken + veggies"
        }
    elif diet == "Vegan":
        base = {
            "Breakfast": "Poha / oats + fruits",
            "Lunch": "Rajma/chole + rice",
            "Snack": "Fruit + nuts",
            "Dinner": "Tofu sabzi + roti"
        }
    else:  # Jain / Eggetarian fallback
        base = {
            "Breakfast": "Fruit bowl + nuts",
            "Lunch": "Dal, roti, ghee, sabzi",
            "Snack": "Buttermilk / sprouts",
            "Dinner": "Light sabzi + roti"
        }

    if goal == "Fat Loss":
        base["Tip"] = "Control portions, avoid sugar & fried food"
    elif goal == "Muscle Gain":
        base["Tip"] = "Add protein: paneer, eggs, chicken, dal"
    elif goal == "Strength":
        base["Tip"] = "Eat enough carbs + protein"
    else:
        base["Tip"] = "Maintain balanced meals"

    return base

diet_plan = get_diet_plan(goal, diet)

# ---------- Display ----------
st.header("📋 Your Daily Meal Plan")

for meal, food in diet_plan.items():
    st.markdown(f"**{meal}:** {food}")

st.divider()

st.info("💡 Tip: Drink 3–4 liters of water daily and sleep 7–8 hours.")
