from fastapi import APIRouter, Depends

from models.attendance import Attendance

from services.attendance_service import (
    mark_attendance_service,
    update_attendance_service,
    get_employee_attendance_service,
    get_all_attendance_service,
    get_attendance_percentage_service
)

from security.role_checker import require_role


router = APIRouter()


@router.post("/attendance/mark")
def mark_attendance(
    attendance: Attendance,
    current_user=Depends(require_role("HR"))
):
    return mark_attendance_service(attendance)


@router.put("/attendance/update/{attendance_id}")
def update_attendance(
    attendance_id: int,
    attendance: Attendance,
    current_user=Depends(require_role("HR"))
):
    return update_attendance_service(
        attendance_id,
        attendance
    )


@router.get("/attendance")
def get_all_attendance(
    current_user=Depends(require_role("Admin", "HR"))
):
    return get_all_attendance_service()


@router.get("/attendance/employee/{employee_id}")
def get_employee_attendance(
    employee_id: str,
    current_user=Depends(require_role("Admin", "HR"))
):
    return get_employee_attendance_service(employee_id)


@router.get("/attendance/percentage/{employee_id}")
def get_attendance_percentage(
    employee_id: str,
    current_user=Depends(require_role("Admin", "HR"))
):
    return get_attendance_percentage_service(employee_id)


@router.get("/attendance/my")
def get_my_attendance(
    current_user=Depends(require_role("Employee"))
):
    employee_id = current_user["employee_id"]

    return get_employee_attendance_service(employee_id)


@router.get("/attendance/my/percentage")
def get_my_attendance_percentage(
    current_user=Depends(require_role("Employee"))
):
    employee_id = current_user["employee_id"]

    return get_attendance_percentage_service(employee_id)