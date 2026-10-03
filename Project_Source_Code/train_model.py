"""
Trains a Gradient Boosting Classifier on the Students Performance dataset
and saves the model + label encoders for use in the Django web app.

"""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "student_performance.settings")

import joblib
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

CSV_PATH = os.path.join(os.path.dirname(__file__), "StudentsPerformance.csv")
ML_DIR = os.path.join(os.path.dirname(__file__), "prediction", "ml_model")
ENCODER_DIR = os.path.join(ML_DIR, "label_encoders")


def assign_grade(avg):
    if avg >= 90:
        return "A+"
    elif avg >= 80:
        return "A"
    elif avg >= 70:
        return "B"
    elif avg >= 60:
        return "C"
    elif avg >= 50:
        return "D"
    else:
        return "F"


def main():
    os.makedirs(ENCODER_DIR, exist_ok=True)

    df = pd.read_csv(CSV_PATH)
    print(f"Dataset shape: {df.shape}")
    print(f"Missing values:\n{df.isnull().sum()}")

    df["average_score"] = (df["math score"] + df["reading score"] + df["writing score"]) / 3
    df["performance_grade"] = df["average_score"].apply(assign_grade)

    X = df[["gender", "race/ethnicity", "parental level of education",
            "lunch", "test preparation course",
            "math score", "reading score", "writing score"]].copy()
    y = df["performance_grade"]

    categorical_cols = ["gender", "race/ethnicity",
                        "parental level of education", "lunch",
                        "test preparation course"]

    encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        encoders[col] = le

    le_grade = LabelEncoder()
    y_encoded = le_grade.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )

    model = GradientBoostingClassifier(
        n_estimators=200, learning_rate=0.05, max_depth=3, random_state=42
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\nGradient Boosting Accuracy: {acc:.4f}")
    print(classification_report(
        le_grade.inverse_transform(y_test), le_grade.inverse_transform(y_pred)
    ))

    joblib.dump(model, os.path.join(ML_DIR, "model.joblib"))
    joblib.dump(encoders["gender"], os.path.join(ENCODER_DIR, "gender.joblib"))
    joblib.dump(encoders["race/ethnicity"], os.path.join(ENCODER_DIR, "ethnicity.joblib"))
    joblib.dump(encoders["parental level of education"],
                os.path.join(ENCODER_DIR, "parental_education.joblib"))
    joblib.dump(encoders["lunch"], os.path.join(ENCODER_DIR, "lunch.joblib"))
    joblib.dump(encoders["test preparation course"],
                os.path.join(ENCODER_DIR, "test_prep_course.joblib"))
    joblib.dump(le_grade, os.path.join(ENCODER_DIR, "grade.joblib"))

    print("\nModel and encoders saved to:", ML_DIR)


if __name__ == "__main__":
    main()