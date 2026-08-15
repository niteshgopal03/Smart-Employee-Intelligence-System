from fastapi import APIRouter, Depends

from models.leave import LeaveRequest

from services.leave_service import (
    apply_leave_service,
    get_my_leave_requests_service,
    get_all_leave_requests_service,
    approve_leave_service,
    reject_leave_service
)

from security.role_checker import require_role


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
    return get_all_leave_requests_service()



@router.put("/leave/approve/{leave_id}")
def approve_leave(
    leave_id: int,
    current_user=Depends(require_role("HR"))
):
    return approve_leave_service(leave_id)



@router.put("/leave/reject/{leave_id}")
def reject_leave(
    leave_id: int,
    current_user=Depends(require_role("HR"))
):
    return reject_leave_service(leave_id)