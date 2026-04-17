import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

DATA_PATH = "final_dataset.csv"
MODEL_PATH = "phishawaremodel.pkl"

df = pd.read_csv(DATA_PATH)

# Drop unused
if "url" in df.columns:
    df = df.drop(columns=["url"])

df = df.dropna()

# 🔥 SELECT ONLY OUR FEATURES
selected_features = [
    "url_length",
    "hostname_length",
    "path_length",
    "query_length",
    "url_depth",
    "path_segments_count",
    "num_dots",
    "num_hyphens",
    "num_at",
    "num_question",
    "num_ampersand",
    "num_equals",
    "num_underscore",
    "num_slash",
    "num_digits",
    "num_letters",
    "num_special_chars",
    "ratio_digits",
    "ratio_letters",
    "uses_https",
    "is_ip_address",
    "contains_login"
]

X = df[selected_features]
y = df["label"]

print(f"📊 Using {len(selected_features)} features")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print("✅ Model trained")

os.makedirs("model", exist_ok=True)
joblib.dump(model, MODEL_PATH)

print("✅ Model saved")