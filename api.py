from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import os
import time
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="PhishAware API",
    description="Machine Learning + Behavioural Phishing Detection System",
    version="1.0"
)

# Enable CORS (Flutter support)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# GOOGLE DRIVE MODEL SETUP
# =========================

# MODEL_DIR = os.path.join(os.path.dirname(__file__), "../model")
# MODEL_PATH = os.path.join(MODEL_DIR, "phishawaremodel.pkl")
MODEL_PATH = os.path.join("phishawaremodel.pkl")

# 🔴 PUT YOUR GOOGLE DRIVE DIRECT DOWNLOAD LINK HERE
MODEL_URL = "https://drive.google.com/uc?id=1LCqWuVKJVznXOLWrrvEi-XerA_6KAEX0"


def download_model():
    """Download model from Google Drive if not exists"""
    if not os.path.exists(MODEL_PATH):
        print("⬇ Downloading model from Google Drive...")

        os.makedirs(MODEL_DIR, exist_ok=True)

        response = requests.get(MODEL_URL)
        if response.status_code != 200:
            raise RuntimeError("❌ Failed to download model")

        with open(MODEL_PATH, "wb") as f:
            f.write(response.content)

        print("✅ Model downloaded successfully")


# Load model safely
def load_model():
    download_model()
    return joblib.load(MODEL_PATH)


model = load_model()
print("✅ Model loaded successfully")

# =========================
# INPUT SCHEMA (UNCHANGED)
# =========================

class URLFeatures(BaseModel):
    url_length: float
    domain_length: float
    hostname_length: float
    path_length: float
    first_dir_length: float
    tld_length: float
    tld_length_domain: float
    url_depth: float
    query_length: float
    path_segments_count: float
    num_digits: float
    num_letters: float
    num_special_chars: float
    num_dots: float
    num_hyphens: float
    num_at: float
    num_percent: float
    num_equals: float
    num_question: float
    num_ampersand: float
    num_hash: float
    num_underscore: float
    num_special: float
    num_slash: float
    num_params: float
    entropy_url: float
    entropy_hostname: float
    entropy_domain: float
    entropy_path: float
    query_entropy: float
    ratio_digits: float
    ratio_letters: float
    ratio_special_chars: float
    uppercase_ratio: float
    lowercase_ratio: float
    is_ip_address: float
    starts_with_ip: float
    is_suspicious_tld: float
    uses_https: float
    has_www: float
    unusual_double_slash: float
    multiple_http: float
    contains_port_number: float
    path_has_encoded_chars: float
    query_has_base64: float
    contains_login: float
    contains_secure: float
    contains_verify: float
    contains_account: float
    contains_update: float
    contains_bank: float
    contains_cloud: float
    contains_brand: float
    query_key_count: float
    query_value_length_avg: float
    success: float
    dns_resolves: float
    has_mx_record: float
    has_txt_record: float
    has_ns_record: float
    ttl_value: float
    ip_count: float
    cname_count: float
    resolves_to_private_ip: float
    whois_success: float
    domain_age_days: float
    expiration_days: float
    creation_year: float
    domain_is_recent: float
    domain_registered_before_2020: float
    registrar_valid: float
    name_servers_count: float
    is_privacy_protected: float
    whois_missing: float


# =========================
# ROUTES
# =========================

@app.get("/")
def home():
    return {"message": "PhishAware API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/predict", summary="Predict phishing URL")
def predict(data: URLFeatures):
    try:
        start_time = time.time()

        features = np.array([list(data.dict().values())])

        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0]

        end_time = time.time()

        return {
            "prediction": int(prediction),
            "probability_phishing": float(probability[1]),
            "probability_legitimate": float(probability[0]),
            "response_time_ms": round((end_time - start_time) * 1000, 2)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))