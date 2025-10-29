import streamlit as st  # type: ignore

# Import pages
from page_views import (
    dataset_explorer,
    home,
    form_predict,
    csv_upload,
    model_evaluation,
    dashboard,
    model_comparison,
    ai_assistant,
    project_background,
)

st.set_page_config(page_title="Hospital Readmission Predictor", layout="centered")
st.title("🏥 Hospital Readmission Prediction System")

# Sidebar Navigation
st.sidebar.markdown("## 🚀 Navigation")
choice = st.sidebar.radio("", [
    "🏠 Home", 
    "📖 Project Background",
    "📝 Predict from Form", 
    "📁 Upload CSV", 
    "📊 Model Evaluation", 
    "🔍 Dataset Exploration", 
    "📈 Dashboard", 
    "📌 Model Comparison", 
    "🤖 AI Assistant"
])

# Routing Logic
if choice == "🏠 Home":
    home.render()
elif choice == "📖 Project Background":  
    project_background.render()
elif choice == "📝 Predict from Form":
    form_predict.render()
elif choice == "📁 Upload CSV":
    csv_upload.render()
elif choice == "📊 Model Evaluation":
    model_evaluation.render()
elif choice == "🔍 Dataset Exploration":
    dataset_explorer.render()
elif choice == "📈 Dashboard":
    dashboard.render()
elif choice == "📌 Model Comparison":
    model_comparison.render()
elif choice == "🤖 AI Assistant":
    ai_assistant.render()
