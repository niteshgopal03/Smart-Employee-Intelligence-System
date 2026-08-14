from fastapi import APIRouter, Depends

from models.hr import HR

from services.hr_service import (
    add_hr_service,
    delete_hr_service
)

from security.role_checker import require_role


router = APIRouter()


@router.post("/hr/add")
def add_hr(
    hr: HR,
    current_user=Depends(require_role("Admin"))
):
    return add_hr_service(hr)


@router.delete("/hr/{employee_id}")
def delete_hr(
    employee_id: str,
    current_user=Depends(require_role("Admin"))
):
    return delete_hr_service(employee_id)