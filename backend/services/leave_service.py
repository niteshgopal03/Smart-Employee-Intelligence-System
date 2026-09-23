from database import connection


def calculate_leave_days(from_date, to_date):
    return (to_date - from_date).days + 1


def apply_leave_service(employee_id: str, leave):

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT employee_id, status, leave_balance
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

    if leave.to_date < leave.from_date:
        cursor.close()
        return {
            "message": "To date cannot be before from date"
        }

    leave_days = calculate_leave_days(
        leave.from_date,
        leave.to_date
    )

    cursor.execute(
        """
        SELECT leave_id
        FROM leave_requests
        WHERE employee_id = %s
          AND status IN ('Pending', 'Approved')
          AND from_date <= %s
          AND to_date >= %s
        LIMIT 1
        """,
        (
            employee_id,
            leave.to_date,
            leave.from_date
        )
    )

    overlapping_leave = cursor.fetchone()

    if overlapping_leave is not None:
        cursor.close()
        return {
            "message": (
                "Leave request overlaps with an existing "
                "pending or approved leave"
            ),
            "existing_leave_id": overlapping_leave["leave_id"]
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
        "leave_days": leave_days,
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

    for leave in leaves:
        leave["leave_days"] = calculate_leave_days(
            leave["from_date"],
            leave["to_date"]
        )

    cursor.close()

    return leaves


def get_all_leave_requests_service(department_id=None):

    cursor = connection.cursor(dictionary=True)

    if department_id is None:

        cursor.execute(
            """
            SELECT
                l.leave_id,
                l.employee_id,
                e.first_name,
                e.last_name,
                e.department_id,
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

    else:

        cursor.execute(
            """
            SELECT
                l.leave_id,
                l.employee_id,
                e.first_name,
                e.last_name,
                e.department_id,
                l.from_date,
                l.to_date,
                l.reason,
                l.status,
                l.applied_date
            FROM leave_requests l
            JOIN employees e
                ON l.employee_id = e.employee_id
            WHERE e.department_id = %s
            ORDER BY l.applied_date DESC
            """,
            (department_id,)
        )

    leaves = cursor.fetchall()

    for leave in leaves:
        leave["leave_days"] = calculate_leave_days(
            leave["from_date"],
            leave["to_date"]
        )

    cursor.close()

    return leaves


def approve_leave_service(
    leave_id: int,
    department_id=None
):

    cursor = connection.cursor(dictionary=True)

    try:

        
        # Get leave request
        
        
        if department_id is None:

            cursor.execute(
                """
                SELECT
                    l.leave_id,
                    l.employee_id,
                    l.from_date,
                    l.to_date,
                    l.status
                FROM leave_requests l
                WHERE l.leave_id = %s
                FOR UPDATE
                """,
                (leave_id,)
            )

        else:

            cursor.execute(
                """
                SELECT
                    l.leave_id,
                    l.employee_id,
                    l.from_date,
                    l.to_date,
                    l.status
                FROM leave_requests l
                JOIN employees e
                    ON l.employee_id = e.employee_id
                WHERE l.leave_id = %s
                  AND e.department_id = %s
                FOR UPDATE
                """,
                (
                    leave_id,
                    department_id
                )
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

        leave_days = calculate_leave_days(
            leave["from_date"],
            leave["to_date"]
        )

        
        # Lock employee row
       
        cursor.execute(
            """
            SELECT
                employee_id,
                leave_balance
            FROM employees
            WHERE employee_id = %s
            FOR UPDATE
            """,
            (leave["employee_id"],)
        )

        employee = cursor.fetchone()

        if employee is None:
            connection.rollback()
            cursor.close()
            return {
                "message": "Employee not found"
            }

        current_balance = employee["leave_balance"] or 0

        
        if current_balance < leave_days:

            connection.rollback()
            cursor.close()

            return {
                "message": "Insufficient leave balance",
                "leave_id": leave_id,
                "required_days": leave_days,
                "available_days": current_balance
            }

        
        # Approve leave
        
        cursor.execute(
            """
            UPDATE leave_requests
            SET status = 'Approved'
            WHERE leave_id = %s
            """,
            (leave_id,)
        )

        
        # Deduct leave balance
        
        cursor.execute(
            """
            UPDATE employees
            SET leave_balance = leave_balance - %s
            WHERE employee_id = %s
            """,
            (
                leave_days,
                leave["employee_id"]
            )
        )

        connection.commit()

        cursor.close()

        return {
            "message": "Leave approved successfully",
            "leave_id": leave_id,
            "employee_id": leave["employee_id"],
            "leave_days": leave_days,
            "status": "Approved",
            "remaining_leave_balance": (
                current_balance - leave_days
            )
        }

    except Exception:

        connection.rollback()
        cursor.close()
        raise


def reject_leave_service(
    leave_id: int,
    department_id=None
):

    cursor = connection.cursor(dictionary=True)

    
    # Find leave request
    
    if department_id is None:

        cursor.execute(
            """
            SELECT
                leave_id,
                status
            FROM leave_requests
            WHERE leave_id = %s
            """,
            (leave_id,)
        )

    else:

        cursor.execute(
            """
            SELECT
                l.leave_id,
                l.status
            FROM leave_requests l
            JOIN employees e
                ON l.employee_id = e.employee_id
            WHERE l.leave_id = %s
              AND e.department_id = %s
            """,
            (
                leave_id,
                department_id
            )
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


def get_my_leave_service(employee_id: str):

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

    records = cursor.fetchall()

    cursor.close()

    leave_requests = []

    for record in records:

        leave_days = (
            record["to_date"] - record["from_date"]
        ).days + 1

        leave_requests.append({
            "leave_id": record["leave_id"],
            "employee_id": record["employee_id"],
            "from_date": record["from_date"],
            "to_date": record["to_date"],
            "leave_days": leave_days,
            "reason": record["reason"],
            "status": record["status"],
            "applied_date": record["applied_date"]
        })

    return {
        "employee_id": employee_id,
        "leave_requests": leave_requests
    }


def get_leave_dashboard_service(
    department_id=None
):

    cursor = connection.cursor(dictionary=True)

    
    # Summary
    
    if department_id is None:

        cursor.execute(
            """
            SELECT
                COUNT(*) AS total_requests,
                SUM(
                    CASE
                        WHEN status = 'Pending'
                        THEN 1 ELSE 0
                    END
                ) AS pending_requests,
                SUM(
                    CASE
                        WHEN status = 'Approved'
                        THEN 1 ELSE 0
                    END
                ) AS approved_requests,
                SUM(
                    CASE
                        WHEN status = 'Rejected'
                        THEN 1 ELSE 0
                    END
                ) AS rejected_requests
            FROM leave_requests
            """
        )

    else:

        cursor.execute(
            """
            SELECT
                COUNT(*) AS total_requests,
                SUM(
                    CASE
                        WHEN lr.status = 'Pending'
                        THEN 1 ELSE 0
                    END
                ) AS pending_requests,
                SUM(
                    CASE
                        WHEN lr.status = 'Approved'
                        THEN 1 ELSE 0
                    END
                ) AS approved_requests,
                SUM(
                    CASE
                        WHEN lr.status = 'Rejected'
                        THEN 1 ELSE 0
                    END
                ) AS rejected_requests
            FROM leave_requests lr
            JOIN employees e
                ON lr.employee_id = e.employee_id
            WHERE e.department_id = %s
            """,
            (department_id,)
        )

    summary = cursor.fetchone()

    
    # Leave requests

    if department_id is None:

        cursor.execute(
            """
            SELECT
                lr.leave_id,
                lr.employee_id,
                e.first_name,
                e.last_name,
                e.department_id,
                lr.from_date,
                lr.to_date,
                lr.reason,
                lr.status,
                lr.applied_date
            FROM leave_requests lr
            JOIN employees e
                ON lr.employee_id = e.employee_id
            ORDER BY lr.applied_date DESC
            """
        )

    else:

        cursor.execute(
            """
            SELECT
                lr.leave_id,
                lr.employee_id,
                e.first_name,
                e.last_name,
                e.department_id,
                lr.from_date,
                lr.to_date,
                lr.reason,
                lr.status,
                lr.applied_date
            FROM leave_requests lr
            JOIN employees e
                ON lr.employee_id = e.employee_id
            WHERE e.department_id = %s
            ORDER BY lr.applied_date DESC
            """,
            (department_id,)
        )

    requests = cursor.fetchall()

    cursor.close()

    leave_requests = []

    for record in requests:

        leave_days = (
            record["to_date"] - record["from_date"]
        ).days + 1

        leave_requests.append({
            "leave_id": record["leave_id"],
            "employee_id": record["employee_id"],
            "first_name": record["first_name"],
            "last_name": record["last_name"],
            "department_id": record["department_id"],
            "from_date": record["from_date"],
            "to_date": record["to_date"],
            "leave_days": leave_days,
            "reason": record["reason"],
            "status": record["status"],
            "applied_date": record["applied_date"]
        })

    return {
        "summary": {
            "total_requests": summary["total_requests"] or 0,
            "pending": summary["pending_requests"] or 0,
            "approved": summary["approved_requests"] or 0,
            "rejected": summary["rejected_requests"] or 0
        },
        "leave_requests": leave_requests
    }