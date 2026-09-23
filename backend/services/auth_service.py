from database import connection

from models.user import UserLogin

from security.password import verify_password
from security.jwt_handler import create_access_token


def login_service(user: UserLogin):


   

    # HR / Employee Login

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username = %s
        AND status = 'Active'
        """,
        (user.username,)
    )

    db_user = cursor.fetchone()

    if db_user is None:

        cursor.close()

        return {
            "message": "Invalid Username or Inactive Account"
        }


    if not verify_password(
        user.password,
        db_user["password_hash"]
    ):

        cursor.close()

        return {
            "message": "Invalid Password"
        }

    # Update Last Login
    cursor.execute(
        """
        UPDATE users
        SET last_login = CURRENT_TIMESTAMP
        WHERE user_id = %s
        """,
        (db_user["user_id"],)
    )

    connection.commit()

    cursor.close()


    # Generate JWT

    access_token = create_access_token({
    "user_id": db_user["user_id"],
    "username": db_user["username"],
    "employee_id": db_user["employee_id"],
    "role": db_user["role"]
    })

    return {
        "message": "Login Successful",
        "access_token": access_token,
        "token_type": "Bearer",
        "employee_id": db_user["employee_id"],
        "role": db_user["role"]
    }