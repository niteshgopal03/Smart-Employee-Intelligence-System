from fastapi import APIRouter
from models.employee import Employee

from services.employee_service import (
    add_employee_service,
    get_all_employees_service,
    get_employee_service,
    update_employee_service,
    delete_employee_service
)

router = APIRouter()


@router.post("/employee/add")
def add_employee(employee: Employee):

    return add_employee_service(employee)


@router.get("/employees")
def get_all_employees():

    return get_all_employees_service()


@router.get("/employee/{employee_id}")
def get_employee(employee_id: str):

    return get_employee_service(employee_id)


@router.put("/employee/update/{employee_id}")
def update_employee(
    employee_id: str,
    employee: Employee
):

    return update_employee_service(
        employee_id,
        employee
    )


@router.delete("/employee/delete/{employee_id}")
def delete_employee(employee_id: str):

    return delete_employee_service(employee_id)