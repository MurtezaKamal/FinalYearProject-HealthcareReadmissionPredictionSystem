# pages/home.py
import streamlit as st # type: ignore

def render():
    st.markdown("---")

    # Introduction section
    st.subheader("📌 Project Overview")
    st.markdown("""
    This system is designed to assist healthcare professionals in identifying diabetic patients 
    who are at risk of being readmitted to the hospital. By analyzing a variety of clinical, 
    demographic, and treatment-related factors, it leverages machine learning—particularly the Gradient Boosting algorithm—
    to make accurate and data-driven predictions.
    """)

    # Core features section
    st.subheader("🔧 System Features")
    st.markdown("""
    - **📖 Project Background**: Learn about the dataset, methodology, and overall approach used in this project.  
    - **📝 Predict from Form**: Enter patient-level data and get a personalized readmission prediction in real time.  
    - **📁 Upload CSV**: Upload a file containing multiple records for batch processing and prediction.  
    - **📊 Model Evaluation**: Explore model performance using metrics like accuracy, AUC, precision, recall, and confusion matrix.  
    - **🔍 Dataset Exploration**: Filter and examine key patterns across demographic and clinical attributes.  
    - **📈 Dashboard**: Visualize trends across race, age, diagnoses, visit history, and hospital utilization.  
    - **📌 Model Comparison**: Compare various machine learning models evaluated throughout the project.  
    - **🤖 AI Assistant**: Ask questions using natural language and receive intelligent insights powered by Gemini + pandas.
    """)

    # Dataset section
    st.subheader("📂 Dataset Summary")
    st.markdown("""
    The system was trained on a real-world hospital dataset containing over 100,000 patient records.  
    Features include demographics, diagnosis codes, lab results, medications, and hospital utilization metrics.  
    All data was carefully preprocessed and encoded to ensure optimal model performance.
    """)

    # Visual or CTA (optional)
    st.markdown("---")
    st.success("Use the sidebar to navigate through the system and explore its capabilities!")
