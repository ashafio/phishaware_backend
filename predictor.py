import numpy as np
from feature_extractor import extract_features

def predict_url(model, url: str):
    # Get the list of 22 features
    features = extract_features(url) 
    
    # Convert to 2D array for the model: shape (1, 22)
    features_array = np.array([features])

    prediction = model.predict(features_array)[0]
    probability = model.predict_proba(features_array)[0]

    return {
        "prediction": int(prediction),
        "confidence": float(max(probability)),
        "phishing_probability": float(probability[1]),
        "legitimate_probability": float(probability[0]),
    }