# utils/ai_helpers.py
import re
from utils.gemini_intent import model
from utils.mappings import encoding_maps

# ---------------------- Fallback Query ---------------------- #
def run_fallback_query(user_query, df):
    fallback_prompt = f"""
You are a Python pandas expert.

A user will ask a question about a DataFrame named `df` that contains numerically encoded medical data.

👉 Return ONLY a single-line valid Python expression using `df[...]`.
❌ Do NOT include backticks, markdown, explanations, or code blocks.

🧠 Use ONLY the exact column names and values listed below. DO NOT guess based on the wording.

Column Mappings:
- gender: 0 = Female, 1 = Male  
- readmitted: 0 = Not Readmitted, 1 = Readmitted  
- race: 0 = Caucasian, 1 = AfricanAmerican, 2 = Other, 3 = Asian, 4 = Hispanic  
- change: 0 = No, 1 = Yes  
- diabetesMed: 0 = No, 1 = Yes  
- age: 0 = 0–10, 1 = 10–20, ..., 9 = 90–100  
- diag_1: 1 = Circulatory, ..., 9 = Other  
- admission_source_id: 0 = Referral, ..., 4 = Readmission/Home Health  
- admission_type_id: 0 = Emergency, ..., 4 = Trauma Center  
- discharge_disposition_id: 0 = Home, ..., 5 = Still Patient

User query: {user_query}
    """

    response = model.generate_content(fallback_prompt)
    raw_code = response.text.strip()
    cleaned_code = re.sub(r"```[\w]*\n", "", raw_code).replace("```", "").strip()
    return cleaned_code

# ---------------------- Intent-Based Explanation ---------------------- #
def respond_to_query(intent, df, correlation_matrix, feature_importances, model_scores):
    if intent == "get_top_correlation":
        top_corr = correlation_matrix["readmitted"].drop("readmitted").abs().sort_values(ascending=False).head(1)
        feature = top_corr.index[0]
        value = correlation_matrix["readmitted"][feature]
        return model.generate_content(
            f"The feature most correlated with readmission is {feature} (correlation: {value:.3f}). "
            "Explain this in simple terms."
        ).text

    elif intent == "get_negative_correlation":
        top_neg = correlation_matrix["readmitted"].drop("readmitted").sort_values().head(1)
        feature = top_neg.index[0]
        value = top_neg.iloc[0]
        return model.generate_content(
            f"The feature most negatively correlated with readmission is {feature} (correlation: {value:.3f}). "
            "Explain why this matters."
        ).text

    elif intent == "get_best_model":
        best_model = max(model_scores.items(), key=lambda x: x[1]["auc"])[0]
        auc = model_scores[best_model]["auc"]
        accuracy = model_scores[best_model]["accuracy"]
        return model.generate_content(
            f"The best performing model is {best_model} with an AUC of {auc:.4f} and accuracy of {accuracy:.4f}. "
            "Explain what this means for model performance in the context of hospital readmissions."
        ).text
    
    elif intent == "get_model_ranking":
        sorted_models = sorted(model_scores.items(), key=lambda x: x[1]["auc"], reverse=True)
        ranking_list = [
            f"{i+1}. {name} — Accuracy: {score['accuracy']:.4f}, AUC: {score['auc']:.4f}"
            for i, (name, score) in enumerate(sorted_models)
        ]
        ranking_text = "\n".join(ranking_list)

        # Generate Gemini's explanation first
        explanation_prompt = f"""
We tested five different machine learning models to predict hospital readmission among diabetic patients.

They were ranked based on AUC (Area Under the Curve), a reliable metric for binary classification. 
Accuracy scores were close across models, but AUC gives a clearer picture of performance in imbalanced datasets.

The top model was Gradient Boost (Grid Search) with an AUC of 0.8692 and accuracy of 0.8099, 
followed closely by LightGBM and CatBoost. Hyperparameter tuning (grid vs. random search) made minimal difference.

Explain this result in simple ML terms.
"""
        explanation = model.generate_content(explanation_prompt).text.strip()

        # Combine explanation and ranked list
        return f"{explanation}\n\n**📊 Top 5 Model Rankings:**\n" + "\n".join(ranking_list)

    elif intent == "get_top_features":
        top_feats = sorted(feature_importances.items(), key=lambda x: x[1], reverse=True)
        summary = ", ".join([f"{feat} ({imp:.2f})" for feat, imp in top_feats[:5]])
        return model.generate_content(
            f"The top features contributing to readmission prediction are: {summary}. "
            "Explain what this means."
        ).text

    elif intent == "get_readmission_rate":
        rate = df["readmitted"].mean()
        return model.generate_content(
            f"The overall readmission rate in the dataset is {rate:.2%}. "
            "Explain this insight to the user."
        ).text

    else:
        return "🤖 I'm not sure how to answer that yet. Try rephrasing your question."

# ---------------------- Decode for Display ---------------------- #
def decode_dataframe(df_result, mappings):
    for col in df_result.columns:
        if col in mappings:
            df_result[col] = df_result[col].map(mappings[col])
    return df_result

# ---------------------- Gemini Explanation for Model Metrics ---------------------- #
def explain_model_metrics_with_gemini(accuracy, roc_auc, report):
    try:
        summary = f"""
We evaluated a Gradient Boosting model used to predict hospital readmissions among diabetic patients.

Here are the key metrics:
- Accuracy: {accuracy:.3f}
- ROC AUC Score: {roc_auc:.3f}
- Class 0 (Not Readmitted): Precision={report['0']['precision']:.3f}, Recall={report['0']['recall']:.3f}, F1-Score={report['0']['f1-score']:.3f}
- Class 1 (Readmitted): Precision={report['1']['precision']:.3f}, Recall={report['1']['recall']:.3f}, F1-Score={report['1']['f1-score']:.3f}

Explain these results in simple terms that a healthcare professional can understand.
"""
        response = model.generate_content(summary)
        return response.text
    except Exception as e:
        return f"❌ Gemini could not generate explanation: {e}"
