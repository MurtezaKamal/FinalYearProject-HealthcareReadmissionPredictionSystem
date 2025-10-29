# pages/project_background.py

import streamlit as st # type: ignore

def render():
    st.title("📖 Project Background")
    
    st.subheader("🎯 Problem Statement")
    st.markdown("""
    Diabetes-related hospital readmissions pose a significant burden on global healthcare systems, both financially and in terms of patient well-being. 
    Diabetic patients have almost double the readmission rate of non-diabetic individuals. This project aims to leverage machine learning to 
    predict hospital readmissions among diabetic patients, enabling timely intervention and better patient care.
    """)

    st.subheader("📂 Dataset Overview")
    st.markdown("""
    - **Source**: [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008)  
    - **Name**: Diabetes 130-US Hospitals for Years 1999–2008  
    - **Size**: ~100,000 records from 130 hospitals  
    - **Attributes**: Demographics, diagnoses, lab tests, medications, and admission details  
    - **Target Variable**: Whether a patient is readmitted within 30 days
    """)

    st.subheader("🧹 Data Preprocessing Summary")
    st.markdown("""
    - Removed missing and redundant values  
    - Encoded categorical variables (e.g., age, race, gender, diagnoses)  
    - Engineered features such as **Number of Medication Changes** and **Number of Visits**  
    - Addressed outliers via Winsorization  
    - Transformed readmission into a binary classification target
    """)

    st.subheader("📊 Exploratory Data Analysis (EDA)")
    st.markdown("""
    - Visualized distributions for attributes like age, gender, diagnoses, time in hospital  
    - Analyzed trends in readmission across race, medication use, and admission types  
    - Performed correlation analysis to understand feature relationships  
    - Found that frequent visits and inpatient history are most correlated with readmission risk
    """)

    st.subheader("🤖 Modeling Approach")
    st.markdown("""
    - Adopted the **CRISP-DM** methodology  
    - Tested models: Logistic Regression, Random Forest, CatBoost, LightGBM, XGBoost  
    - Final model selection based on evaluation metrics: Accuracy, AUC, Precision, Recall  
    - Incorporated **Explainable AI (SHAP)** to interpret model decisions
    """)

    st.subheader("🚀 Deployment & System")
    st.markdown("""
    - Built using **Streamlit** with an intuitive sidebar-based navigation  
    - Key features include:  
        • Manual prediction form  
        • CSV-based batch prediction  
        • Interactive dashboard with filters  
        • AI Assistant (Gemini + pandas hybrid)  
        • Model evaluation with confusion matrix and AUC  
    """)

    st.subheader("🌍 Alignment with SDG 3")
    st.markdown("""
    This project contributes to **Sustainable Development Goal 3: Good Health and Well-Being** by:
    - Supporting early intervention for diabetic patients  
    - Reducing avoidable hospitalizations  
    - Promoting data-driven healthcare delivery
    """)

