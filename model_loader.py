import os
import gdown
import joblib

MODEL_PATH = "phishawaremodel.pkl"

FILE_ID = "18HaDZ_K_GrV82NfQsVhGRbf4uFNn5Awl"
MODEL_URL = f"https://drive.google.com/uc?id={FILE_ID}"


def download_model():
    os.makedirs("model", exist_ok=True)

    if not os.path.exists(MODEL_PATH):
        print("📥 Downloading model...")
        gdown.download(MODEL_URL, MODEL_PATH, quiet=False)
        print("✅ Model downloaded")
    else:
        print("✅ Model already exists")


def load_model():
    download_model()
    model = joblib.load(MODEL_PATH)

    # 🔥 IMPORTANT: get expected feature size
    feature_count = model.n_features_in_

    print(f"✅ Model loaded with {feature_count} features")

    return model, feature_count