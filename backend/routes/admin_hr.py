from fastapi import APIRouter, Depends

from models.hr import HR
from models.department import (
    DepartmentCreate,
    DepartmentUpdate,
)

from security.role_checker import require_role

from services.hr_service import (
    add_hr_service,
    delete_hr_service,
    get_all_hr_service,
    get_all_departments_service,
    add_department_service,
    update_department_service,
    delete_department_service,
)

router = APIRouter()


@router.get("/admin/hr")
def get_all_hr(
    current_user=Depends(require_role("Admin"))
):
    return get_all_hr_service()


@router.post("/admin/hr/add")
def add_hr(
    hr: HR,
    current_user=Depends(require_role("Admin"))
):
    return add_hr_service(hr)


@router.delete("/admin/hr/delete/{employee_id}")
def delete_hr(
    employee_id: str,
    current_user=Depends(require_role("Admin"))
):
    return delete_hr_service(employee_id)



@router.get("/admin/departments")
def get_all_departments(
    current_user=Depends(require_role("Admin"))
):
    return get_all_departments_service()


@router.post("/admin/departments")
def add_department(
    department: DepartmentCreate,
    current_user=Depends(require_role("Admin"))
):
    return add_department_service(department)


@router.put("/admin/departments/{department_id}")
def update_department(
    department_id: int,
    department: DepartmentUpdate,
    current_user=Depends(require_role("Admin"))
):
    return update_department_service(
        department_id,
        department
    )


@router.delete("/admin/departments/{department_id}")
def delete_department(
    department_id: int,
    current_user=Depends(require_role("Admin"))
):
    return delete_department_service(
        department_id
    )