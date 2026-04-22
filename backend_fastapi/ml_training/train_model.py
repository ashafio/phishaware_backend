import pandas as pd
import joblib
import os
import sys

# Path fix to see 'app' folder
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(current_dir, "..")))
from app.services.feature_extractor import extract_features

# 1. Load Data
df_phish = pd.read_csv(os.path.join(current_dir, "final_dataset.csv"))
df_safe = pd.read_csv(os.path.join(current_dir, "tranco_oneml_safe.csv"), names=['rank', 'url'], header=None)

# 2. Labeling
df_phish['label'] = 1
df_safe['label'] = 0

# 3. BALANCE & CLEAN: Take 10,000 of each to start
df_combined = pd.concat([
    df_phish[['url', 'label']].head(10000),
    df_safe[['url', 'label']].head(10000)
]).dropna()

# 4. EXTRACT: This uses the protocol-blind logic
print("Extracting features (Protocol Blind)...")
X = [extract_features(str(url)) for url in df_combined['url']]
y = df_combined['label']

# 5. TRAIN: Use a smaller max_depth to prevent overfitting (memorization)
from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LGBMClassifier(
    n_estimators=500, 
    learning_rate=0.05, 
    max_depth=5,     # Hard limit on depth prevents memorizing specific URLs
    min_child_samples=20
)
model.fit(X_train, y_train)

# 6. SAVE
joblib.dump(model, os.path.join(current_dir, "../model/phishing_model.pkl"))
print(f"Model saved. Test Accuracy: {model.score(X_test, y_test)}")