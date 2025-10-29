# pages/csv_upload.py
import streamlit as st # type: ignore
import pandas as pd
import numpy as np
from utils.model_loader import load_model

def render():
    st.subheader("📄 Batch Prediction from CSV File (Top 10 Features)")

    st.markdown("""
    Upload a CSV file containing the top 10 features used by the model.  
    All column names must match exactly as shown below.  
    You can download a sample template and fill it with your own patient records.
    """)

    st.markdown("**📋 Expected Columns:**")
    st.markdown("""
    - `number_of_visits`  
    - `number_inpatient`  
    - `number_diagnoses`  
    - `number_emergency`  
    - `number_outpatient`  
    - `admission_source_id`  
    - `diabetesMed`  
    - `numchange`  
    - `time_in_hospital`  
    - `num_lab_procedures`
    """)

    # Sample data template
    sample_data = {
        "number_of_visits": [1],
        "number_inpatient": [0],
        "number_diagnoses": [5],
        "number_emergency": [1],
        "number_outpatient": [0],
        "admission_source_id": [2],
        "diabetesMed": ["Yes"],
        "numchange": [1],
        "time_in_hospital": [3],
        "num_lab_procedures": [45]
    }

    sample_df = pd.DataFrame(sample_data)
    sample_csv = sample_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Sample CSV Template",
        data=sample_csv,
        file_name="sample_input_template.csv",
        mime="text/csv"
    )

    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file is not None:
        try:
            input_df = pd.read_csv(uploaded_file)

            required_columns = [
                "number_of_visits",
                "number_inpatient",
                "number_diagnoses",
                "number_emergency",
                "number_outpatient",
                "admission_source_id",
                "diabetesMed",
                "numchange",
                "time_in_hospital",
                "num_lab_procedures"
            ]

            missing_cols = [col for col in required_columns if col not in input_df.columns]
            if missing_cols:
                st.error(f"❌ Missing columns in uploaded file: {missing_cols}")
                return

            # Map diabetesMed Yes/No to 1/0
            input_df["diabetesMed"] = input_df["diabetesMed"].map({"Yes": 1, "No": 0})

            # Load model
            model = load_model("Top10Model/lightgbm_top10_randomsearch.pkl")

            # Predict
            predictions = model.predict(input_df[required_columns])
            input_df["Prediction"] = ["Readmitted" if p == 1 else "Not Readmitted" for p in predictions]

            st.success("✅ Predictions complete!")
            st.dataframe(input_df)

            csv_output = input_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Prediction Results as CSV",
                data=csv_output,
                file_name='batch_predictions.csv',
                mime='text/csv',
            )

        except Exception as e:
            st.error(f"❌ Error processing file: {e}")
