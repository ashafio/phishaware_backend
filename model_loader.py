import os
import joblib
import gdown

MODEL_DIR = "model"
MODEL_PATH = os.path.join(MODEL_DIR, "phishing_model.pkl")

FILE_ID = "1Ps8gpq4i4lVdoLbKDCZvVrx_OcuHF1U7"

MODEL_URL = f"https://drive.google.com/uc?id={FILE_ID}"


def download_model():
    os.makedirs(MODEL_DIR, exist_ok=True)

    if not os.path.exists(MODEL_PATH):
        print("📥 Model not found locally")
        print("⬇ Downloading model from Google Drive...")

        gdown.download(MODEL_URL, MODEL_PATH, quiet=False)

        print("✅ Model downloaded successfully")
    else:
        print("✅ Model already exists locally")


def load_model():
    download_model()

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("❌ Failed to load model")

    model = joblib.load(MODEL_PATH)

    print("✅ Model loaded successfully")

    return model