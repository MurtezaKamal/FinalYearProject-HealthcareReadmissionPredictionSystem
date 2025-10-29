# pages/dashboard.py
import streamlit as st  # type: ignore
import pandas as pd
import plotly.express as px

def render():
    st.subheader("📊 Interactive Dashboard")

    # Load dataset
    df = pd.read_csv("data/FYP_Cleaned2.csv")

    # Mappings
    readmit_map = {0: "Not Readmitted", 1: "Readmitted"}
    gender_map = {0: 'Female', 1: 'Male'}
    race_map = {0: 'Caucasian', 1: 'AfricanAmerican', 2: 'Other', 3: 'Asian', 4: 'Hispanic'}
    adm_type_map = {0: "Emergency", 1: "Urgent", 2: "Elective", 3: "Newborn", 4: "Trauma"}
    discharge_map = {
        0: "Home", 1: "Transfer", 2: "Expired", 3: "Hospice", 4: "Left AMA", 5: "Still Patient"
    }
    admission_source_map = {
    0: "Referral",
    1: "Transfer from Healthcare Facility",
    2: "Emergency",
    3: "Birth/Neonatal",
    4: "Readmission/Home Health"
    }

    df["readmitted_display"] = df["readmitted"].map(readmit_map)
    df["gender"] = df["gender"].map(gender_map)
    df["race"] = df["race"].map(race_map)
    df["admission_type_id"] = df["admission_type_id"].map(adm_type_map)
    df["discharge_disposition_id"] = df["discharge_disposition_id"].map(discharge_map)
    df["admission_source_id"] = df["admission_source_id"].map(admission_source_map)

    # Sidebar filters (Dynamic)
    st.sidebar.write("### 🧰 Filters")

    #Let user pick which filters to apply
    available_filters = [
        "Readmitted","Gender", "Race", "Age", "Admission Type",
        "Discharge Disposition", "Admission Source ID",
        "Diabetes Medication", "Medication Change",
        "Number of Visits", "Time in Hospital"
    ]
    selected_filters = st.sidebar.multiselect("🧩 Choose filters to apply:", available_filters, default=["Gender", "Race", "Age"])

    #Conditionally display filter widgets
    if "Readmitted" in selected_filters:
        readmit_options = df["readmitted_display"].dropna().unique().tolist()
        selected_readmit = st.sidebar.multiselect("Readmitted Status", options=readmit_options, default=readmit_options)
    else:
        selected_readmit = df["readmitted_display"].unique().tolist()
    
    if "Gender" in selected_filters:
        gender_options = df["gender"].dropna().unique().tolist()
        selected_gender = st.sidebar.multiselect("Gender", options=gender_options, default=gender_options)
    else:
        selected_gender = df["gender"].unique().tolist()

    if "Race" in selected_filters:
        race_options = df["race"].dropna().unique().tolist()
        selected_race = st.sidebar.multiselect("Race", options=race_options, default=race_options)
    else:
        selected_race = df["race"].unique().tolist()

    if "Age" in selected_filters:
        age_min, age_max = int(df["age"].min()), int(df["age"].max())
        selected_age = st.sidebar.slider("Age", age_min, age_max, (age_min, age_max))
    else:
        selected_age = (int(df["age"].min()), int(df["age"].max()))

    if "Admission Type" in selected_filters:
        adm_type_options = df["admission_type_id"].dropna().unique().tolist()
        selected_adm_types = st.sidebar.multiselect("Admission Type", options=adm_type_options, default=adm_type_options)
    else:
        selected_adm_types = df["admission_type_id"].unique().tolist()

    if "Discharge Disposition" in selected_filters:
        discharge_options = df["discharge_disposition_id"].dropna().unique().tolist()
        selected_discharges = st.sidebar.multiselect("Discharge Disposition", options=discharge_options, default=discharge_options)
    else:
        selected_discharges = df["discharge_disposition_id"].unique().tolist()

    if "Admission Source ID" in selected_filters:
        adm_source_options = df["admission_source_id"].dropna().unique().tolist()
        selected_adm_sources = st.sidebar.multiselect("Admission Source", options=adm_source_options, default=adm_source_options)
    else:
        selected_adm_sources = df["admission_source_id"].unique().tolist()

    if "Diabetes Medication" in selected_filters:
        diabetes_med_options = df["diabetesMed"].dropna().unique().tolist()
        selected_diabetes_med = st.sidebar.multiselect("Diabetes Medication", options=diabetes_med_options, default=diabetes_med_options)
    else:
        selected_diabetes_med = df["diabetesMed"].unique().tolist()

    if "Medication Change" in selected_filters:
        change_options = df["change"].dropna().unique().tolist()
        selected_change = st.sidebar.multiselect("Change of Medication", options=change_options, default=change_options)
    else:
        selected_change = df["change"].unique().tolist()

    if "Number of Visits" in selected_filters:
        visits_min, visits_max = int(df["number_of_visits"].min()), int(df["number_of_visits"].max())
        selected_visits = st.sidebar.slider("Number of Visits", visits_min, visits_max, (visits_min, visits_max))
    else:
        selected_visits = (int(df["number_of_visits"].min()), int(df["number_of_visits"].max()))

    if "Time in Hospital" in selected_filters:
        time_min, time_max = int(df["time_in_hospital"].min()), int(df["time_in_hospital"].max())
        selected_time = st.sidebar.slider("Time in Hospital", time_min, time_max, (time_min, time_max))
    else:
        selected_time = (int(df["time_in_hospital"].min()), int(df["time_in_hospital"].max()))

    filtered_df = df[
    (df["readmitted_display"].isin(selected_readmit))  &
    (df["gender"].isin(selected_gender)) &
    (df["race"].isin(selected_race)) &
    (df["age"].between(selected_age[0], selected_age[1])) &
    (df["admission_type_id"].isin(selected_adm_types)) &
    (df["discharge_disposition_id"].isin(selected_discharges)) &
    (df["admission_source_id"].isin(selected_adm_sources)) &
    (df["diabetesMed"].isin(selected_diabetes_med)) &
    (df["change"].isin(selected_change)) &
    (df["number_of_visits"].between(selected_visits[0], selected_visits[1])) &
    (df["time_in_hospital"].between(selected_time[0], selected_time[1]))
    ]   

    # If no data after filtering
    if filtered_df.empty:
        st.warning("⚠️ No data available for the selected filter combination. Please adjust your filters.")
        return

    # ----------------------------
    # Top Summary Metrics Section
    # ----------------------------
    st.write("### 📌 Key Statistics Summary")

    col1, col2 = st.columns(2)
    with col1:
        count = filtered_df.shape[0]
        st.metric(label="🧍 Matching Patients", value=f"{count:,}")
    with col2:
        rate = filtered_df["readmitted"].mean()
        st.metric(label="🔁 Readmission Rate", value=f"{rate:.2%}")

    st.markdown("---")

    # ----------------------------
    # Graphs & Visual Insights
    # ----------------------------

    # Readmission Overview
    st.write("### 🔄 Readmission Distribution")
    readmit_counts = filtered_df["readmitted"].value_counts().sort_index()
    st.plotly_chart(
        px.bar(
            x=readmit_counts.index.map({0: "No", 1: "Yes"}),
            y=readmit_counts.values,
            labels={"x": "Readmitted", "y": "Count"},
            title="Readmission Count",
            color=readmit_counts.index.map({0: "No", 1: "Yes"}),
            color_discrete_sequence=["#1f77b4", "#ff7f0e"]
        )
    )
    # Key Feature Distributions
    st.write("### 📈 Key Feature Distributions")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(px.histogram(
            filtered_df, x="number_of_visits", nbins=30, title="Number of Visits",
            color_discrete_sequence=["#6a5acd"]
        ))
    with col2:
        st.plotly_chart(px.histogram(
            filtered_df, x="time_in_hospital", nbins=15, title="Time in Hospital",
            color_discrete_sequence=["#20b2aa"]
        ))

    st.plotly_chart(px.histogram(
        filtered_df, x="number_diagnoses", nbins=15, title="Number of Diagnoses",
        color_discrete_sequence=["#ffa07a"]
    ))

    # Clinical & Utilization Metrics
    st.write("### 🏥 Clinical and Utilization Metrics")
    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(px.histogram(
            filtered_df, x="num_lab_procedures", nbins=20, title="Lab Procedures",
            color_discrete_sequence=["#8a2be2"]
        ))

    with col4:
        st.plotly_chart(px.histogram(
            filtered_df, x="num_medications", nbins=20, title="Medications",
            color_discrete_sequence=["#2ca02c"]
        ))

    st.plotly_chart(px.histogram(
        filtered_df, x="numchange", nbins=10, title="Medication Changes",
        color_discrete_sequence=["#d62728"]
    ))
    # Admission & Discharge
    st.write("### 🏷️ Admission & Discharge Patterns")

    adm_df = filtered_df["admission_type_id"].value_counts().reset_index()
    adm_df.columns = ["Admission Type", "Count"]
    st.plotly_chart(px.bar(
        adm_df, x="Admission Type", y="Count", title="Admission Type Distribution",
        color="Admission Type", color_discrete_sequence=px.colors.qualitative.Pastel
    ))

    dis_df = filtered_df["discharge_disposition_id"].value_counts().reset_index()
    dis_df.columns = ["Discharge Disposition", "Count"]
    st.plotly_chart(px.bar(
        dis_df, x="Discharge Disposition", y="Count", title="Discharge Disposition Distribution",
        color="Discharge Disposition", color_discrete_sequence=px.colors.qualitative.Set3
    ))

    # Diabetes Medication Use
    st.write("### 💊 Diabetes Medication Usage")
    color_map = {
        "metformin": "#9b59b6",
        "insulin": "#f39c12",
        "glipizide": "#16a085"
    }
    for med in ["metformin", "insulin", "glipizide"]:
        if med in filtered_df.columns:
            med_counts = filtered_df[med].value_counts().sort_index()
            labels = med_counts.index.map({0: "No", 1: "Yes"})
            usage_df = pd.DataFrame({
                "Usage": labels,
                "Count": med_counts.values
            })
            st.plotly_chart(px.bar(
                usage_df, x="Usage", y="Count", title=f"{med.capitalize()} Usage",
                color="Usage",
                color_discrete_sequence=[color_map[med], "#95a5a6"]
            ))

