from fastapi import APIRouter, Depends

from security.role_checker import require_role
from services.hr_service import (
    get_hr_department_id,
    get_employee_report_service,
    get_department_report_service,
    get_attendance_report_service,
    get_leave_report_service,
    get_performance_report_service,
    get_salary_report_service,
)


router = APIRouter()


@router.get("/hr/reports/employees")
def employee_report(
    current_user=Depends(require_role("Admin", "HR"))
):
    department_id = None

    if current_user["role"].lower() == "hr":
        department_id = get_hr_department_id(current_user)

    return get_employee_report_service(
        department_id=department_id
    )


@router.get("/hr/reports/departments")
def department_report(
    current_user=Depends(require_role("Admin", "HR"))
):
    department_id = None

    if current_user["role"].lower() == "hr":
        department_id = get_hr_department_id(current_user)

    return get_department_report_service(
        department_id=department_id
    )


@router.get("/hr/reports/attendance")
def attendance_report(
    current_user=Depends(require_role("Admin", "HR"))
):
    department_id = None

    if current_user["role"].lower() == "hr":
        department_id = get_hr_department_id(current_user)

    return get_attendance_report_service(
        department_id=department_id
    )


@router.get("/hr/reports/leave")
def leave_report(
    current_user=Depends(require_role("Admin", "HR"))
):
    department_id = None

    if current_user["role"].lower() == "hr":
        department_id = get_hr_department_id(current_user)

    return get_leave_report_service(
        department_id=department_id
    )


@router.get("/hr/reports/performance")
def performance_report(
    current_user=Depends(require_role("Admin", "HR"))
):
    department_id = None

    if current_user["role"].lower() == "hr":
        department_id = get_hr_department_id(current_user)

    return get_performance_report_service(
        department_id=department_id
    )


@router.get("/hr/reports/salary")
def salary_report(
    current_user=Depends(require_role("Admin", "HR"))
):
    department_id = None

    if current_user["role"].lower() == "hr":
        department_id = get_hr_department_id(current_user)

    return get_salary_report_service(
        department_id=department_id
    )