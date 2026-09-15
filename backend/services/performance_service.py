from fastapi import HTTPException

from database import connection


def update_manager_rating(
    employee_id: str,
    manager_rating: float
):

    cursor = connection.cursor(dictionary=True)

    # Check employee
    cursor.execute(
        """
        SELECT employee_id, first_name, last_name
        FROM employees
        WHERE employee_id=%s
        AND status='Active'
        """,
        (employee_id,)
    )

    employee = cursor.fetchone()

    if employee is None:

        cursor.close()

        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    # Update rating
    cursor.execute(
        """
        UPDATE employees
        SET manager_rating=%s
        WHERE employee_id=%s
        """,
        (manager_rating, employee_id)
    )

    connection.commit()

    cursor.close()

    return {
        "message": "Manager rating updated successfully",
        "employee_id": employee_id,
        "employee_name": (
            employee["first_name"]
            + " "
            + employee["last_name"]
        ),
        "manager_rating": manager_rating
    }


def get_manager_rating(employee_id: str):

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            employee_id,
            first_name,
            last_name,
            manager_rating
        FROM employees
        WHERE employee_id=%s
        """,
        (employee_id,)
    )

    employee = cursor.fetchone()

    cursor.close()

    if employee is None:

        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return {
        "employee_id": employee["employee_id"],
        "employee_name": (
            employee["first_name"]
            + " "
            + employee["last_name"]
        ),
        "manager_rating": employee["manager_rating"]
    }