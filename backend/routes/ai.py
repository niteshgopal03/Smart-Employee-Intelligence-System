from fastapi import APIRouter, Depends


from services.ai_service import (
    predict_salary_for_employee,
    predict_promotion_for_employee,
    predict_attrition_for_employee,
    get_attendance_features
)
from security.role_checker import require_role


router = APIRouter()


@router.post("/ai/employee/{employee_id}/salary")
def employee_salary_prediction(
    employee_id: str,
    current_user=Depends(
        require_role("Admin", "HR")
    )
):
    return predict_salary_for_employee(
        employee_id
    )



@router.post("/ai/employee/{employee_id}/promotion")
def employee_promotion_prediction(
    employee_id: str,
    current_user=Depends(
        require_role("Admin", "HR")
    )
):
    return predict_promotion_for_employee(
        employee_id
    )


@router.post("/ai/employee/{employee_id}/attrition")
def employee_attrition_prediction(
    employee_id: str,
    current_user=Depends(
        require_role("Admin", "HR")
    )
):
    return predict_attrition_for_employee(
        employee_id
    )