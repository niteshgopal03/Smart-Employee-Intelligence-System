from database import connection


def mark_attendance_service(attendance):

    cursor = connection.cursor(dictionary=True)

    # Check employee exists
    cursor.execute("""
        SELECT employee_id, status
        FROM employees
        WHERE employee_id = %s
    """, (attendance.employee_id,))

    employee = cursor.fetchone()

    if not employee:
        cursor.close()
        return {
            "message": "Employee not found"
        }

    if employee["status"] == "Resigned":
        cursor.close()
        return {
            "message": "Cannot mark attendance for a resigned employee"
        }

    # Check duplicate attendance
    cursor.execute("""
        SELECT attendance_id
        FROM attendance
        WHERE employee_id = %s
        AND attendance_date = %s
    """, (
        attendance.employee_id,
        attendance.attendance_date
    ))

    existing = cursor.fetchone()

    if existing:
        cursor.close()
        return {
            "message": "Attendance already exists for this date"
        }

    # Insert attendance
    cursor.execute("""
        INSERT INTO attendance (
            employee_id,
            attendance_date,
            check_in,
            check_out,
            status
        )
        VALUES (%s, %s, %s, %s, %s)
    """, (
        attendance.employee_id,
        attendance.attendance_date,
        attendance.check_in,
        attendance.check_out,
        attendance.status
    ))

    connection.commit()
    cursor.close()

    return {
        "message": "Attendance marked successfully",
        "employee_id": attendance.employee_id,
        "attendance_date": attendance.attendance_date,
        "status": attendance.status
    }


def update_attendance_service(attendance_id: int, attendance):

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT attendance_id
        FROM attendance
        WHERE attendance_id = %s
    """, (attendance_id,))

    existing = cursor.fetchone()

    if not existing:
        cursor.close()
        return {
            "message": "Attendance record not found"
        }

    cursor.execute("""
        UPDATE attendance
        SET
            attendance_date = %s,
            check_in = %s,
            check_out = %s,
            status = %s
        WHERE attendance_id = %s
    """, (
        attendance.attendance_date,
        attendance.check_in,
        attendance.check_out,
        attendance.status,
        attendance_id
    ))

    connection.commit()
    cursor.close()

    return {
        "message": "Attendance updated successfully",
        "attendance_id": attendance_id
    }


def get_employee_attendance_service(employee_id: str):

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            attendance_id,
            employee_id,
            attendance_date,
            check_in,
            check_out,
            status
        FROM attendance
        WHERE employee_id = %s
        ORDER BY attendance_date DESC
    """, (employee_id,))

    records = cursor.fetchall()

    cursor.close()

    return records


def get_all_attendance_service():

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            a.attendance_id,
            a.employee_id,
            e.first_name,
            e.last_name,
            a.attendance_date,
            a.check_in,
            a.check_out,
            a.status
        FROM attendance a
        JOIN employees e
            ON a.employee_id = e.employee_id
        ORDER BY a.attendance_date DESC
    """)

    records = cursor.fetchall()

    cursor.close()

    return records


def get_attendance_percentage_service(employee_id: str):

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            COUNT(*) AS total_days,
            SUM(
                CASE
                    WHEN status = 'Present' THEN 1
                    ELSE 0
                END
            ) AS present_days
        FROM attendance
        WHERE employee_id = %s
    """, (employee_id,))

    result = cursor.fetchone()

    cursor.close()

    total_days = result["total_days"] or 0
    present_days = result["present_days"] or 0

    if total_days == 0:
        percentage = 0
    else:
        percentage = (present_days / total_days) * 100

    return {
        "employee_id": employee_id,
        "total_days": total_days,
        "present_days": present_days,
        "attendance_percentage": round(percentage, 2)
    }