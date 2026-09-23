from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from jose import jwt

from database import connection
from security.jwt_handler import SECRET_KEY, ALGORITHM


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user_id = payload.get("user_id")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token"
        )

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            user_id,
            username,
            role,
            employee_id,
            status
        FROM users
        WHERE user_id = %s
    """, (user_id,))

    user = cursor.fetchone()

    cursor.close()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User account not found"
        )

    if user["status"] != "Active":
        raise HTTPException(
            status_code=401,
            detail="User account is inactive"
        )

    return user