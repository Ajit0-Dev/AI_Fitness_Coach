import streamlit as st
import json
import os

PROFILE_PATH = "data/user_profile.json"

st.set_page_config(page_title="Indian Diet Plan - AI Fitness Coach", page_icon="🥗", layout="wide")

st.markdown("""
    <style>
    h1 { color: #ff6b35 !important; font-weight: 900 !important; }
    h2 { color: #1a73e8 !important; border-bottom: 3px solid #ff6b35 !important; padding-bottom: 10px !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🥗 Indian Cuisine Diet Planner")
st.markdown("Authentic Indian meals aligned with your fitness goals")
st.markdown("---")

# Load Profile
def load_profile():
    if os.path.exists(PROFILE_PATH):
        with open(PROFILE_PATH, "r") as f:
            return json.load(f)
    return None

profile = load_profile()
if profile is None:
    st.warning("⚠️ Please complete your profile first.")
    st.info("Go to the Profile page to get started!")
    st.stop()

goal = profile.get("primary_goal")
diet = profile.get("diet_type")

# Display profile info
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🎯 Goal", goal)
with col2:
    st.metric("🍽️ Diet Type", diet)
with col3:
    st.metric("📊 Weight", f"{profile.get('weight')} kg")

st.markdown("---")

# Diet Logic with enhanced Indian meals
def get_diet_plan(goal, diet):
    if diet == "Vegetarian":
        base = {
            "Breakfast": {
                "meal": "Masala Oats with Paneer / Poha with vegetables",
                "items": ["Oats (50g)", "Paneer (100g)", "Green vegetables", "Milk"],
                "protein": "High"
            },
            "Mid-Morning": {
                "meal": "Sprouts Salad with Lemon & Olive Oil",
                "items": ["Moong sprouts (100g)", "Carrots", "Cucumber", "Lemon"],
                "protein": "Medium"
            },
            "Lunch": {
                "meal": "Dal with Brown Rice and Sabzi",
                "items": ["Mixed Dal (150g cooked)", "Brown Rice (150g)", "Seasonal vegetables", "Ghee"],
                "protein": "High"
            },
            "Evening Snack": {
                "meal": "Paneer Tikka or Roasted Chickpeas",
                "items": ["Paneer (100g) OR Chickpeas (80g roasted)", "Spices", "Yogurt"],
                "protein": "High"
            },
            "Dinner": {
                "meal": "Tofu Curry with Roti",
                "items": ["Paneer/Tofu (150g)", "Whole Wheat Roti (2)", "Vegetables", "Low-fat yogurt"],
                "protein": "High"
            }
        }
    elif diet == "Non-Vegetarian":
        base = {
            "Breakfast": {
                "meal": "Egg Masala Omelette with Toast",
                "items": ["3 Eggs", "Whole Wheat Toast", "Tomato", "Onion", "Spices"],
                "protein": "High"
            },
            "Mid-Morning": {
                "meal": "Chicken Salad",
                "items": ["Chicken Breast (100g grilled)", "Mixed greens", "Lemon", "Olive oil"],
                "protein": "High"
            },
            "Lunch": {
                "meal": "Tandoori Chicken with Basmati Rice",
                "items": ["Chicken Breast (150g)", "Basmati Rice (150g)", "Yogurt marinade", "Vegetables"],
                "protein": "High"
            },
            "Evening Snack": {
                "meal": "Boiled Eggs with Fruit",
                "items": ["2 Boiled Eggs", "Apple or Banana", "Almonds (10)"],
                "protein": "High"
            },
            "Dinner": {
                "meal": "Grilled Fish Curry with Roti",
                "items": ["Fish Fillet (150g)", "Whole Wheat Roti (2)", "Coconut curry", "Vegetables"],
                "protein": "High"
            }
        }
    elif diet == "Vegan":
        base = {
            "Breakfast": {
                "meal": "Chickpea Flour Pancakes (Cheela)",
                "items": ["Chickpea flour (50g)", "Vegetables", "Cumin seeds", "Coconut oil"],
                "protein": "High"
            },
            "Mid-Morning": {
                "meal": "Fruit and Nut Mix",
                "items": ["Banana", "Almonds (10)", "Walnuts (5)", "Dates"],
                "protein": "Medium"
            },
            "Lunch": {
                "meal": "Rajma with Brown Rice",
                "items": ["Kidney Beans (150g cooked)", "Brown Rice (150g)", "Vegetables", "Coconut oil"],
                "protein": "High"
            },
            "Evening Snack": {
                "meal": "Roasted Chickpeas & Pumpkin Seeds",
                "items": ["Chickpeas (80g roasted)", "Pumpkin seeds (30g)", "Spices"],
                "protein": "High"
            },
            "Dinner": {
                "meal": "Tofu Stir-Fry with Quinoa",
                "items": ["Tofu (150g)", "Quinoa (100g cooked)", "Mixed vegetables", "Sesame oil"],
                "protein": "High"
            }
        }
    else:  # Jain / Eggetarian
        base = {
            "Breakfast": {
                "meal": "Fruit Bowl with Nuts",
                "items": ["Mixed fruits", "Almonds", "Walnuts", "Coconut milk"],
                "protein": "Medium"
            },
            "Mid-Morning": {
                "meal": "Buttermilk with Spices",
                "items": ["Low-fat yogurt", "Cumin", "Salt", "Green chilli"],
                "protein": "High"
            },
            "Lunch": {
                "meal": "Dal & Vegetable Rice",
                "items": ["Moong Dal (150g cooked)", "Basmati Rice (150g)", "Seasonal vegetables", "Ghee"],
                "protein": "High"
            },
            "Evening Snack": {
                "meal": "Sprouts Salad",
                "items": ["Moong sprouts (100g)", "Carrot", "Cucumber", "Lemon juice"],
                "protein": "Medium"
            },
            "Dinner": {
                "meal": "Light Vegetable Curry with Roti",
                "items": ["Mixed vegetables (200g)", "Whole wheat roti (2)", "Yogurt", "Minimal oil"],
                "protein": "Medium"
            }
        }

    return base

diet_plan = get_diet_plan(goal, diet)

# Display Diet Plan
st.subheader("📋 Your Daily Meal Plan")

for meal_time, meal_info in diet_plan.items():
    with st.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{meal_time}**")
            st.markdown(f"🍽️ {meal_info['meal']}")
        with col2:
            st.markdown(f"**{meal_info['protein']} Protein**")
        
        st.markdown(f"**Ingredients:** {', '.join(meal_info['items'])}")
        st.divider()

st.markdown("---")

# Tips based on goal
st.subheader("💡 Personalized Tips for Your Goal")

tips = {
    "Fat Loss": """
    - **Portion Control:** Use smaller plates
    - **Hydration:** Drink 3-4L water daily
    - **Spices:** Use turmeric, ginger, green chilli for metabolism
    - **Timing:** No eating 2-3 hours before sleep
    - **Cardio:** Add 30 mins daily cardio with diet
    """,
    "Muscle Gain": """
    - **Calorie Surplus:** Eat 300-500 calories above maintenance
    - **Protein:** Aim for 1.6-2.2g per kg body weight
    - **Frequency:** Eat every 3-4 hours
    - **Indian Superfoods:** Paneer, moong, chickpeas, ghee
    - **Strength Training:** Combine with heavy resistance training
    """,
    "Strength": """
    - **Carbs & Protein:** Balance both for energy and recovery
    - **Traditional Foods:** Use ghee, milk, almonds for strength
    - **Pre-Workout:** Eat 1-2 hours before training
    - **Post-Workout:** Protein + carbs within 1 hour
    - **Sleep:** 7-8 hours for muscle recovery
    """,
    "Recomposition": """
    - **Maintenance Calories:** Stay at current calorie level
    - **High Protein:** 1.8-2.2g per kg body weight
    - **Strength Training:** Focus on progressive overload
    - **Clean Foods:** Reduce processed foods
    - **Consistency:** Track macros for 4-6 weeks
    """,
    "General Fitness": """
    - **Balance:** 50% carbs, 30% protein, 20% fats
    - **Whole Foods:** Prioritize unprocessed Indian foods
    - **Variety:** Include all food groups daily
    - **Hydration:** 2.5-3L water daily
    - **Moderation:** Enjoy traditional sweets occasionally
    """
}

tip = tips.get(goal, tips["General Fitness"])
st.info(tip)

st.markdown("---")
st.markdown("""
### 🌟 Pro Tips for Indian Cuisine
- Use **whole wheat roti** instead of white bread
- Cook with **ghee and coconut oil** in moderation
- Add **turmeric, ginger, and cumin** to every meal
- Drink **warm water with lemon** in the morning
- Rotate between different dal varieties for nutrition
- Make **overnight soaked moong** for better digestion
""")

