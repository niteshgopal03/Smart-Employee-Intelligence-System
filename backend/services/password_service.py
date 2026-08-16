from fastapi import HTTPException

from database import connection

from security.password import (
    verify_password,
    hash_password
)


def change_password_service(current_user, password_data):

    employee_id = current_user["employee_id"]

    cursor = connection.cursor(dictionary=True)

    # Find logged-in user's account
    cursor.execute(
        """
        SELECT user_id, password_hash, status
        FROM users
        WHERE employee_id = %s
        AND status = 'Active'
        """,
        (employee_id,)
    )

    db_user = cursor.fetchone()

    if db_user is None:
        cursor.close()

        raise HTTPException(
            status_code=404,
            detail="User account not found"
        )

    # Verify old password
    if not verify_password(
        password_data.old_password,
        db_user["password_hash"]
    ):
        cursor.close()

        raise HTTPException(
            status_code=400,
            detail="Old password is incorrect"
        )

    # Check new password confirmation
    if password_data.new_password != password_data.confirm_password:
        cursor.close()

        raise HTTPException(
            status_code=400,
            detail="New passwords do not match"
        )

    #Avoid  same password
    if verify_password(
        password_data.new_password,
        db_user["password_hash"]
    ):
        cursor.close()

        raise HTTPException(
            status_code=400,
            detail="New password must be different from old password"
        )


    new_password_hash = hash_password(
        password_data.new_password
    )

    # Update password
    cursor.execute(
        """
        UPDATE users
        SET password_hash = %s
        WHERE user_id = %s
        """,
        (
            new_password_hash,
            db_user["user_id"]
        )
    )

    connection.commit()
    cursor.close()

    return {
        "message": "Password changed successfully"
    }