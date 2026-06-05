import pandas as pd

df = pd.read_csv("Training.csv")

symptoms = list(
    df.drop("prognosis", axis=1).columns
)

print(symptoms)
print("\nTotal Symptoms =", len(symptoms))