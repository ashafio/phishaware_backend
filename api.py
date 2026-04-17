from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import time
import re
from urllib.parse import urlparse
from fastapi.middleware.cors import CORSMiddleware
from model_loader import load_model

# =========================
# INIT
# =========================

app = FastAPI(
    title="PhishAware API",
    version="3.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# LOAD MODEL
# =========================

model, EXPECTED_FEATURES = load_model()


# =========================
# INPUT
# =========================

class URLRequest(BaseModel):
    url: str


# =========================
# FEATURE GENERATOR (CONSISTENT)
# =========================

def extract_features(url: str):

    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    path = parsed.path or ""
    query = parsed.query or ""

    # -------- BASIC (6) --------
    features = [
        len(url),
        len(hostname),
        len(path),
        len(query),
        len(hostname.split(".")),
        len(path.split("/")),
    ]

    # -------- COUNTS (8) --------
    features += [
        url.count("."),
        url.count("-"),
        url.count("@"),
        url.count("?"),
        url.count("&"),
        url.count("="),
        url.count("_"),
        url.count("/"),
    ]

    # -------- CHARACTER FEATURES (3) --------
    features += [
        sum(c.isdigit() for c in url),
        sum(c.isalpha() for c in url),
        len(re.findall(r'[^a-zA-Z0-9]', url)),
    ]

    # -------- RATIOS (2) --------
    length = max(len(url), 1)
    features += [
        sum(c.isdigit() for c in url) / length,
        sum(c.isalpha() for c in url) / length,
    ]

    # -------- FLAGS (3) --------
    features += [
        1 if url.startswith("https") else 0,
        1 if re.match(r'\d+\.\d+\.\d+\.\d+', hostname) else 0,
        1 if "login" in url.lower() else 0,
    ]

    # ✅ FINAL CHECK
    if len(features) != EXPECTED_FEATURES:
        raise ValueError(
            f"Feature mismatch: expected {EXPECTED_FEATURES}, got {len(features)}"
        )

    return features


# =========================
# ROUTES
# =========================

@app.get("/")
def home():
    return {"message": "PhishAware API running"}

@app.get("/health")
def health():
    return {"status": "healthy"}


# =========================
# PREDICT
# =========================

@app.post("/predicturl")
def predict_url(data: URLRequest):
    try:
        start = time.time()

        features = np.array([extract_features(data.url)])

        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0]

        return {
            "url": data.url,
            "prediction": int(prediction),
            "confidence": float(max(probability)),
            "phishing_probability": float(probability[1]),
            "legitimate_probability": float(probability[0]),
            "response_time_ms": round((time.time() - start) * 1000, 2)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))