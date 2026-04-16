import os
import gdown
import joblib

# =========================
# LOCAL CACHE PATH
# =========================
MODEL_PATH = "phishawaremodel.pkl"

# =========================
# GOOGLE DRIVE FILE ID
# =========================
FILE_ID = "1LCqWuVKJVznXOLWrrvEi-XerA_6KAEX0"

# Proper gdown URL format
MODEL_URL = f"https://drive.google.com/uc?id={FILE_ID}"


def download_model():
    """
    Download model from Google Drive if not exists locally
    """
    if not os.path.exists(MODEL_PATH):
        print("📥 Downloading model from Google Drive...")

        gdown.download(MODEL_URL, MODEL_PATH, quiet=False)

        print("✅ Model downloaded successfully!")
    else:
        print("✅ Model already exists locally")


def load_model():
    """
    Load ML model safely
    """
    download_model()

    try:
        model = joblib.load(MODEL_PATH)
        print("✅ Model loaded successfully")
        return model

    except Exception as e:
        raise RuntimeError(f"❌ Model loading failed: {e}")