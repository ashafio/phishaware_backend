import numpy as np
from app.services.feature_extractor import extract_features

EXPECTED_FEATURES = 21

def predict_url(model, url: str):
    features = extract_features(url)

    if len(features) != EXPECTED_FEATURES:
        raise ValueError(f"Feature mismatch: expected {EXPECTED_FEATURES}, got {len(features)}")

    features = np.array([features])

    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0]

    return {
        "prediction": int(prediction),
        "phishing_probability": float(probability[1]),
        "legitimate_probability": float(probability[0])
    }