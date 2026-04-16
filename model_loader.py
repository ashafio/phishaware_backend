import os
import gdown
import joblib



MODEL_PATH = "phishawaremodel.pkl"

FILE_ID = "1LCqWuVKJVznXOLWrrvEi-XerA_6KAEX0"
MODEL_URL = f"https://drive.google.com/uc?id={FILE_ID}"


def download_model():
    if not os.path.exists(MODEL_PATH):
        print("📥 Downloading model...")

        gdown.download(MODEL_URL, MODEL_PATH, quiet=False)

        print("✅ Model downloaded!")
    else:
        print("✅ Model already exists")


def load_model():
    download_model()
    return joblib.load(MODEL_PATH)