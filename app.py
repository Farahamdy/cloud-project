import gradio as gr
import joblib
import pandas as pd
import numpy as np

# Load trained model (preprocessor + classifier)
model = joblib.load("privacy_income_model.pkl")

# Dropdown options
workclass_opts = ["Private", "Self-emp-not-inc", "Self-emp-inc", "Federal-gov",
                  "Local-gov", "State-gov", "Without-pay", "Never-worked"]

education_opts = ["Bachelors", "Some-college", "11th", "HS-grad", "Prof-school",
                  "Assoc-acdm", "Assoc-voc", "9th", "7th-8th", "12th", "Masters",
                  "1st-4th", "10th", "Doctorate", "5th-6th", "Preschool"]

marital_opts = ["Married-civ-spouse", "Divorced", "Never-married", "Separated",
                "Widowed", "Married-spouse-absent", "Married-AF-spouse"]

occupation_opts = ["Tech-support", "Craft-repair", "Other-service", "Sales",
                    "Exec-managerial", "Prof-specialty", "Handlers-cleaners",
                    "Machine-op-inspct", "Adm-clerical", "Farming-fishing",
                    "Transport-moving", "Priv-house-serv", "Protective-serv",
                    "Armed-Forces"]

relationship_opts = ["Wife", "Own-child", "Husband", "Not-in-family",
                     "Other-relative", "Unmarried"]

race_opts = ["White", "Asian-Pac-Islander", "Amer-Indian-Eskimo", "Other", "Black"]

sex_opts = ["Female", "Male"]

native_country_opts = ["United-States", "Cambodia", "England", "Puerto-Rico",
                       "Canada", "Germany", "Outlying-US(Guam-USVI-etc)",
                       "India", "Japan", "Greece", "South", "China", "Cuba", "Iran",
                       "Honduras", "Philippines", "Italy", "Poland", "Jamaica",
                       "Vietnam", "Mexico", "Portugal", "Ireland", "France",
                       "Dominican-Republic", "Laos", "Ecuador", "Taiwan", "Haiti",
                       "Columbia", "Hungary", "Guatemala", "Nicaragua", "Scotland",
                       "Thailand", "Yugoslavia", "El-Salvador", "Trinadad&Tobago",
                       "Peru", "Hong", "Holand-Netherlands"]


# Prediction function
def predict_income(age, workclass, fnlwgt, education, education_num, marital_status,
                    occupation, relationship, race, sex, capital_gain,
                    capital_loss, hours_per_week, native_country):

    # Build dataframe for model
    sample = pd.DataFrame([{
        "age": age,
        "workclass": workclass,
        "fnlwgt": fnlwgt,
        "education": education,
        "education-num": education_num,
        "marital-status": marital_status,
        "occupation": occupation,
        "relationship": relationship,
        "race": race,
        "sex": sex,
        "capital-gain": capital_gain,
        "capital-loss": capital_loss,
        "hours-per-week": hours_per_week,
        "native-country": native_country
    }])

    pred = model.predict(sample)[0]
    proba = model.predict_proba(sample)[0]
    confidence = round(max(proba) * 100, 2)

    label = ">50K (High Income)" if pred == ">50K" or pred == 1 else "<=50K (Low Income)"

    return f"""
 **Predicted Income:** {label}
 **Confidence:** {confidence}%
 **Based on your input:**
- Age: {age}
- Workclass: {workclass}
- Education: {education}
- Hours per week: {hours_per_week}
- Occupation: {occupation}
- Marital Status: {marital_status}
"""


# Gradio Interface
demo = gr.Interface(
    fn=predict_income,
    inputs=[
        gr.Number(label="Age"),
        gr.Dropdown(workclass_opts, label="Workclass"),
        gr.Number(label="fnlwgt"),
        gr.Dropdown(education_opts, label="Education"),
        gr.Number(label="Education-num"),
        gr.Dropdown(marital_opts, label="Marital Status"),
        gr.Dropdown(occupation_opts, label="Occupation"),
        gr.Dropdown(relationship_opts, label="Relationship"),
        gr.Dropdown(race_opts, label="Race"),
        gr.Dropdown(sex_opts, label="Sex"),
        gr.Number(label="Capital Gain"),
        gr.Number(label="Capital Loss"),
        gr.Number(label="Hours per Week"),
        gr.Dropdown(native_country_opts, label="Native Country")
    ],
outputs = gr.Textbox(
    label="Prediction",
    lines=4,
    max_lines=None,
    container=True
),
    title="Income Prediction Demo",
    description="Predict whether a person earns >50K or <=50K using a trained Random Forest model."
)

demo.launch(
    server_name="0.0.0.0",
    server_port=7860,
    debug=True
)
