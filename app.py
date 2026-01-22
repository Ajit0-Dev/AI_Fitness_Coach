import streamlit as st

st.set_page_config(
    page_title="AI Fitness Coach - Professional Gym Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "AI Fitness Coach - Your Personal AI-Powered Fitness Companion"
    }
)

# Custom CSS for professional fitness app styling
st.markdown("""
    <style>
    /* Main theme colors - Muscular/Professional */
    :root {
        --primary-color: #ff6b35;
        --secondary-color: #004e89;
        --accent-color: #1a73e8;
        --dark-bg: #0d1117;
        --light-text: #ffffff;
    }
    
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #0d1117 0%, #1a1f2e 100%);
    }
    
    /* Title styling */
    h1 {
        color: #ff6b35 !important;
        font-weight: 900 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3) !important;
        letter-spacing: 1px !important;
    }
    
    h2 {
        color: #1a73e8 !important;
        border-bottom: 3px solid #ff6b35 !important;
        padding-bottom: 10px !important;
    }
    
    h3 {
        color: #004e89 !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #ff6b35 0%, #ff8c5a 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        padding: 12px 30px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 107, 53, 0.5) !important;
    }
    
    /* Input styling */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #1a1f2e !important;
        color: #ffffff !important;
        border: 2px solid #ff6b35 !important;
        border-radius: 6px !important;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background-color: #1a1f2e !important;
        color: #ffffff !important;
    }
    
    /* Slider styling */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #ff6b35, #1a73e8) !important;
    }
    
    /* Cards/Containers */
    .metric-card {
        background: linear-gradient(135deg, #1a1f2e 0%, #252d3d 100%);
        border-left: 5px solid #ff6b35;
        padding: 20px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    /* Sidebar styling */
    .stSidebar {
        background: linear-gradient(180deg, #0d1117 0%, #1a1f2e 100%) !important;
    }
    
    /* Warning/Info boxes */
    .stWarning {
        background-color: #2a1810 !important;
        border-left: 4px solid #ff6b35 !important;
    }
    
    .stSuccess {
        background-color: #1a2e1a !important;
        border-left: 4px solid #2ecc71 !important;
    }
    
    /* Text styling */
    p, span {
        color: #e0e0e0 !important;
    }
    
    /* Chat messages */
    .stChatMessage {
        background-color: #1a1f2e !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("# 💪 AI FITNESS COACH")
    st.markdown("### Professional AI-Powered Fitness & Nutrition Assistant")
with col2:
    st.markdown("")
    st.markdown("")
    

st.markdown("---")

# Fitness Stats section
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("💪 Muscle", "Building", "Grow Strong")
with col2:
    st.metric("⚡ Energy", "Boost", "Feel Powerful")
with col3:
    st.metric("🎯 Goal", "Focused", "Stay on Track")
with col4:
    st.metric("🔥 Burn", "Calories", "Get Results")

st.markdown("---")

# Features section
st.markdown("## 🌟 Features")
feature_col1, feature_col2, feature_col3 = st.columns(3)

with feature_col1:
    st.markdown("""
    **📋 User Profile**
    - Personalized assessment
    - Track fitness metrics
    - Medical history tracking
    """)

with feature_col2:
    st.markdown("""
    **🤖 AI Chatbot**
    - Expert fitness guidance
    - Form corrections
    - Nutrition advice
    """)

with feature_col3:
    st.markdown("""
    **🏋️ Workout Plans**
    - Customized programs
    - Progressive overload
    - Equipment-flexible
    """)

feature_col4, feature_col5, feature_col6 = st.columns(3)

with feature_col4:
    st.markdown("""
    **🥗 Diet Plans**
    - Indian cuisine focused
    - Goal-aligned nutrition
    - Allergy-safe
    """)

with feature_col5:
    st.markdown("""
    **📊 Analytics**
    - Progress tracking
    - Workout statistics
    - Goal monitoring
    """)

with feature_col6:
    st.markdown("""
    **📱 Tracking**
    - Weight logging
    - Workout history
    - Performance metrics
    """)

st.markdown("---")

# Getting started
st.markdown("## 🚀 Getting Started")
st.info("""
1️⃣ **Complete Your Profile** - Go to the "Profile" section to provide your fitness details
2️⃣ **Chat with AI Coach** - Ask questions in the Chatbot section
3️⃣ **Generate Plans** - Get personalized workout & diet plans
4️⃣ **Track Progress** - Monitor your fitness journey with analytics
""")

st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; color: #888; font-size: 12px; margin-top: 50px;'>
    <p>⚠️ <strong>Disclaimer:</strong> This AI assistant provides general fitness information. Always consult healthcare professionals for medical advice.</p>
    <p>© 2026 AI Fitness Coach </p>
</div>
""", unsafe_allow_html=True)
