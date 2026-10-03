"""Loads the trained model + label encoders and makes predictions."""
import os

import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model.joblib")
ENCODER_PATH = os.path.join(BASE_DIR, "label_encoders")

GRADE_TO_LEVEL = {
    "A+": "Excellent",
    "A": "Very Good",
    "B": "Good",
    "C": "Average",
    "D": "Below Average",
    "F": "Poor",
}

# Load model + encoders once at import time
_model = joblib.load(MODEL_PATH)
_encoders = {
    "gender": joblib.load(os.path.join(ENCODER_PATH, "gender.joblib")),
    "ethnicity": joblib.load(os.path.join(ENCODER_PATH, "ethnicity.joblib")),
    "parental education": joblib.load(os.path.join(ENCODER_PATH, "parental_education.joblib")),
    "lunch": joblib.load(os.path.join(ENCODER_PATH, "lunch.joblib")),
    "test preparation course": joblib.load(os.path.join(ENCODER_PATH, "test_prep_course.joblib")),
    "grade": joblib.load(os.path.join(ENCODER_PATH, "grade.joblib")),
}


def predict_performance(gender, ethnicity, parental_education, lunch,
                        test_prep_course, math_score, reading_score, writing_score):
    """Return (grade, level) predicted for the given student details."""
    sample = {
        "gender": _encoders["gender"].transform([gender])[0],
        "race/ethnicity": _encoders["ethnicity"].transform([ethnicity])[0],
        "parental level of education":
            _encoders["parental education"].transform([parental_education])[0],
        "lunch": _encoders["lunch"].transform([lunch])[0],
        "test preparation course":
            _encoders["test preparation course"].transform([test_prep_course])[0],
        "math score": int(math_score),
        "reading score": int(reading_score),
        "writing score": int(writing_score),
    }

    # Build a DataFrame with the same column order used during training
    features = pd.DataFrame([sample])
    features = features[[
        "gender",
        "race/ethnicity",
        "parental level of education",
        "lunch",
        "test preparation course",
        "math score",
        "reading score",
        "writing score",
    ]]

    encoded_grade = _model.predict(features)[0]
    grade = _encoders["grade"].inverse_transform([encoded_grade])[0]
    level = GRADE_TO_LEVEL.get(grade, "Unknown")
    return grade, level