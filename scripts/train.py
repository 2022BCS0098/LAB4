import json
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# ------------------ LOAD DATA ------------------
DATA_PATH = "dataset/winequality-red.csv"

df = pd.read_csv(DATA_PATH, sep=";")

X = df.drop("quality", axis=1)
y = df["quality"]

# ------------------ TRAIN-TEST SPLIT ------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ------------------ MODEL ------------------
model = LinearRegression()
model.fit(X_train, y_train)

# ------------------ PREDICTION ------------------
y_pred = model.predict(X_test)

# ------------------ METRICS ------------------
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# ------------------ SAVE MODEL ------------------
joblib.dump(model, "model.pkl")

# ------------------ SAVE METRICS ------------------
metrics = {
    "r2": float(r2),
    "mse": float(mse)
}

with open("metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

# ------------------ LOGS ------------------
print("Training complete")
print(f"R2 Score: {r2}")
print(f"MSE: {mse}")
