from fastapi import FastAPI

from routes.auth import router as auth_router
from routes.employee import router as employee_router
from routes.hr import router as hr_router
from routes.attendance import router as attendance_router
from routes.leave import router as leave_router
from routes.password import router as password_router
from routes.performance import router as performance_router
from routes.ai import router as ai_router
from routes.admin_dashboard import router as admin_dashboard_router


app = FastAPI(
    title="Employee Management System API",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(hr_router)
app.include_router(employee_router)
app.include_router(attendance_router)
app.include_router(leave_router)
app.include_router(password_router)
app.include_router(performance_router)
app.include_router(ai_router)
app.include_router(admin_dashboard_router)

@app.get("/")
def home():

    return {
        "message": "Employee Management System API Running Successfully"
    }