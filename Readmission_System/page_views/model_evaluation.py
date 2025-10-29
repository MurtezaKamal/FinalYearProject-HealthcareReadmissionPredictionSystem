import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import joblib
from utils.ai_helpers import explain_model_metrics_with_gemini

def render():
    st.subheader("📊 LightGBM Model Evaluation (Hyper-Tuning Random Search CV)")

    st.markdown("""
    This evaluation showcases the performance of a LightGBM model trained on the dataset,  
    optimized using **RandomizedSearchCV (5-fold, 50 iterations)**.  
    The metrics below reflect the model's ability to classify whether a diabetic patient will be readmitted.
    """)

    try:
        # Load saved metrics
        metrics = joblib.load("EvaluationMetrics/Lightgbm_Randomsearch_Metrics.pkl")
        report = metrics["classification_report"]
        cm = metrics["confusion_matrix"]
        roc_auc = metrics["roc_auc"]
        accuracy = metrics["accuracy"]
        if "roc_curve" in metrics:
            fpr = metrics["roc_curve"].get("fpr")
            tpr = metrics["roc_curve"].get("tpr")
        else:
            fpr = metrics.get("fpr")
            tpr = metrics.get("tpr")

        # ---------- Classification Report ---------- #
        st.write("### 🧾 Classification Report")
        st.markdown("""
        - **Precision**: Of predicted positives, how many were actually positive  
        - **Recall**: Of actual positives, how many were predicted correctly  
        - **F1-Score**: Harmonic mean of precision and recall  
        """)

        report_df = pd.DataFrame(report).transpose()
        report_df = report_df[["precision", "recall", "f1-score", "support"]].round(3)

        # Format accuracy row
        if "accuracy" in report_df.index:
            report_df.loc["accuracy", ["precision", "recall", "f1-score"]] = report_df.loc["accuracy", "precision"]
            report_df.loc["accuracy", "support"] = None

        report_df["support"] = report_df["support"].apply(lambda x: f"{int(x):,}" if pd.notna(x) else "")

        def dark_mode_friendly_style(report_df):
            return (
            report_df.style
            .format("{:.3f}", subset=["precision", "recall", "f1-score"])
            .apply(lambda s: ['background-color: #2e2f38; color: #f1f1f1']*len(s) if s.name == 'accuracy' else ['']*len(s), axis=1)
            .background_gradient(cmap="PuBuGn", subset=["precision", "recall", "f1-score"], axis=None)
            .set_properties(subset=["precision", "recall", "f1-score", "support"], **{
                'text-align': 'center',
                'font-size': '14px',
                'padding': '8px',
                'color': 'white',
                'background-color': '#1e1e1e',
                'border': '1px solid #3a3a3a'
            })
            .set_table_styles([
                {"selector": "th", "props": [
                    ("font-size", "14px"),
                    ("text-align", "center"),
                    ("color", "white"),
                    ("background-color", "#111"),
                    ("padding", "8px")
                ]},
                {"selector": "td", "props": [
                    ("border", "1px solid #3a3a3a")
                ]},
                {"selector": "caption", "props": [
                    ("caption-side", "top"),
                    ("font-size", "16px"),
                    ("color", "#ccc"),
                    ("text-align", "center"),
                    ("padding", "10px")
                ]}
            ])
            .set_caption("📋 Detailed Classification Report")
        )

        styled_report = dark_mode_friendly_style(report_df)
        st.dataframe(styled_report, use_container_width=True)

        # ---------- Confusion Matrix (Plotly) ---------- #
        st.write("### 📘 Confusion Matrix (Interactive)")
        fig_cm = go.Figure(data=go.Heatmap(
            z=cm,
            x=["Predicted 0", "Predicted 1"],
            y=["Actual 0", "Actual 1"],
            colorscale="Blues",
            showscale=True,
            text=cm,
            texttemplate="%{text}"
        ))
        fig_cm.update_layout(title="Confusion Matrix Heatmap", xaxis_title="Predicted", yaxis_title="Actual")
        st.plotly_chart(fig_cm)

        # ---------- ROC AUC Score ---------- #
        st.write("### 🎯 ROC AUC Score")
        st.markdown("""
        **AUC (Area Under Curve)** measures how well the model distinguishes between classes.  
        A score closer to 1.0 indicates excellent performance.
        """)
        st.metric(label="ROC AUC", value=f"{roc_auc:.4f}")
        st.metric(label="Accuracy", value=f"{accuracy:.4f}")

        # ---------- ROC Curve ---------- #
        st.write("### 📈 ROC Curve")
        fig_roc = go.Figure()
        fig_roc.add_trace(go.Scatter(
            x=fpr,
            y=tpr,
            mode='lines',
            name='ROC Curve',
            line=dict(color='blue')
        ))
        fig_roc.add_trace(go.Scatter(
            x=[0, 1],
            y=[0, 1],
            mode='lines',
            name='Random Guess',
            line=dict(dash='dash', color='gray')
        ))
        fig_roc.update_layout(
            xaxis_title='False Positive Rate',
            yaxis_title='True Positive Rate',
            title='ROC Curve',
            width=700,
            height=500
        )
        st.plotly_chart(fig_roc)

        # ---------- Gemini Explanation ---------- #
        st.write("### 🤖 Gemini Interpretation")
        with st.spinner("Generating explanation with Gemini..."):
            gemini_explanation = explain_model_metrics_with_gemini(accuracy, roc_auc, report)
        with st.expander("📘 What does this mean? (AI Explanation)"):
            st.markdown(gemini_explanation)

    except Exception as e:
        st.error(f"❌ Could not load evaluation metrics: {e}")
