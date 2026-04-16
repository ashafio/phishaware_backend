# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# import joblib

# # Load dataset
# df = pd.read_csv("data/final_dataset.csv")

# # Drop non-numeric column
# df = df.drop(columns=["url"])

# # Features and label
# X = df.drop(columns=["label"])
# y = df["label"]

# # Split
# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.2, random_state=42
# )

# # Train model
# model = RandomForestClassifier(n_estimators=100)
# model.fit(X_train, y_train)

# # Save model (IMPORTANT: use joblib)
# joblib.dump(model, "model/phishawaremodel.pkl")

# print("✅ Model trained and saved successfully")