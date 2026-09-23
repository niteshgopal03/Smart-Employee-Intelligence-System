from fastapi import APIRouter, Depends

from models.change_password import ChangePassword
from services.password_service import change_password_service
from security.role_checker import require_role


router = APIRouter()


@router.put("/auth/change-password")
def change_password(
    password_data: ChangePassword,
    current_user=Depends(
        require_role("Admin", "HR", "Employee")
    )
):
    return change_password_service(
        current_user,
        password_data
    )


@router.put("/employee/me/password")
def change_my_password(
    password_data: ChangePassword,
    current_user=Depends(
        require_role("Employee")
    )
):
    return change_password_service(
        current_user,
        password_data
    )