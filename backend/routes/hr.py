
from fastapi import APIRouter, Depends

from models.hr import HR

from services.hr_service import (
    add_hr_service,
    delete_hr_service,
    get_employee_report_service,
    get_department_report_service,
    get_attendance_report_service,
    get_leave_report_service,
    get_performance_report_service,
    get_salary_report_service
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



# HR REPORTS & STATISTICS

@router.get("/hr/reports/employees")
def employee_report(
    current_user=Depends(require_role("Admin", "HR"))
):
    return get_employee_report_service()


@router.get("/hr/reports/departments")
def department_report(
    current_user=Depends(require_role("Admin", "HR"))
):
    return get_department_report_service()


@router.get("/hr/reports/attendance")
def attendance_report(
    current_user=Depends(require_role("Admin", "HR"))
):
    return get_attendance_report_service()


@router.get("/hr/reports/leave")
def leave_report(
    current_user=Depends(require_role("Admin", "HR"))
):
    return get_leave_report_service()


@router.get("/hr/reports/performance")
def performance_report(
    current_user=Depends(require_role("Admin", "HR"))
):
    return get_performance_report_service()


@router.get("/hr/reports/salary")
def salary_report(
    current_user=Depends(require_role("Admin", "HR"))
):
    return get_salary_report_service()
