from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import predict

app = FastAPI(
    title="LinkBox ML API",
    version="FINAL"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict.router)

@app.get("/")
def root():
    return {"message": "LinkBox API running "}

@app.get("/health")
def health():
    return {"status": "ok"}