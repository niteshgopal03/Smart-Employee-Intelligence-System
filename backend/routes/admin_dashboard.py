from fastapi import APIRouter, Depends

from database import connection
from security.role_checker import require_role


router = APIRouter()


@router.get("/dashboard/admin")
def get_admin_dashboard(
    current_user=Depends(require_role("Admin"))
):

    cursor = connection.cursor(dictionary=True)

    # Employee overview
    cursor.execute("""
        SELECT
            COUNT(*) AS total_employees,
            SUM(
                CASE
                    WHEN status = 'Active' THEN 1
                    ELSE 0
                END
            ) AS active_employees,
            SUM(
                CASE
                    WHEN status = 'Resigned' THEN 1
                    ELSE 0
                END
            ) AS resigned_employees
        FROM employees
    """)

    employee_overview = cursor.fetchone()

    # department-wise emp count
    cursor.execute("""
        SELECT
            d.department_name,
            COUNT(e.employee_id) AS employee_count
        FROM departments d
        LEFT JOIN employees e
            ON d.department_id = e.department_id
            AND e.status = 'Active'
        GROUP BY
            d.department_id,
            d.department_name
        ORDER BY employee_count DESC
    """)

    department_summary = cursor.fetchall()

    # Today's attendance
    cursor.execute("""
    SELECT
        COUNT(*) AS total,
        SUM(status = 'Present') AS present,
        SUM(status = 'Absent') AS absent,
        SUM(status = 'Leave') AS leave_count
    FROM attendance
    WHERE attendance_date = CURDATE()""")

    today_attendance = cursor.fetchone()

    # Leave request overview
    cursor.execute("""
        SELECT
            COUNT(*) AS total_requests,
            SUM(
                CASE
                    WHEN status = 'Pending' THEN 1
                    ELSE 0
                END
            ) AS pending,
            SUM(
                CASE
                    WHEN status = 'Approved' THEN 1
                    ELSE 0
                END
            ) AS approved,
            SUM(
                CASE
                    WHEN status = 'Rejected' THEN 1
                    ELSE 0
                END
            ) AS rejected
        FROM leave_requests
    """)

    leave_overview = cursor.fetchone()

    # User/account overview
    cursor.execute("""
        SELECT
            COUNT(*) AS total_users,
            SUM(
                CASE
                    WHEN role = 'Admin' THEN 1
                    ELSE 0
                END
            ) AS admin_users,
            SUM(
                CASE
                    WHEN role = 'HR' THEN 1
                    ELSE 0
                END
            ) AS hr_users,
            SUM(
                CASE
                    WHEN role = 'Employee' THEN 1
                    ELSE 0
                END
            ) AS employee_users,
            SUM(
                CASE
                    WHEN status = 'Active' THEN 1
                    ELSE 0
                END
            ) AS active_users
        FROM users
    """)

    user_overview = cursor.fetchone()

    # Salary overview
    cursor.execute("""
        SELECT
            COALESCE(SUM(base_salary), 0) AS total_salary,
            COALESCE(AVG(base_salary), 0) AS average_salary
        FROM employees
        WHERE status = 'Active'
    """)

    salary_overview = cursor.fetchone()

    cursor.close()

    return {
        "employee_overview": employee_overview,
        "department_summary": department_summary,
        "today_attendance": today_attendance,
        "leave_overview": leave_overview,
        "user_overview": user_overview,
        "salary_overview": salary_overview
    }