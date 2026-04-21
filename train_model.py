import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

FEATURE_COLUMNS = [
    "url_length","hostname_length","path_length","query_length",
    "path_segments_count","num_dots","num_hyphens","num_at",
    "num_question","num_ampersand","num_equals","num_underscore",
    "num_slash","num_digits","num_letters","num_special_chars",
    "ratio_digits","ratio_letters","uses_https","is_ip_address",
    "contains_login"
]

df = pd.read_csv("final_dataset.csv")
df = df[FEATURE_COLUMNS + ["label"]].dropna()

X = df[FEATURE_COLUMNS]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier()
model.fit(X_train, y_train)

joblib.dump(model, "phishing_model.pkl")

print("✅ Model trained & saved")