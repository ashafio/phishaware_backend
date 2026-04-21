from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import time

from app.services.predictor import predict_url
from app.core.model_loader import load_model

router = APIRouter()

model = load_model()

class URLRequest(BaseModel):
    url: str

@router.post("/predicturl")
def predict(data: URLRequest):
    try:
        start = time.time()

        result = predict_url(model, data.url)

        return {
            "url": data.url,
            **result,
            "response_time_ms": round((time.time() - start) * 1000, 2)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))