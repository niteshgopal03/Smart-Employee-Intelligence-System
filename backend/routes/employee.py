from fastapi import APIRouter, Depends

from models.employee import Employee

from services.employee_service import (
    add_employee_service,
    get_all_employees_service,
    get_employee_service,
    update_employee_service,
    delete_employee_service,
    get_my_employee_service,
    search_employees_service,
)

from services.hr_service import get_hr_department_id
from security.role_checker import require_role


router = APIRouter()


@router.post("/employee/add")
def add_employee(
    employee: Employee,
    current_user=Depends(require_role("Admin", "HR"))
):
    hr_department_id = None

    if current_user["role"].lower() == "hr":
        hr_department_id = get_hr_department_id(current_user)

    return add_employee_service(
        employee,
        hr_department_id=hr_department_id
    )


@router.get("/employees")
def get_all_employees(
    current_user=Depends(require_role("Admin", "HR"))
):
    hr_department_id = None

    if current_user["role"].lower() == "hr":
        hr_department_id = get_hr_department_id(current_user)

    return get_all_employees_service(
        hr_department_id=hr_department_id
    )


@router.get("/employees/search")
def search_employees(
    search: str,
    current_user=Depends(require_role("Admin", "HR"))
):
    hr_department_id = None

    if current_user["role"].lower() == "hr":
        hr_department_id = get_hr_department_id(current_user)

    return search_employees_service(
    search=search,
    hr_department_id=hr_department_id,
    exclude_employee_id=current_user.get("employee_id")
)


@router.get("/employee/me")
def get_my_employee(
    current_user=Depends(require_role("Employee"))
):
    employee_id = current_user["employee_id"]

    return get_my_employee_service(employee_id)


@router.get("/employee/{employee_id}")
def get_employee(
    employee_id: str,
    current_user=Depends(require_role("Admin", "HR"))
):
    hr_department_id = None

    if current_user["role"].lower() == "hr":
        hr_department_id = get_hr_department_id(current_user)

    return get_employee_service(
        employee_id,
        hr_department_id=hr_department_id
    )


@router.put("/employee/update/{employee_id}")
def update_employee(
    employee_id: str,
    employee: Employee,
    current_user=Depends(require_role("Admin", "HR"))
):
    hr_department_id = None

    if current_user["role"].lower() == "hr":
        hr_department_id = get_hr_department_id(current_user)

    return update_employee_service(
        employee_id,
        employee,
        hr_department_id=hr_department_id
    )


@router.delete("/employee/delete/{employee_id}")
def delete_employee(
    employee_id: str,
    current_user=Depends(require_role("Admin", "HR"))
):
    hr_department_id = None

    if current_user["role"].lower() == "hr":
        hr_department_id = get_hr_department_id(current_user)

    return delete_employee_service(
        employee_id,
        hr_department_id=hr_department_id
    )