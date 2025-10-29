# pages/model_compare.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import joblib

def render():
    st.subheader("📌 Comparison of Top 5 Machine Learning Models")

    st.markdown("""
    Below is a comparison of the top 5 models developed to predict hospital readmissions among diabetic patients.  
    Metrics were loaded directly from saved `.pkl` evaluation files.  
    Each hypertuned model was tuned using 5-fold cross-validation and evaluated based on ROC AUC, Precision, Recall, F1-Score, and Accuracy (for class 1: readmitted).
    """)

    # Path to the top 5 metrics
    model_info = {
        "LightGBM with Random Search CV": "EvaluationMetrics/Lightgbm_Randomsearch_Metrics.pkl",
        "CatBoost with Random Search CV": "EvaluationMetrics/CatBoost_Randomsearch_Metrics.pkl",
        "LightGBM with Grid Search CV": "EvaluationMetrics/Lightgbm_Gridsearch_Metrics.pkl",
        "XGBoost with Grid Search CV": "EvaluationMetrics/XGBoost_Gridsearch_Metrics.pkl",
        "CatBoost Base Model": "BaseModelMetrics/catboost_base_metrics.pkl"
    }

    data = {
        "Model": [],
        "ROC AUC": [],
        "Accuracy": [],
        "Precision (1)": [],
        "Recall (1)": [],
        "F1-Score (1)": []
    }

    # Read metrics from each model
    for model_name, file_path in model_info.items():
        try:
            metrics = joblib.load(file_path)
            report = metrics["classification_report"]
            auc = metrics["roc_auc"]
            accuracy = metrics.get("accuracy", None)

            if accuracy is None:
                accuracy = report.get("accuracy", None)

            precision = report["1"]["precision"]
            recall = report["1"]["recall"]
            f1 = report["1"]["f1-score"]

            data["Model"].append(model_name)
            data["ROC AUC"].append(round(auc, 4))
            data["Accuracy"].append(round(accuracy, 4) if accuracy is not None else None)
            data["Precision (1)"].append(round(precision, 4))
            data["Recall (1)"].append(round(recall, 4))
            data["F1-Score (1)"].append(round(f1, 4))

        except Exception as e:
            st.error(f"❌ Failed to load metrics for {model_name}: {e}")

    # Create DataFrame and sort by ROC AUC
    df_eval = pd.DataFrame(data).sort_values(by="ROC AUC", ascending=False).reset_index(drop=True)
    df_eval["Rank"] = df_eval.index + 1

    st.dataframe(df_eval)

   # ---------- Interactive Plotly Chart ---------- #
    st.markdown("### 📊 Visual Comparison")

    view_option = st.radio("Select view mode:", ["All Models", "Individual Model"], horizontal=True)

    if view_option == "All Models":
        models_to_plot = df_eval["Model"].tolist()
    else:
        models_to_plot = st.multiselect(
            "Select model(s) to compare:",
            options=df_eval["Model"].tolist(),
            default=df_eval["Model"].tolist()[0:1]
        )

    # Define metric and model colors
    metric_colors = {
        "ROC AUC": "skyblue",
        "Accuracy": "lightgreen",
        "Precision (1)": "lightcoral",
        "Recall (1)": "plum",
        "F1-Score (1)": "lightsalmon"
    }
    model_colors = px.colors.qualitative.Plotly  # will be used for single metric

    # Select metrics to show
    available_metrics = list(metric_colors.keys())
    metric_option = st.selectbox("Select metrics to display:", ["All"] + available_metrics)
    metrics_to_plot = available_metrics if metric_option == "All" else [metric_option]
    filtered_df = df_eval[df_eval["Model"].isin(models_to_plot)]

    fig = go.Figure()

    # =============== CASE: ALL METRICS (Grouped, colored by metric) =============== #
    if metric_option == "All":
        for metric in metrics_to_plot:
            fig.add_trace(go.Bar(
                x=filtered_df["Model"],
                y=filtered_df[metric],
                name=metric,
                marker_color=metric_colors.get(metric),
                text=filtered_df[metric].round(4),
                textposition='auto'
            ))
    # =============== CASE: ONE METRIC (Single, colored by model) =============== #
    else:
        metric = metrics_to_plot[0]
        for idx, row in filtered_df.iterrows():
            fig.add_trace(go.Bar(
                x=[row["Model"]],
                y=[row[metric]],
                name=row["Model"],
                marker_color=model_colors[idx % len(model_colors)],
                text=f"{row[metric]:.4f}",
                textposition='auto'
            ))

    fig.update_layout(
        barmode="group",
        title="Performance Metrics Comparison",
        xaxis_title="Model",
        yaxis_title="Score",
        legend_title="Metric" if metric_option == "All" else "Model",
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )

    st.plotly_chart(fig, use_container_width=True)

    # Dynamically update best model summary
    if not df_eval.empty:
        best_metric = "ROC AUC" if metric_option == "All" else metric_option
        top_model_row = df_eval.loc[df_eval[best_metric].idxmax()]
        best_model_name = top_model_row["Model"]
        best_score = top_model_row[best_metric]

        st.markdown(
            f"🔍 Based on the **{best_metric}**, the best model is **{best_model_name}** with a score of **{best_score:.4f}**."
        )
    # ---------- ROC AUC Curve Plot ---------- #
    st.markdown("### 🧪 ROC Curve Comparison")

    roc_view_option = st.radio(
        "Select ROC view mode:", 
        ["All Models", "Individual Model"], 
        horizontal=True, 
        key="roc_view"
    )

    if roc_view_option == "All Models":
        selected_roc_models = list(model_info.keys())
    else:
        selected_roc_models = st.multiselect(
            "Select model(s) for ROC curve:",
            options=list(model_info.keys()),
            default=list(model_info.keys())[0:1],
            key="roc_select"
        )

    fig_auc = go.Figure()

    # Custom line styles
    line_styles = {
        "LightGBM with Random Search CV": dict(color='skyblue', width=3),
        "CatBoost with Random Search CV": dict(color='deepskyblue', dash='dot', width=3),
        "LightGBM with Grid Search CV": dict(color='lightgreen', dash='dash', width=2),
        "XGBoost with Grid Search CV": dict(color='salmon', width=2),
        "CatBoost Base Model": dict(color='palegreen', dash='dashdot', width=2)
    }

    for model_name in selected_roc_models:
        file_path = model_info[model_name]
        try:
            metrics = joblib.load(file_path)
            fpr = metrics.get("roc_curve", {}).get("fpr") or metrics.get("fpr")
            tpr = metrics.get("roc_curve", {}).get("tpr") or metrics.get("tpr")
            auc = metrics.get("roc_auc", None)

            if fpr is not None and tpr is not None:
                style = line_styles.get(model_name, {})
                fig_auc.add_trace(go.Scatter(
                    x=fpr,
                    y=tpr,
                    mode='lines',
                    name=f"{model_name} (AUC = {auc:.4f})" if auc else model_name,
                    line=style
                ))
            else:
                st.warning(f"⚠️ ROC data missing for {model_name} — no fpr and tpr found.")
        except Exception as e:
            st.error(f"❌ Failed to load ROC for {model_name}: {e}")

    # Diagonal reference line
    fig_auc.add_trace(go.Scatter(
        x=[0, 1],
        y=[0, 1],
        mode='lines',
        name='Random Guess',
        line=dict(color='gray', dash='dash'),
        showlegend=True
    ))

    # Update layout
    fig_auc.update_layout(
        title=dict(
            text="ROC Curve Comparison",
            x=0.25,
            font=dict(size=20)
        ),
        xaxis_title="False Positive Rate",
        yaxis_title="True Positive Rate",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        legend=dict(
            bgcolor='rgba(0,0,0,0.1)',
            bordercolor='gray',
            borderwidth=1
        ),
        height=500
    )

    st.plotly_chart(fig_auc, use_container_width=True)