import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv("Training.csv")

X = df.drop("prognosis", axis=1)
y = df["prognosis"]

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X, y)

joblib.dump(
    model,
    "disease_model.pkl"
)

print("Model Trained Successfully")
print("Features:", len(X.columns))