# utils/shap_plot.py
import shap
import plotly.graph_objects as go
import streamlit as st
from utils.gemini_intent import model

def generate_shap_plot(model_obj, input_df):
    explainer = shap.TreeExplainer(model_obj)
    shap_values = explainer.shap_values(input_df)

    st.write("### 🔍 SHAP Explanation of Prediction")
    st.markdown("""
    **ℹ️ How to read this chart:**
    - 🔵 Blue bars decrease the likelihood of readmission.
    - 🔴 Red bars increase it.
    - The base value is the model’s average prediction before seeing patient-specific data.
    """)

    # Prepare data for Plotly waterfall
    shap_values_list = shap_values[0]
    base_value = float(explainer.expected_value)
    final_value = float(base_value + sum(shap_values_list))

    features = input_df.columns.tolist()
    values = shap_values_list.tolist()
    measure = ["relative"] * len(features) + ["total"]
    x_labels = features + ["Prediction"]
    y_values = values + [final_value]
    colors = ["#EF553B" if val > 0 else "#636EFA" for val in values] + ["#00CC96"]

    fig = go.Figure(go.Waterfall(
        orientation="v",
        measure=measure,
        x=x_labels,
        y=y_values,
        text=[f"{float(v):+.2f}" for v in y_values],
        connector={"line": {"color": "gray"}},
        increasing={"marker": {"color": "#EF553B"}},
        decreasing={"marker": {"color": "#636EFA"}},
        totals={"marker": {"color": "#00CC96"}}
    ))

    fig.update_layout(
        title="SHAP Feature Impact on Prediction",
        yaxis_title="Impact on Model Output",
        waterfallgroupgap=0.4
    )

    st.plotly_chart(fig, use_container_width=True)

def explain_with_gemini(model_obj, input_df, prediction, probability):
    explainer = shap.TreeExplainer(model_obj)
    shap_values = explainer.shap_values(input_df)

    shap_impact = dict(zip(input_df.columns, shap_values[0]))
    base_value = float(explainer.expected_value)
    fx_val = float(base_value + sum(shap_values[0]))
    prob_percent = round(float(probability) * 100, 2)

    prompt = f"""
    You are helping explain a LightGBM model prediction for hospital readmission among diabetic patients.

    Prediction: {"Readmitted" if prediction == 1 else "Not Readmitted"}
    Predicted probability of readmission: {prob_percent}%

    Base value (E[f(X)]): {round(base_value, 2)}
    Final model output (f(x)): {round(fx_val, 2)}

    Here are the SHAP impact values showing how each feature influenced the prediction.
    Positive values increase readmission risk, negative values reduce it:

    {shap_impact}

    Please provide a clear explanation of why this prediction was made, referencing the most influential features and what they imply about the patient's risk. Begin with the predicted probability.
    """

    try:
        response = model.generate_content(prompt)
        st.markdown("### 🧠 Gemini Explanation of Prediction")
        st.info(response.text)
    except Exception as e:
        st.warning("Could not generate Gemini explanation.")
        st.text(str(e))
