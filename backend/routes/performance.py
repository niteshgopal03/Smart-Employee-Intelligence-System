from fastapi import APIRouter, Depends,HTTPException

from models.performance import PerformanceUpdate
from services.performance_service import (
    update_manager_rating,
    get_manager_rating,
    get_performance_dashboard_service
)

from security.role_checker import require_role


router = APIRouter()

@router.get("/performance/dashboard")
def get_performance_dashboard(
    current_user=Depends(require_role("Admin", "HR","Employee"))
):
    return get_performance_dashboard_service()

@router.put("/performance/{employee_id}")
def update_performance(
    employee_id: str,
    data: PerformanceUpdate,
    current_user=Depends(
        require_role("Admin", "HR")
    )
):

    return update_manager_rating(
        employee_id,
        data.manager_rating
    )


@router.get("/performance/{employee_id}")
def get_performance(
    employee_id: str,
    current_user=Depends(require_role("Admin", "HR", "Employee"))
):
    if current_user["role"].lower() == "employee":
        if current_user["employee_id"] != employee_id:
            raise HTTPException(
                status_code=403,
                detail="Employees can only view their own performance."
            )
    return get_manager_rating(employee_id)

