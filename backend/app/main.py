from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.ai_analysis import router as ai_analysis_router
from app.routes.anomalies import router as anomalies_router


# Instance of FastAPI application
app = FastAPI(
    title="AquaGuard AI",
    description="AI-powered water conservation and leakage detection system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "AquaGuard AI API is running"
    }


# Health endpoint
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# AI analysis routes
app.include_router(ai_analysis_router)

# Anomaly routes
app.include_router(anomalies_router)