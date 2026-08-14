from fastapi import APIRouter

from models.user import UserLogin

from services.auth_service import login_service

router = APIRouter()


@router.post("/login")
def login(user: UserLogin):

    return login_service(user)