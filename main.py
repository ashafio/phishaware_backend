import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# =========================
# CONFIG PATHS
# =========================

DATA_PATH = "final_dataset.csv"
MODEL_PATH = "phishawaremodel.pkl"

# =========================
# LOAD DATASET
# =========================

df = pd.read_csv(DATA_PATH)

# Drop non-useful column
if "url" in df.columns:
    df = df.drop(columns=["url"])

# Remove missing values
df = df.dropna()

# =========================
# SPLIT FEATURES / LABEL
# =========================

X = df.drop(columns=["label"])
y = df["label"]

# =========================
# TRAIN TEST SPLIT
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# TRAIN MODEL
# =========================

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print("✅ Model trained successfully")

# =========================
# CREATE MODEL FOLDER IF NOT EXISTS
# =========================

os.makedirs("model", exist_ok=True)

# =========================
# SAVE MODEL
# =========================

joblib.dump(model, MODEL_PATH)

print(f"✅ Model saved at {MODEL_PATH}")