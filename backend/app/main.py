from fastapi import FastAPI

#Instance of FastAPI application to provide metadata
app = FastAPI(
    title="AquaGuard AI",
    description="AI-powered water conservation and leakage detection system",
    version="1.0.0"
)

#define get endpoint at root url
@app.get("/")
def root():
    return {
        "message": "AquaGuard AI API is running"
    }


#Define get endpoint at health
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }