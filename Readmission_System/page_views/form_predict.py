# pages/form_predict.py
import streamlit as st # type: ignore
import numpy as np
import pandas as pd
from utils.model_loader import load_model
from utils.shap_plot import generate_shap_plot, explain_with_gemini

def render():
    st.subheader("Manual Input Form (Top 10 Features + SHAP Explanation)")

    # Mapping for diabetesMed
    diabetesMed_map = {"Yes": 1, "No": 0}

    # Grouped admission source mapping
    admission_source_options = {
        "Referral (Clinic, Physician, HMO)": 0,
        "Transfer from Healthcare Facility (SNF, rehab, etc.)": 1,
        "Emergency Admission": 2,
        "Birth / Neonatal Care": 3,
        "Readmission or Home Health Referral": 4
    }

    # ---- Input Fields with Help Tooltips ----
    number_of_visits = st.number_input(
        "Number of Visits", 
        min_value=0, 
        help="Total number of hospital visits (sum of inpatient, outpatient, and emergency visits)."
    )

    number_inpatient = st.number_input(
        "Number of Inpatient Visits", 
        min_value=0,
        help="Number of times the patient was admitted as an inpatient (overnight stay)."
    )

    number_diagnoses = st.slider(
        "Number of Diagnoses", 0, 20,
        help="Number of distinct ICD-9 diagnoses entered during the encounter (1–20)."
    )

    number_emergency = st.number_input(
        "Number of Emergency Visits", 
        min_value=0,
        help="Number of emergency room visits in the year preceding the hospital encounter."
    )

    number_outpatient = st.number_input(
        "Number of Outpatient Visits", 
        min_value=0,
        help="Number of outpatient visits (i.e., visits not requiring admission)."
    )

    admission_source_label = st.selectbox(
        "Admission Source", 
        list(admission_source_options.keys()),
        help="How the patient was admitted (e.g., emergency, referral, transfer, etc.)."
    )
    admission_source_id = admission_source_options[admission_source_label]

    diabetesMed = st.selectbox(
        "On Diabetes Medication?", 
        ["Yes", "No"],
        help="Indicates whether the patient was prescribed diabetes medication during the encounter."
    )

    numchange = st.number_input(
        "Number of Medication Changes", 
        min_value=0,
        help="Number of medications that were either started, stopped, or changed during the encounter."
    )

    time_in_hospital = st.slider(
        "Time in Hospital (days)", 1, 30,
        help="Length of stay in the hospital in days (1–14 typical, capped at 30)."
    )

    num_lab_procedures = st.slider(
        "Number of Lab Procedures", 0, 100,
        help="Number of lab tests performed during the encounter."
    )

    # ------------------ Prediction ------------------ #
    if st.button("Predict Readmission"):
        try:
            # Prepare input
            input_data = np.array([[
                number_of_visits,
                number_inpatient,
                number_diagnoses,
                number_emergency,
                number_outpatient,
                admission_source_id,
                diabetesMed_map[diabetesMed],
                numchange,
                time_in_hospital,
                num_lab_procedures
            ]])
            feature_names = [
                "number_of_visits", "number_inpatient", "number_diagnoses",
                "number_emergency", "number_outpatient", "admission_source_id",
                "diabetesMed", "numchange", "time_in_hospital", "num_lab_procedures"
            ]
            input_df = pd.DataFrame(input_data, columns=feature_names)

            # Load model
            model = load_model("Top10Model/lightgbm_top10_randomsearch.pkl")

            # Predict with probability
            probability = float(model.predict_proba(input_df)[0][1])
            prediction = 1 if probability >= 0.5 else 0
            label = "Readmitted" if prediction == 1 else "Not Readmitted"

            st.success(f"Prediction: **{label}**")
            st.info(f"📊 Probability of Readmission: **{probability:.2%}**")

            # SHAP Plot + Gemini Explanation
            generate_shap_plot(model, input_df)
            explain_with_gemini(model, input_df, prediction, probability)

        except Exception as e:
            st.error(f"Something went wrong: {e}")
