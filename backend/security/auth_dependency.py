from fastapi import Header, HTTPException
from security.jwt_handler import verify_access_token


def get_current_user(authorization: str = Header(None)):

    if authorization is None:
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing"
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization format"
        )

    token = authorization.split(" ")[1]

    payload = verify_access_token(token)

    return payload