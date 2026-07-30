from fastapi import HTTPException
from database import connection
from models.employee import Login
from security.password import verify_password
from security.jwt_handler import create_access_token


def login_service(login_data: Login):

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username=%s
        """,
        (login_data.username,)
    )

    user = cursor.fetchone()

    if user is None:

        cursor.close()

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(
        login_data.password,
        user["password_hash"]
    ):

        cursor.close()

        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    access_token = create_access_token(
        {
            "employee_id": user["employee_id"],
            "role": user["role"]
        }
    )

    cursor.close()

    return {
        "message": "Login Successful",
        "access_token": access_token,
        "token_type": "Bearer",
        "role": user["role"],
        "employee_id": user["employee_id"]
    }