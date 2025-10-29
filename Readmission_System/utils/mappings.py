# utils/mappings.py

encoding_maps = {
    "gender": {0: "Female", 1: "Male"},
    "readmitted": {0: "Not Readmitted", 1: "Readmitted"},
    "race": {
        0: "Caucasian", 1: "AfricanAmerican", 2: "Other",
        3: "Asian", 4: "Hispanic"
    },
    "change": {0: "No", 1: "Yes"},
    "diabetesMed": {0: "No", 1: "Yes"},
    "age": {
        0: "0–10", 1: "10–20", 2: "20–30", 3: "30–40", 4: "40–50",
        5: "50–60", 6: "60–70", 7: "70–80", 8: "80–90", 9: "90–100"
    },
    "diag_1": {
        1: "Circulatory", 2: "Respiratory", 3: "Digestive", 4: "Diabetes",
        5: "Injury", 6: "Musculoskeletal", 7: "Genitourinary", 8: "Neoplasms", 9: "Other"
    },
    "admission_source_id": {
        0: "Referral",
        1: "Transfer from Healthcare Facility",
        2: "Emergency",
        3: "Birth/Neonatal",
        4: "Readmission/Home Health"
    },
    "admission_type_id": {
        0: "Emergency",
        1: "Urgent",
        2: "Elective",
        3: "Newborn",
        4: "Trauma Center"
    },
    "discharge_disposition_id": {
        0: "Home Discharge",
        1: "Transferred to Another Facility",
        2: "Expired",
        3: "Hospice",
        4: "Left AMA",
        5: "Still Patient"
    }
}
