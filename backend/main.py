from fastapi import FastAPI

app = FastAPI(
    title="Smart Employee Intelligence System API",
    description="Backend API for Smart Employee Intelligence System",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to Smart Employee Intelligence System API",
        "status": "Running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "Healthy"
    }