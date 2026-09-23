from fastapi import APIRouter, Depends

from models.leave import LeaveRequest

from security.role_checker import require_role

from services.hr_service import get_hr_department_id

from services.leave_service import (
    apply_leave_service,
    get_my_leave_requests_service,
    get_all_leave_requests_service,
    approve_leave_service,
    reject_leave_service,
    get_my_leave_service,
    get_leave_dashboard_service,
)

router = APIRouter()


@router.post("/leave/apply")
def apply_leave(
    leave: LeaveRequest,
    current_user=Depends(require_role("Employee"))
):
    employee_id = current_user["employee_id"]

    return apply_leave_service(
        employee_id,
        leave
    )


@router.get("/leave/my")
def get_my_leave_requests(
    current_user=Depends(require_role("Employee"))
):
    employee_id = current_user["employee_id"]

    return get_my_leave_requests_service(
        employee_id
    )


@router.get("/leave")
def get_all_leave_requests(
    current_user=Depends(require_role("Admin", "HR"))
):
    department_id = None

    if current_user["role"].lower() == "hr":
        department_id = get_hr_department_id(
            current_user
        )

    return get_all_leave_requests_service(
        department_id=department_id
    )


@router.put("/leave/approve/{leave_id}")
def approve_leave(
    leave_id: int,
    current_user=Depends(require_role("Admin", "HR"))
):
    department_id = None

    if current_user["role"].lower() == "hr":
        department_id = get_hr_department_id(
            current_user
        )

    return approve_leave_service(
        leave_id,
        department_id=department_id
    )


@router.put("/leave/reject/{leave_id}")
def reject_leave(
    leave_id: int,
    current_user=Depends(require_role("Admin", "HR"))
):
    department_id = None

    if current_user["role"].lower() == "hr":
        department_id = get_hr_department_id(
            current_user
        )

    return reject_leave_service(
        leave_id,
        department_id=department_id
    )


@router.get("/employee/me/leave")
def get_my_leave(
    current_user=Depends(require_role("Employee"))
):
    employee_id = current_user["employee_id"]

    return get_my_leave_service(
        employee_id
    )


@router.get("/leave/dashboard")
def get_leave_dashboard(
    current_user=Depends(require_role("Admin", "HR"))
):
    department_id = None

    if current_user["role"].lower() == "hr":
        department_id = get_hr_department_id(
            current_user
        )

    return get_leave_dashboard_service(
        department_id=department_id
    )