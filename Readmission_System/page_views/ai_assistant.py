# pages/ai_assistant.py
import streamlit as st # type: ignore
import pandas as pd
import numpy as np
from utils.gemini_intent import get_user_intent, model
from utils.ai_helpers import run_fallback_query, decode_dataframe
from utils.mappings import encoding_maps

def render():
    st.subheader("🤖 AI Assistant (Gemini Hybrid + Pandas Mode)")
    st.markdown("You can ask questions like:")
    st.markdown("- What's the readmission rate?")
    st.markdown("- How many male Asian patients were readmitted?")
    st.markdown("- How many patients aged 50–60 were not readmitted?")

    df = pd.read_csv("data/FYP_Cleaned2.csv")

    user_query = st.text_input("Type your question here:")

    if st.button("Ask Gemini"):
        with st.spinner("Thinking..."):
            try:
                fallback_keywords = [
                    "how many", "patients", "age", "gender", "race", "readmitted",
                    "diabetesMed", "transferred", "discharge", "admission", "hospice", "expired"
                ]
                use_fallback = any(word in user_query.lower() for word in fallback_keywords)

                # Check for high-level intent
                intent = get_user_intent(user_query)

                # Fallback to pandas query
                if intent == "unknown" or use_fallback:
                    code_expr = run_fallback_query(user_query, df)
                    st.markdown("**🔍 Interpreted Code:**")
                    st.code(code_expr, language="python")

                    result = eval(code_expr, {}, {"df": df})

                    # Display
                    if isinstance(result, (pd.Series, pd.DataFrame)):
                        decoded_result = decode_dataframe(result, encoding_maps)
                        st.markdown("**📊 Result:**")
                        st.dataframe(decoded_result)
                    elif isinstance(result, (int, float, np.integer, np.float64)):
                        st.markdown(f"**📌 Answer:** {int(result)} patients match your query.")
                    else:
                        st.markdown(f"**📌 Answer:** {result}")

                    # Natural language explanation
                    explain_prompt = f"The user asked: '{user_query}'\nThe result was: {result}\nExplain what this means in plain English."
                    explanation = model.generate_content(explain_prompt).text.strip()
                    st.markdown(f"**🧠 Gemini's Explanation:**\n\n{explanation}")

                else:
                    # Structured rule-based intent
                    correlation_matrix = df.corr()
                    feature_importances = {
                        "number_inpatient": 0.22,
                        "number_emergency": 0.18,
                        "number_of_visits": 0.16,
                        "time_in_hospital": 0.14,
                        "number_diagnoses": 0.10,
                        "number_outpatient": 0.08,
                        "num_lab_procedures": 0.06,
                        "numchange": 0.05,
                        "admission_source_id": 0.01,
                        "diabetesMed": 0.003
                    }
                    model_scores = {
                        "LightGBM (Random Search)": {"accuracy": 0.8098, "auc": 0.8692},
                        "CatBoost (Random Search)": {"accuracy": 0.8097, "auc": 0.8689},
                        "LightGBM (Grid Search)": {"accuracy": 0.8096, "auc": 0.8689},
                        "XGBoost (Grid Search)": {"accuracy": 0.8095, "auc": 0.8683},
                        "CatBoost (Base Model)": {"accuracy": 0.8091, "auc": 0.8689}
                    }

                    from utils.ai_helpers import respond_to_query
                    response = respond_to_query(intent, df, correlation_matrix, feature_importances, model_scores)
                    st.markdown(f"**🤖 Gemini says:**\n\n{response}")

            except Exception as e:
                st.error(f"❌ Error: {e}")
