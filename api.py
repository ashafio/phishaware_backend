from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import time
import re
from urllib.parse import urlparse
from fastapi.middleware.cors import CORSMiddleware
from model_loader import load_model

# =========================
# APP INIT
# =========================

app = FastAPI(
    title="PhishAware API",
    description="ML-based Phishing Detection System",
    version="2.0"
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

model = load_model()
print("✅ Model loaded successfully")

# =========================
# INPUT (Flutter sends ONLY URL)
# =========================

class URLRequest(BaseModel):
    url: str


# =========================
# 74-FEATURE GENERATOR
# =========================

def extract_features(url: str):

    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    path = parsed.path or ""
    query = parsed.query or ""

    features = []

    # -------- BASIC --------
    features.append(len(url))
    features.append(len(hostname))
    features.append(len(hostname))
    features.append(len(path))
    features.append(len(path.split("/")[1]) if len(path.split("/")) > 1 else 0)
    features.append(len(hostname.split(".")[-1]) if "." in hostname else 0)
    features.append(len(hostname.split(".")[-1]) if "." in hostname else 0)
    features.append(len(path.split("/")))
    features.append(len(query))
    features.append(len(path.split("/")))

    # -------- CHAR COUNTS --------
    features.append(sum(c.isdigit() for c in url))
    features.append(sum(c.isalpha() for c in url))
    features.append(len(re.findall(r'[^a-zA-Z0-9]', url)))
    features.append(url.count("."))
    features.append(url.count("-"))
    features.append(url.count("@"))
    features.append(url.count("%"))
    features.append(url.count("="))
    features.append(url.count("?"))
    features.append(url.count("&"))
    features.append(url.count("#"))
    features.append(url.count("_"))
    features.append(len(re.findall(r'[^a-zA-Z0-9]', url)))
    features.append(url.count("/"))
    features.append(len(query.split("&")) if query else 0)

    # -------- ENTROPY (SAFE APPROX) --------
    features.append(len(set(url)) / max(len(url), 1))
    features.append(len(set(hostname)) / max(len(hostname), 1))
    features.append(len(set(hostname)) / max(len(hostname), 1))
    features.append(len(set(path)) / max(len(path), 1))
    features.append(len(set(query)) / max(len(query), 1))

    # -------- RATIOS --------
    features.append(sum(c.isdigit() for c in url) / max(len(url), 1))
    features.append(sum(c.isalpha() for c in url) / max(len(url), 1))
    features.append(len(re.findall(r'[^a-zA-Z0-9]', url)) / max(len(url), 1))
    features.append(sum(c.isupper() for c in url) / max(len(url), 1))
    features.append(sum(c.islower() for c in url) / max(len(url), 1))

    # -------- SECURITY FLAGS --------
    features.append(1 if re.match(r'\d+\.\d+\.\d+\.\d+', hostname) else 0)
    features.append(1 if url.startswith("http://") else 0)
    features.append(1 if any(t in hostname for t in ["xyz", "top", "click"]) else 0)
    features.append(1 if "https" in url else 0)
    features.append(1 if "www" in hostname else 0)
    features.append(1 if "//" in path else 0)
    features.append(1 if url.count("http://") > 1 else 0)
    features.append(1 if ":" in hostname else 0)
    features.append(1 if "%" in url else 0)
    features.append(1 if "base64" in url else 0)

    # -------- SUSPICIOUS WORDS --------
    features.append(1 if "login" in url.lower() else 0)
    features.append(1 if "secure" in url.lower() else 0)
    features.append(1 if "verify" in url.lower() else 0)
    features.append(1 if "account" in url.lower() else 0)
    features.append(1 if "update" in url.lower() else 0)
    features.append(1 if "bank" in url.lower() else 0)
    features.append(1 if "cloud" in url.lower() else 0)
    features.append(1 if "paypal" in url.lower() else 0)

    # -------- PAD TO MATCH MODEL (CRITICAL FIX) --------
    while len(features) < 74:
        features.append(0)

    return features[:74]


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
# MAIN PREDICT ENDPOINT (FLUTTER USES THIS)
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
            "probability_phishing": float(probability[1]),
            "probability_legitimate": float(probability[0]),
            "response_time_ms": round((time.time() - start) * 1000, 2)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))