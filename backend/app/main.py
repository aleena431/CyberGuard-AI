
from fastapi import FastAPI

app = FastAPI(
    title="CyberGuard AI",
    description="AI-powered cybersecurity threat analysis API",
    version="0.1.0",
)


@app.get("/")
def home():
    return {
        "message": "Welcome to CyberGuard AI",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "CyberGuard AI API",
    }


@app.get("/features")
def features():
    return {
        "features": [
            "Security log analysis",
            "Threat intelligence",
            "RAG-based investigation",
            "Incident reporting",
        ]
    }