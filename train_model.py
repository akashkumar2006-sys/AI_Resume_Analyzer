import pandas as pd
import os
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline


# Dataset path
DATASET_PATH = "dataset/careers.csv"


# Load dataset
data = pd.read_csv(DATASET_PATH)


# Input and output
X = data["Skills"]
y = data["Career"]


# ML Pipeline
model = Pipeline([

    ("tfidf", TfidfVectorizer()),

    ("classifier", RandomForestClassifier(
        n_estimators=100,
        random_state=42
    ))

])


# Train model
model.fit(X, y)


# Create model folder
if not os.path.exists("model"):
    os.makedirs("model")


# Save model
joblib.dump(
    model,
    "model/resume_model.pkl"
)


print("✅ Model trained successfully!")
print("✅ Model saved: model/resume_model.pkl")
