# pages/feature_explore.py
import streamlit as st # type: ignore
import pandas as pd
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder # type: ignore

def render():
    st.subheader("📊 Explore Dataset Features")

   
    # Load dataset
    df = pd.read_csv("data/FYP_Cleaned2.csv")

# ========== Reverse Encoding ==========
    # Race
    race_map = {0: 'Caucasian', 1: 'AfricanAmerican', 2: 'Other', 3: 'Asian', 4: 'Hispanic'}
    df['race'] = df['race'].map(race_map)

    # Gender
    gender_map = {0: 'Female', 1: 'Male'}
    df['gender'] = df['gender'].map(gender_map)

    # Readmitted
    readmit_map = {0: 'Not Readmitted', 1: 'Readmitted'}
    df['readmitted'] = df['readmitted'].map(readmit_map)

    # Change
    df['change'] = df['change'].map({0: 'No', 1: 'Ch'})

    # DiabetesMed
    df['diabetesMed'] = df['diabetesMed'].map({0: 'No', 1: 'Yes'})

    # Admission Source
    admission_source_map = {
        0: 'Referral',
        1: 'Transfer from Healthcare Facility',
        2: 'Emergency',
        3: 'Birth/Neonatal',
        4: 'Readmission/Home Health'
    }
    df['admission_source_id'] = df['admission_source_id'].map(admission_source_map)

    # Admission Type
    admission_type_map = {
        0: 'Emergency',
        1: 'Urgent',
        2: 'Elective',
        3: 'Newborn',
        4: 'Trauma Center'
    }
    df['admission_type_id'] = df['admission_type_id'].map(admission_type_map)

    # Discharge Disposition
    discharge_map = {
        0: 'Home Discharge',
        1: 'Transferred',
        2: 'Expired',
        3: 'Hospice',
        4: 'Left AMA',
        5: 'Still Patient'
    }
    df['discharge_disposition_id'] = df['discharge_disposition_id'].map(discharge_map)

    # A1Cresult
    a1c_map = {0: 'None', 1: 'Norm', 2: '>7', 3: '>8'}
    df['A1Cresult'] = df['A1Cresult'].map(a1c_map)

    # Max Glucose Serum
    glu_map = {0: 'None', 1: 'Norm', 2: '>200', 3: '>300'}
    df['max_glu_serum'] = df['max_glu_serum'].map(glu_map)

    # Diagnosis (optional)
    diag_map = {
        1: 'Circulatory', 2: 'Respiratory', 3: 'Digestive', 4: 'Diabetes',
        5: 'Injury', 6: 'Musculoskeletal', 7: 'Genitourinary',
        8: 'Neoplasms', 9: 'Other'
    }
    df['diag_1'] = df['diag_1'].map(diag_map)

    # Navigation within page
    sub_page = st.selectbox(
        "📂 Select an analysis section:",
        [
            "📘 Feature Reference Guide",
            "Summary Statistics",
            "Univariate Features",
            "Bivariate Features",
            "Correlation Analysis"
        ])

    categorical_cols = [
    'race', 'gender', 'readmitted', 'diabetesMed', 'change',
    'admission_source_id', 'admission_type_id', 'discharge_disposition_id',
    'A1Cresult', 'max_glu_serum', 'diag_1'
    ]
    numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    for col in categorical_cols:
        if col in numerical_cols:
            numerical_cols.remove(col)

   # -------------------- Feature Reference Guide --------------------
    if sub_page == "📘 Feature Reference Guide":
        st.title("📘 Hospital Dataset Feature Reference Guide")

        st.markdown("""
        This guide provides a comprehensive breakdown of all features used in the hospital readmission prediction model.  
        Features are grouped into categories to help you understand their role in the system.
        """)

        # ==== Display Helper ====
        def display_feature_section(title, features_dict):
            with st.expander(title, expanded=True):
                col1, col2 = st.columns(2)
                items = list(features_dict.items())

                for i, (_, desc) in enumerate(items):
                    html = f"<div style='margin-bottom: 6px;'>• {desc}</div>"
                    if i % 2 == 0:
                        col1.markdown(html, unsafe_allow_html=True)
                    else:
                        col2.markdown(html, unsafe_allow_html=True)

        # ==== Feature Groups ==== #
        demographic_features = {
            "race": "🧬 <strong>race</strong> – Patient’s race (e.g., Caucasian, AfricanAmerican).",
            "gender": "🚻 <strong>gender</strong> – Biological sex of the patient.",
            "age": "🎂 <strong>age</strong> – Age group of the patient (e.g., 60–70)."
        }

        admission_features = {
            "admission_type_id": "🛬 <strong>admission_type_id</strong> – Type of hospital admission.",
            "admission_source_id": "📥 <strong>admission_source_id</strong> – Source of admission.",
            "discharge_disposition_id": "📤 <strong>discharge_disposition_id</strong> – Discharge destination.",
            "time_in_hospital": "⏱ <strong>time_in_hospital</strong> – Duration of hospital stay (days)."
        }

        visit_features = {
            "number_outpatient": "🏥 <strong>number_outpatient</strong> – Outpatient visits in past year.",
            "number_emergency": "🚑 <strong>number_emergency</strong> – Emergency visits in past year.",
            "number_inpatient": "🛌 <strong>number_inpatient</strong> – Inpatient visits in past year.",
            "number_of_visits": "🔢 <strong>number_of_visits</strong> – Total of all visit types."
        }

        diagnostic_features = {
            "diag_1": "📋 <strong>diag_1</strong> – Primary diagnosis code.",
            "number_diagnoses": "📈 <strong>number_diagnoses</strong> – Number of diagnosis codes.",
            "max_glu_serum": "🧪 <strong>max_glu_serum</strong> – Glucose test result flag.",
            "A1Cresult": "🩸 <strong>A1Cresult</strong> – A1C blood sugar test result."
        }

        medication_flags = {
            "diabetesMed": "💊 <strong>diabetesMed</strong> – Whether diabetes medication was prescribed.",
            "change": "🔁 <strong>change</strong> – Whether meds were changed during stay.",
            "numchange": "🔢 <strong>numchange</strong> – Number of medication changes."
        }

        outcome_features = {
            "readmitted": "🎯 <strong>readmitted</strong> – Whether the patient was readmitted (target)."
        }

        drug_features = {
            "metformin": "💊 <strong>metformin</strong>, common oral diabetes medication.",
            "glipizide": "💊 <strong>glipizide</strong>, stimulates insulin production.",
            "rosiglitazone": "💊 <strong>rosiglitazone</strong>, improves insulin sensitivity.",
            "acarbose": "💊 <strong>acarbose</strong>, slows carb absorption.",
            "tolbutamide": "💊 <strong>tolbutamide</strong>, sulfonylurea class.",
            "nateglinide": "💊 <strong>nateglinide</strong>, stimulates pancreas.",
            "glimepiride": "💊 <strong>glimepiride</strong>, enhances insulin release.",
            "tolazamide": "💊 <strong>tolazamide</strong>, less common today.",
            "glyburide-metformin": "💊 <strong>glyburide-metformin</strong>, combination therapy.",
            "glimepiride-pioglitazone": "💊 <strong>glimepiride-pioglitazone</strong>, dual-action therapy.",
            "metformin-pioglitazone": "💊 <strong>metformin-pioglitazone</strong>, dual therapy.",
            "insulin": "💉 <strong>insulin</strong>, injected diabetes medication.",
            "glyburide": "💊 <strong>glyburide</strong>, oral antidiabetic.",
            "pioglitazone": "💊 <strong>pioglitazone</strong>, reduces insulin resistance.",
            "repaglinide": "💊 <strong>repaglinide</strong>, fast-acting insulin releaser.",
            "chlorpropamide": "💊 <strong>chlorpropamide</strong>, older sulfonylurea.",
            "troglitazone": "💊 <strong>troglitazone</strong>, withdrawn drug.",
            "acetohexamide": "💊 <strong>acetohexamide</strong>, first-gen sulfonylurea.",
            "glipizide-metformin": "💊 <strong>glipizide-metformin</strong>, combo therapy.",
            "metformin-rosiglitazone": "💊 <strong>metformin-rosiglitazone</strong>, combination therapy."
        }

        # ==== Render All Sections ====
        display_feature_section("🧍 Demographic Features", demographic_features)
        display_feature_section("🏥 Admission Details", admission_features)
        display_feature_section("📅 Visit History", visit_features)
        display_feature_section("🧪 Diagnostic Features", diagnostic_features)
        display_feature_section("🔁 Medication Status", medication_flags)
        display_feature_section("💊 Medication Types", drug_features)
        display_feature_section("🎯 Target Variable", outcome_features)

        st.info("💡 Tip: Understanding each feature improves model interpretation and builds trust.")

    # -------------------- Summary Stats --------------------
    if sub_page == "Summary Statistics":
        st.markdown("## 🧠 Summary Statistics by Feature Type")
        st.markdown("This section summarizes both categorical and numerical attributes in your dataset.")

        st.markdown("---")

        # === Categorical Summary ===
        st.markdown("### 🧩 Categorical Feature Summary")
        st.caption("🔠 This table shows mode frequency, unique values, and category distributions for categorical features.")

        cat_summary = (
            df[categorical_cols]
            .describe(include="all")
            .transpose()
            .round(2)
            .reset_index()
            .rename(columns={"index": "Feature"})
        )
        cat_summary = cat_summary[["Feature", "count", "unique", "top", "freq"]]

        # Setup AgGrid for categorical summary
        gb_cat = GridOptionsBuilder.from_dataframe(cat_summary)
        gb_cat.configure_default_column(filter=True, sortable=True, resizable=True)
        gb_cat.configure_pagination(paginationAutoPageSize=True)
        gb_cat.configure_grid_options(domLayout='normal', rowHeight=35)
        grid_cat = gb_cat.build()

        st.markdown("<div style='margin-top: -10px;'></div>", unsafe_allow_html=True)
        AgGrid(cat_summary, gridOptions=grid_cat, theme="balham-dark", height=250, fit_columns_on_grid_load=True)

        st.markdown("---")

        # === Numerical Summary ===
        st.markdown("### 📐 Numerical Feature Summary")
        st.caption("📊 This table summarizes key statistics such as mean, standard deviation, and range for numerical features.")

        num_summary = (
            df[numerical_cols]
            .describe()
            .transpose()
            .round(2)
            .reset_index()
            .rename(columns={"index": "Feature"})
        )
        num_summary = num_summary[["Feature", "count", "mean", "std", "min", "25%", "50%", "75%", "max"]]

        # Setup AgGrid for numerical summary
        gb_num = GridOptionsBuilder.from_dataframe(num_summary)
        gb_num.configure_default_column(filter=True, sortable=True, resizable=True)
        gb_num.configure_pagination(paginationAutoPageSize=True)
        gb_num.configure_grid_options(domLayout='normal', rowHeight=35)
        grid_num = gb_num.build()

        AgGrid(num_summary, gridOptions=grid_num, theme="balham-dark", height=320, fit_columns_on_grid_load=True)

        st.markdown("---")
    # -------------------- Univariate --------------------
    elif sub_page == "Univariate Features":
        selected_col = st.selectbox("Choose a feature to explore:", df.columns)
        st.markdown("---")

        if selected_col in categorical_cols:
            st.write(f"### 📊 Distribution of {selected_col}")
            fig = px.histogram(df, x=selected_col, color_discrete_sequence=['#636EFA'])
            fig.update_layout(title=f"Distribution of {selected_col}")
            st.plotly_chart(fig, use_container_width=True)

            st.write("### 📋 Summary Statistics")
            value_counts = df[selected_col].value_counts()
            summary_df = pd.DataFrame({"Value": value_counts.index, "Count": value_counts.values})
            st.table(summary_df)

        elif selected_col in numerical_cols:
            st.write(f"### 📈 Histogram of {selected_col}")
            fig = px.histogram(df, x=selected_col, nbins=30, marginal="box", color_discrete_sequence=['#00CC96'])
            st.plotly_chart(fig, use_container_width=True)

            st.write("### 📉 Boxplot")
            fig2 = px.box(df, y=selected_col, color_discrete_sequence=['#EF553B'])
            st.plotly_chart(fig2, use_container_width=True)

            st.write("### 📋 Summary Statistics")
            stats = df[selected_col].describe()
            stats_df = pd.DataFrame({"Statistic": stats.index, "Value": stats.values.round(2)})
            stats_df.loc[len(stats_df)] = ["median", round(df[selected_col].median(), 2)]
            st.table(stats_df)

    # -------------------- Bivariate --------------------
    elif sub_page == "Bivariate Features":
        st.write("### Feature Relationship with Readmission")
        bivar_col = st.selectbox("Select a feature to compare with Readmitted:", [col for col in df.columns if col != 'readmitted'])

        if bivar_col in categorical_cols:
            ct = pd.crosstab(df[bivar_col], df['readmitted'], normalize='index').reset_index()
            ct_melted = ct.melt(id_vars=bivar_col, var_name='Readmitted', value_name='Proportion')

            fig = px.bar(ct_melted, x=bivar_col, y='Proportion', color='Readmitted', barmode='stack')
            fig.update_layout(title=f"{bivar_col} vs Readmitted (Proportions)")
            st.plotly_chart(fig, use_container_width=True)

        elif bivar_col in numerical_cols:
            fig = px.box(df, x='readmitted', y=bivar_col, color='readmitted')
            fig.update_layout(title=f"{bivar_col} by Readmission Status")
            st.plotly_chart(fig, use_container_width=True)

    # -------------------- Correlation Analysis --------------------
    elif sub_page == "Correlation Analysis":
        st.write("### 🔗 Correlation Heatmap of Numerical Features")

        # Re-encode readmitted for correlation
        corr_df = df.copy()
        corr_df['readmitted'] = corr_df['readmitted'].map({'Not Readmitted': 0, 'Readmitted': 1})

        # Compute correlation
        corr_matrix = corr_df[numerical_cols + ['readmitted']].corr().round(2)

        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            color_continuous_scale='RdBu_r',
            title="Correlation Matrix (Numerical Features + Readmitted)",
            aspect='auto'
        )
        st.plotly_chart(fig, use_container_width=True)

        st.caption("🔍 Values close to +1 or -1 indicate strong correlation. Watch for multicollinearity.")

         # -------- Top Correlated with Readmitted --------
        st.markdown("---")
        st.subheader("📌 Top Features Correlated with Readmission")

        top_corr = corr_matrix['readmitted'].drop('readmitted').sort_values(key=abs, ascending=False)
        top_corr_df = top_corr.reset_index().rename(columns={'index': 'Feature', 'readmitted': 'Correlation'})

        st.table(top_corr_df.head(10))