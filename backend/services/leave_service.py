from database import connection


def apply_leave_service(employee_id: str, leave):

    cursor = connection.cursor(dictionary=True)

    # Check employee
    cursor.execute(
        """
        SELECT employee_id, status
        FROM employees
        WHERE employee_id = %s
        """,
        (employee_id,)
    )

    employee = cursor.fetchone()

    if employee is None:
        cursor.close()
        return {
            "message": "Employee not found"
        }

    if employee["status"] == "Resigned":
        cursor.close()
        return {
            "message": "Resigned employee cannot apply for leave"
        }

    # Validate dates
    if leave.to_date < leave.from_date:
        cursor.close()
        return {
            "message": "To date cannot be before from date"
        }


    cursor.execute(
        """
        INSERT INTO leave_requests (
            employee_id,
            from_date,
            to_date,
            reason
        )
        VALUES (%s, %s, %s, %s)
        """,
        (
            employee_id,
            leave.from_date,
            leave.to_date,
            leave.reason
        )
    )

    connection.commit()

    leave_id = cursor.lastrowid

    cursor.close()

    return {
        "message": "Leave request submitted successfully",
        "leave_id": leave_id,
        "employee_id": employee_id,
        "status": "Pending"
    }


def get_my_leave_requests_service(employee_id: str):

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            leave_id,
            employee_id,
            from_date,
            to_date,
            reason,
            status,
            applied_date
        FROM leave_requests
        WHERE employee_id = %s
        ORDER BY applied_date DESC
        """,
        (employee_id,)
    )

    leaves = cursor.fetchall()

    cursor.close()

    return leaves


def get_all_leave_requests_service():

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            l.leave_id,
            l.employee_id,
            e.first_name,
            e.last_name,
            l.from_date,
            l.to_date,
            l.reason,
            l.status,
            l.applied_date
        FROM leave_requests l
        JOIN employees e
            ON l.employee_id = e.employee_id
        ORDER BY l.applied_date DESC
        """
    )

    leaves = cursor.fetchall()

    cursor.close()

    return leaves


def approve_leave_service(leave_id: int):

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT leave_id, status
        FROM leave_requests
        WHERE leave_id = %s
        """,
        (leave_id,)
    )

    leave = cursor.fetchone()

    if leave is None:
        cursor.close()
        return {
            "message": "Leave request not found"
        }

    if leave["status"] != "Pending":
        cursor.close()
        return {
            "message": "Leave request has already been processed"
        }

    cursor.execute(
        """
        UPDATE leave_requests
        SET status = 'Approved'
        WHERE leave_id = %s
        """,
        (leave_id,)
    )

    connection.commit()
    cursor.close()

    return {
        "message": "Leave approved successfully",
        "leave_id": leave_id,
        "status": "Approved"
    }


def reject_leave_service(leave_id: int):

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT leave_id, status
        FROM leave_requests
        WHERE leave_id = %s
        """,
        (leave_id,)
    )

    leave = cursor.fetchone()

    if leave is None:
        cursor.close()
        return {
            "message": "Leave request not found"
        }

    if leave["status"] != "Pending":
        cursor.close()
        return {
            "message": "Leave request has already been processed"
        }

    cursor.execute(
        """
        UPDATE leave_requests
        SET status = 'Rejected'
        WHERE leave_id = %s
        """,
        (leave_id,)
    )

    connection.commit()
    cursor.close()

    return {
        "message": "Leave rejected successfully",
        "leave_id": leave_id,
        "status": "Rejected"
    }