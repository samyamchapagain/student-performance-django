# Student Performance Prediction System

A Django web application that predicts student performance using a machine learning model. Users register, log in, enter a student's details and get a predicted performance class. Prediction history is saved per user.

Built as a university project at Sunway College (Birmingham City University).

## Features

- User registration and login
- Prediction form backed by a trained Gradient Boosting classifier
- Prediction history for each user
- Admin view of all users and all predictions
- Automated end-to-end test

## Tech Stack

- Python, Django
- scikit-learn, pandas, joblib
- SQLite
- Jupyter / Colab notebook for exploration and training

## Results

Both models were trained and evaluated on the same train/test split.

| Model                                       | Test Accuracy |
| ------------------------------------------- | ------------- |
| Support Vector Machine (RBF)                | 92.50%        |
| **Gradient Boosting Classifier (deployed)** | **95.00%**    |

## Folder Structure

| Folder | Contents |
| ------ | -------- |
| `Project_Source_Code/` | The Django application: views, models, forms, templates, static files, trained model (`prediction/ml_model/model.joblib` and label encoders), the model training script and automated tests |
| `Dataset/` | `StudentsPerformance.csv`, the dataset used to train and test the model (1,000 records, 8 attributes) |
| `ML_Notebook/` | `Final.ipynb`, covering data exploration, preprocessing, model training (SVM and Gradient Boosting) and evaluation |

## How to Run

```bash
# 1. Enter the project folder
cd Project_Source_Code

# 2. Install dependencies
python -m pip install django scikit-learn pandas joblib

# 3. (Optional) Re-train the model from the dataset
python train_model.py

# 4. Create the database tables
python manage.py migrate

# 5. Create an admin account for the admin panel
python manage.py createsuperuser

# 6. Start the server
python manage.py runserver
```

Then open http://127.0.0.1:8000/, register an account, log in and make predictions.

### Admin

- Admin panel: http://127.0.0.1:8000/admin/ (log in with the account you created in step 5)
- All users: `/users/`
- All predictions with usernames: `/history/`

## Notes

- The local SQLite database is not included in this repository. Running `migrate` creates a fresh one.
- This is a student project. Before using it anywhere real, set a new `SECRET_KEY`, turn off `DEBUG` and review the security settings.

## Author

Samyam Chapagain
[GitHub](https://github.com/samyamchapagain)
