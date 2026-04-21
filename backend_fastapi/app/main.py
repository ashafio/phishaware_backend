from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import ONLY prediction route
from app.api.routes import predict

app = FastAPI(
    title="LinkBox ML API",
    description="Phishing Detection Service",
    version="1.0"
)

# ✅ CORS (needed for Flutter)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # For production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register routes
app.include_router(predict.router)


# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def root():
    return {"message": "LinkBox ML API running 🚀"}


@app.get("/health")
def health():
    return {"status": "ok"}