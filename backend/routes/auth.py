from fastapi import APIRouter
from models.employee import Login
from services.auth_service import login_service

router = APIRouter()


@router.post("/login")
def login(login_data: Login):

    return login_service(login_data)