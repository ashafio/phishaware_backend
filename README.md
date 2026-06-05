# PhishAware Backend

> Python-based ML inference API serving the [PhishAware](https://github.com/ashafio/phishaware) Flutter app — part of the research study:
> **"A Comparative Evaluation of Machine Learning-Based Detection and Behavioural Warning Interventions in Reducing User Susceptibility to Phishing Attacks"**

---

## Overview

This backend exposes a REST API built with **FastAPI** that receives URLs or link data from the PhishAware mobile app, extracts engineered features, and runs them through a trained **LightGBM** classification model to predict whether a given link is a phishing attempt or legitimate.

It is containerised with Docker and designed for cloud deployment on platforms that support dynamic port binding (e.g. Render, Railway, Fly.io).

---

## Architecture

```
PhishAware Flutter App
        │
        │  HTTP POST /predict
        ▼
┌─────────────────────────┐
│   FastAPI (main.py)     │
│   CORS enabled          │
├─────────────────────────┤
│  feature_extractor.py   │  ← URL/link feature engineering
│  model_loader.py        │  ← loads trained .pkl model (via gdown)
│  predictor.py           │  ← runs inference
│  predict.py             │  ← API router
└─────────────────────────┘
        │
        ▼
  LightGBM Model
  (scikit-learn pipeline)
```

---

## Tech Stack

| Component | Technology |
|---|---|
| API Framework | FastAPI |
| Server | Uvicorn |
| ML Model | LightGBM |
| Data Processing | pandas, NumPy, scikit-learn |
| Model Loading | joblib, gdown |
| Config | python-dotenv |
| Container | Docker (python:3.10-slim) |

---

## Project Structure

```
phishaware_backend/
├── main.py                # FastAPI app entry point, CORS, router registration
├── predict.py             # API route definitions (/predict)
├── predictor.py           # Inference logic
├── model_loader.py        # Downloads and loads the trained model
├── feature_extractor.py   # URL feature extraction
├── train_model.py         # Model training script
├── prepare_dataset.py     # Dataset preparation utilities
├── requirements.txt       # Python dependencies
├── packages.txt           # System-level packages
└── Dockerfile             # Container definition
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- pip
- Docker (optional, for containerised deployment)

### Local Setup

1. **Clone the repository**

```bash
   git clone https://github.com/ashafio/phishaware_backend.git
   cd phishaware_backend
```

2. **Install dependencies**

```bash
   pip install -r requirements.txt
```

3. **Run the server**

```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

4. **Check it's running**

```
   GET http://localhost:8000/health
   → {"status": "ok"}
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check — returns API name and version |
| `GET` | `/health` | Simple liveness probe |
| `POST` | `/predict` | Accepts a URL and returns a phishing classification |

---

## Docker

### Build and run locally

```bash
docker build -t phishaware-backend .
docker run -e PORT=8000 -p 8000:8000 phishaware-backend
```

### Dockerfile summary

```dockerfile
FROM python:3.10-slim
RUN apt-get update && apt-get install -y libgomp1   # required by LightGBM
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]
```

The `PORT` environment variable is injected at runtime, which is compatible with most cloud platforms.

---

## Model Training

To retrain the model from scratch:

```bash
python prepare_dataset.py   # prepare and clean dataset
python train_model.py       # train LightGBM classifier and export model
```

The trained model is loaded at startup by `model_loader.py`, which uses `gdown` to fetch it from Google Drive if not present locally.

---

## Academic Context

This backend is the ML inference component of the PhishAware research project, which investigates whether machine learning-based detection or behavioural warning interventions are more effective at reducing user susceptibility to phishing attacks.

> Shafi, A. (2026). *A Comparative Evaluation of Machine Learning-Based Detection and Behavioural Warning Interventions in Reducing User Susceptibility to Phishing Attacks*. MSc Software Engineering, University of Hertfordshire.

---

## Licence

This project is developed for academic research purposes. All rights reserved by the author. For enquiries, contact the repository owner.

---

## Author

**Shafi** — MSc Software Engineering, University of Hertfordshire  
GitHub: [@ashafio](https://github.com/ashafio)
