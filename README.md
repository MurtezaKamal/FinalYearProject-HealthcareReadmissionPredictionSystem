# 🏥 Healthcare Readmission System

**Final Year Project – Asia Pacific University (APU)**  
**Author:** Mohammed Murteza Kamal  
**Program:** BSc (Hons) in Computer Science with a Specialism in Data Analytics  

---

## 📘 Project Overview
Hospital readmissions are a critical issue for both healthcare providers and patients, particularly among diabetic individuals who face complex care requirements.  
This project presents a **Healthcare Readmission System**, a predictive machine learning solution designed to analyze patient data and forecast the likelihood of hospital readmission.  

By combining structured medical data with interactive analytics through **Streamlit**, the system provides valuable insights that can support hospitals in identifying at-risk patients, optimizing treatment strategies, and improving healthcare outcomes.

Dataset used - https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008
---

## 🎯 Objectives
- Analyze hospital readmission patterns among diabetic patients.
- Preprocess and clean hospital datasets for reliable model training.
- Identify the most influential factors contributing to readmission.
- Develop and evaluate machine learning models for prediction accuracy.
- Deploy the best-performing model through an interactive **Streamlit** web interface.

---

## ⚙️ System Architecture
The system is divided into two key components:

### 🧩 1. Model Development (Jupyter Notebooks)
- Data preprocessing, cleaning, and feature engineering.  
- Exploratory data analysis (EDA) to identify trends and correlations.  
- Training and evaluation of various machine learning models (e.g., CatBoost, LightGBM).  
- Selection of the top-performing model based on AUC, F1-score, and accuracy metrics.
- Further Hypertuning of the top perfomring models to test for higher performance. 

### 💻 2. Streamlit Application
- User-friendly interface for both individual and batch predictions.  
- Real-time classification of diabetic patients based on input data.  
- Visual representation of results through charts and confusion matrices.  
- Downloadable reports and sample CSV for easy testing.

---

## 🧠 Methodology (CRISP-DM)
1. **Data Acquisition:** Hospital readmission dataset containing patient demographics, diagnoses, treatments, and admission details.  
2. **Data Preprocessing:** Handling of missing values, encoding categorical variables, and scaling numerical features.  
3. **Feature Selection:** Identification of top 10 predictive features for model optimization.  
4. **Model Training:** Comparison between multiple algorithms (LightGBM, Decision Tree, CatBoost, ANN's etc.).  
5. **Evaluation:** Models assessed using accuracy, precision, recall, F1-score, and AUC.  
6. **Deployment:** Integration of the best model (LightGBM) into a Streamlit web app.

---

## 🧩 Technologies Used
| Category | Tools / Libraries |
|-----------|-------------------|
| **Programming Language** | Python |
| **Framework** | Streamlit |
| **Data Processing** | Pandas, NumPy |
| **Modeling** | Scikit-learn, LightGBM, CatBoost, XGBoost, Gradient Boosting, Simpler ANN |
| **Hypertuning Methods** | RandomizedSearchCV, GridSearchCV |
| **Visualization** | Plotly, Matplotlib, Seaborn |
| **Environment** | Jupyter Notebook, VS Code |

---

## 📊 Results and Evaluation
- **Best Model Pre-Tuning:** CatBoost Model
- **Best Model After-Tuning:** LightGBM Model (RandomizedSearchCV)
- **Performance:** High accuracy (0.8098) and High AUC (0.8692)
