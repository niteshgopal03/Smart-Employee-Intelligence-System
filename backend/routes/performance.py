from fastapi import APIRouter, Depends

from models.performance import PerformanceUpdate
from services.performance_service import (
    update_manager_rating,
    get_manager_rating
)

from security.role_checker import require_role


router = APIRouter()


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
    current_user=Depends(
        require_role("Admin", "HR")
    )
):

    return get_manager_rating(employee_id)