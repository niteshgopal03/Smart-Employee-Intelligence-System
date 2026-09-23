from fastapi import APIRouter, Depends

from models.attendance import Attendance

from services.attendance_service import (
    mark_attendance_service,
    update_attendance_service,
    get_employee_attendance_service,
    get_all_attendance_service,
    get_attendance_percentage_service,
    get_my_monthly_attendance_service,
    get_attendance_dashboard_service,
)

from services.hr_service import get_hr_department_id

from security.role_checker import require_role


router = APIRouter()


@router.post("/attendance/mark")
def mark_attendance(
    attendance: Attendance,
    current_user=Depends(require_role("Admin", "HR"))
):
    department_id = None

    if current_user["role"].lower() == "hr":
        department_id = get_hr_department_id(current_user)

    return mark_attendance_service(
        attendance,
        department_id=department_id
    )


@router.put("/attendance/update/{attendance_id}")
def update_attendance(
    attendance_id: int,
    attendance: Attendance,
    current_user=Depends(require_role("Admin", "HR"))
):
    department_id = None

    if current_user["role"].lower() == "hr":
        department_id = get_hr_department_id(current_user)

    return update_attendance_service(
        attendance_id,
        attendance,
        department_id=department_id
    )


@router.get("/attendance")
def get_all_attendance(
    current_user=Depends(require_role("Admin", "HR"))
):
    department_id = None

    if current_user["role"].lower() == "hr":
        department_id = get_hr_department_id(current_user)

    return get_all_attendance_service(
        department_id=department_id
    )


@router.get("/attendance/employee/{employee_id}")
def get_employee_attendance(
    employee_id: str,
    current_user=Depends(require_role("Admin", "HR"))
):
    department_id = None

    if current_user["role"].lower() == "hr":
        department_id = get_hr_department_id(current_user)

    return get_employee_attendance_service(
        employee_id,
        department_id=department_id
    )


@router.get("/attendance/percentage/{employee_id}")
def get_attendance_percentage(
    employee_id: str,
    current_user=Depends(require_role("Admin", "HR"))
):
    department_id = None

    if current_user["role"].lower() == "hr":
        department_id = get_hr_department_id(current_user)

    return get_attendance_percentage_service(
        employee_id,
        department_id=department_id
    )


@router.get("/attendance/my")
def get_my_attendance(
    current_user=Depends(require_role("Employee"))
):
    employee_id = current_user["employee_id"]

    return get_employee_attendance_service(
        employee_id
    )


@router.get("/employee/me/attendance")
def get_my_monthly_attendance(
    month: int,
    year: int,
    current_user=Depends(require_role("Employee"))
):
    employee_id = current_user["employee_id"]

    if month < 1 or month > 12:
        return {
            "message": "Month must be between 1 and 12"
        }

    if year < 2000 or year > 2100:
        return {
            "message": "Invalid year"
        }

    return get_my_monthly_attendance_service(
        employee_id,
        month,
        year
    )


@router.get("/attendance/my/percentage")
def get_my_attendance_percentage(
    current_user=Depends(require_role("Employee"))
):
    employee_id = current_user["employee_id"]

    return get_attendance_percentage_service(
        employee_id
    )


@router.get("/attendance/dashboard")
def get_attendance_dashboard(
    current_user=Depends(require_role("Admin", "HR"))
):
    department_id = None

    if current_user["role"].lower() == "hr":
        department_id = get_hr_department_id(current_user)

    return get_attendance_dashboard_service(
        department_id=department_id
    )