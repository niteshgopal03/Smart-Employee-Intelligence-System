from database import connection
from datetime import date, time
import calendar


def format_time(value):

    if value is None:
        return None

    if isinstance(value, time):
        return value.strftime("%H:%M:%S")

    if isinstance(value, int):
        hours = value // 3600
        minutes = (value % 3600) // 60
        seconds = value % 60

        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    return str(value)


def mark_attendance_service(attendance, department_id=None):

    cursor = connection.cursor(dictionary=True)

    
    # Check employee exists
    
    cursor.execute("""
        SELECT employee_id, status, department_id
        FROM employees
        WHERE employee_id = %s
    """, (attendance.employee_id,))

    employee = cursor.fetchone()

    if not employee:
        cursor.close()
        return {
            "message": "Employee not found"
        }

    
    # HR department restriction
    
    if (
        department_id is not None
        and employee["department_id"] != department_id
    ):
        cursor.close()
        return {
            "message": "You can only manage attendance for your department"
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


def update_attendance_service(
    attendance_id: int,
    attendance,
    department_id=None
):

    cursor = connection.cursor(dictionary=True)

    
    # Get existing attendance and employee department
    
    cursor.execute("""
        SELECT
            a.attendance_id,
            a.employee_id,
            e.department_id
        FROM attendance a
        JOIN employees e
            ON a.employee_id = e.employee_id
        WHERE a.attendance_id = %s
    """, (attendance_id,))

    existing = cursor.fetchone()

    if not existing:
        cursor.close()
        return {
            "message": "Attendance record not found"
        }

   
    # HR department restriction
    
    if (
        department_id is not None
        and existing["department_id"] != department_id
    ):
        cursor.close()
        return {
            "message": "You can only manage attendance for your department"
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


def get_employee_attendance_service(
    employee_id: str,
    department_id=None
):

    cursor = connection.cursor(dictionary=True)

    
    if department_id is not None:

        cursor.execute("""
            SELECT employee_id
            FROM employees
            WHERE employee_id = %s
            AND department_id = %s
        """, (
            employee_id,
            department_id
        ))

        employee = cursor.fetchone()

        if not employee:
            cursor.close()
            return []

    
    # Get attendance
    
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

    for record in records:

        record["check_in"] = format_time(
            record["check_in"]
        )

        record["check_out"] = format_time(
            record["check_out"]
        )

    return records


def get_all_attendance_service(department_id=None):

    cursor = connection.cursor(dictionary=True)

    
    if department_id is None:

        cursor.execute("""
            SELECT
                a.attendance_id,
                a.employee_id,
                e.first_name,
                e.last_name,
                e.department_id,
                a.attendance_date,
                a.check_in,
                a.check_out,
                a.status
            FROM attendance a
            JOIN employees e
                ON a.employee_id = e.employee_id
            ORDER BY a.attendance_date DESC
        """)

    else:

        cursor.execute("""
            SELECT
                a.attendance_id,
                a.employee_id,
                e.first_name,
                e.last_name,
                e.department_id,
                a.attendance_date,
                a.check_in,
                a.check_out,
                a.status
            FROM attendance a
            JOIN employees e
                ON a.employee_id = e.employee_id
            WHERE e.department_id = %s
            ORDER BY a.attendance_date DESC
        """, (department_id,))

    records = cursor.fetchall()

    cursor.close()

    for record in records:

        record["check_in"] = format_time(
            record["check_in"]
        )

        record["check_out"] = format_time(
            record["check_out"]
        )

    return records


def get_attendance_percentage_service(
    employee_id: str,
    department_id=None
):

    cursor = connection.cursor(dictionary=True)

    
    if department_id is not None:

        cursor.execute("""
            SELECT employee_id
            FROM employees
            WHERE employee_id = %s
            AND department_id = %s
        """, (
            employee_id,
            department_id
        ))

        employee = cursor.fetchone()

        if not employee:
            cursor.close()
            return {
                "message": "Employee not found in your department"
            }

    
    # Calculate percentage
    
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


def get_my_monthly_attendance_service(
    employee_id: str,
    month: int,
    year: int
):

    if month < 1 or month > 12:
        return {
            "message": "Month must be between 1 and 12"
        }

    if year < 2000 or year > 2100:
        return {
            "message": "Invalid year"
        }

    last_day = calendar.monthrange(year, month)[1]

    start_date = date(year, month, 1)
    end_date = date(year, month, last_day)

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            attendance_date,
            check_in,
            check_out,
            status
        FROM attendance
        WHERE employee_id = %s
          AND attendance_date BETWEEN %s AND %s
        ORDER BY attendance_date ASC
    """, (
        employee_id,
        start_date,
        end_date
    ))

    records = cursor.fetchall()

    cursor.close()

    present_count = 0
    absent_count = 0
    leave_count = 0

    attendance = []

    for record in records:

        status = record["status"]

        if status == "Present":
            present_count += 1

        elif status == "Absent":
            absent_count += 1

        elif status == "Leave":
            leave_count += 1

        attendance.append({
            "date": record["attendance_date"],
            "status": status,
            "check_in": format_time(
                record["check_in"]
            ),
            "check_out": format_time(
                record["check_out"]
            )
        })

    return {
        "employee_id": employee_id,
        "month": month,
        "year": year,
        "summary": {
            "present": present_count,
            "absent": absent_count,
            "leave": leave_count
        },
        "attendance": attendance
    }


def get_attendance_dashboard_service(
    department_id=None
):

    cursor = connection.cursor(dictionary=True)

    
    # Overall summary
    
    if department_id is None:

        cursor.execute("""
            SELECT
                COUNT(*) AS total_records,
                SUM(
                    CASE
                        WHEN status = 'Present'
                        THEN 1 ELSE 0
                    END
                ) AS present_count,
                SUM(
                    CASE
                        WHEN status = 'Absent'
                        THEN 1 ELSE 0
                    END
                ) AS absent_count,
                SUM(
                    CASE
                        WHEN status = 'Leave'
                        THEN 1 ELSE 0
                    END
                ) AS leave_count
            FROM attendance
        """)

    else:

        cursor.execute("""
            SELECT
                COUNT(*) AS total_records,
                SUM(
                    CASE
                        WHEN a.status = 'Present'
                        THEN 1 ELSE 0
                    END
                ) AS present_count,
                SUM(
                    CASE
                        WHEN a.status = 'Absent'
                        THEN 1 ELSE 0
                    END
                ) AS absent_count,
                SUM(
                    CASE
                        WHEN a.status = 'Leave'
                        THEN 1 ELSE 0
                    END
                ) AS leave_count
            FROM attendance a
            JOIN employees e
                ON a.employee_id = e.employee_id
            WHERE e.department_id = %s
        """, (department_id,))

    summary = cursor.fetchone()

    
    # Employee-wise attendance
    
    if department_id is None:

        cursor.execute("""
            SELECT
                a.employee_id,
                e.first_name,
                e.last_name,
                COUNT(*) AS total_days,
                SUM(
                    CASE
                        WHEN a.status = 'Present'
                        THEN 1 ELSE 0
                    END
                ) AS present_days,
                SUM(
                    CASE
                        WHEN a.status = 'Absent'
                        THEN 1 ELSE 0
                    END
                ) AS absent_days,
                SUM(
                    CASE
                        WHEN a.status = 'Leave'
                        THEN 1 ELSE 0
                    END
                ) AS leave_days
            FROM attendance a
            JOIN employees e
                ON a.employee_id = e.employee_id
            GROUP BY
                a.employee_id,
                e.first_name,
                e.last_name
            ORDER BY
                e.first_name ASC,
                e.last_name ASC
        """)

    else:

        cursor.execute("""
            SELECT
                a.employee_id,
                e.first_name,
                e.last_name,
                COUNT(*) AS total_days,
                SUM(
                    CASE
                        WHEN a.status = 'Present'
                        THEN 1 ELSE 0
                    END
                ) AS present_days,
                SUM(
                    CASE
                        WHEN a.status = 'Absent'
                        THEN 1 ELSE 0
                    END
                ) AS absent_days,
                SUM(
                    CASE
                        WHEN a.status = 'Leave'
                        THEN 1 ELSE 0
                    END
                ) AS leave_days
            FROM attendance a
            JOIN employees e
                ON a.employee_id = e.employee_id
            WHERE e.department_id = %s
            GROUP BY
                a.employee_id,
                e.first_name,
                e.last_name
            ORDER BY
                e.first_name ASC,
                e.last_name ASC
        """, (department_id,))

    employees = cursor.fetchall()

    cursor.close()

    for employee in employees:

        total_days = employee["total_days"]

        if total_days and total_days > 0:
            employee["attendance_percentage"] = round(
                (
                    employee["present_days"]
                    / total_days
                ) * 100,
                2
            )
        else:
            employee["attendance_percentage"] = 0

    return {
        "summary": {
            "total_records": summary["total_records"] or 0,
            "present": summary["present_count"] or 0,
            "absent": summary["absent_count"] or 0,
            "leave": summary["leave_count"] or 0
        },
        "employees": employees
    }