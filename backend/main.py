from fastapi import FastAPI
from routes.employee import router as employee_router
from routes.auth import router as auth_router
from routes.attendance import router as attendance_router

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


app.include_router(employee_router)
app.include_router(auth_router)
app.include_router(attendance_router)