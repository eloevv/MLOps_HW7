import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import json
import os

iris = load_iris()
X = iris.data
y = iris.target

hyperparameters = {"n_estimators": 100, "random_state": 42}

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(**hyperparameters)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Accuracy: {accuracy:.2f}")

os.makedirs("artifacts", exist_ok=True)
joblib.dump(model, "artifacts/model.pkl")

with open("artifacts/metrics.json", "w") as f:
    json.dump({"accuracy": round(float(accuracy), 4), "hyperparameters": hyperparameters}, f)

with open("artifacts/hyperparameters.json", "w") as f:
    json.dump(hyperparameters, f)

print("Artifacts saved to artifacts/")
