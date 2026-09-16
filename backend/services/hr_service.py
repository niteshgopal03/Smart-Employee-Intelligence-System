from database import connection
from security.password import hash_password


def generate_hr_id(department_id: int):

    cursor = connection.cursor()

    # Check whether this department already has HR
    cursor.execute("""
        SELECT employee_id
        FROM employees
        WHERE department_id = %s
        AND employee_id LIKE 'HR%'
        LIMIT 1
    """, (department_id,))

    existing_hr = cursor.fetchone()

    if existing_hr:
        cursor.close()
        return None


    hr_id = f"HR{department_id}001"

    cursor.close()

    return hr_id


def add_hr_service(hr):

    cursor = connection.cursor(dictionary=True)

    # Check department exists
    cursor.execute("""
        SELECT department_id, department_name
        FROM departments
        WHERE department_id = %s
    """, (hr.department_id,))

    department = cursor.fetchone()

    if not department:
        cursor.close()
        return {
            "message": "Department not found"
        }

    
    cursor.execute("""
        SELECT employee_id
        FROM employees
        WHERE department_id = %s
        AND employee_id LIKE 'HR%'
        AND status = 'Active'
    """, (hr.department_id,))

    existing_hr = cursor.fetchone()

    if existing_hr:
        cursor.close()
        return {
            "message": "This department already has an active HR",
            "hr_id": existing_hr["employee_id"]
        }

    # Generate department-based HR ID
    hr_id = f"HR{hr.department_id}001"

    cursor.execute("""
        SELECT employee_id
        FROM employees
        WHERE employee_id = %s
    """, (hr_id,))

    existing_employee = cursor.fetchone()

    if existing_employee:
        cursor.close()
        return {
            "message": f"HR ID {hr_id} already exists"
        }

    # Insert HR into employees
    cursor.execute("""
        INSERT INTO employees (
            employee_id,
            first_name,
            last_name,
            email,
            phone,
            gender,
            dob,
            joining_date,
            department_id,
            designation,
            education,
            skills,
            base_salary,
            status
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Active'
        )
    """, (
        hr_id,
        hr.first_name,
        hr.last_name,
        hr.email,
        hr.phone,
        hr.gender,
        hr.dob,
        hr.joining_date,
        hr.department_id,
        hr.designation,
        hr.education,
        hr.skills,
        hr.base_salary
    ))

    default_password = "Welcome@123"
    password_hash = hash_password(default_password)

    # Create HR login
    cursor.execute("""
        INSERT INTO users (
            username,
            password_hash,
            role,
            employee_id,
            status
        )
        VALUES (
            %s, %s, 'HR', %s, 'Active'
        )
    """, (
        hr_id,
        password_hash,
        hr_id
    ))

    connection.commit()
    cursor.close()

    return {
        "message": "HR added successfully",
        "hr_id": hr_id,
        "username": hr_id,
        "temporary_password": default_password,
        "department_id": hr.department_id,
        "department_name": department["department_name"]
    }


def delete_hr_service(employee_id: str):

    cursor = connection.cursor(dictionary=True)

    # Check HR
    cursor.execute("""
        SELECT employee_id, department_id
        FROM employees
        WHERE employee_id = %s
        AND employee_id LIKE 'HR%'
    """, (employee_id,))

    hr = cursor.fetchone()

    if not hr:
        cursor.close()
        return {
            "message": "HR not found"
        }

    department_id = hr["department_id"]

    # Delete HR login first
    cursor.execute("""
        DELETE FROM users
        WHERE employee_id = %s
        AND role = 'HR'
    """, (employee_id,))

    # Delete only the HR employee record
    cursor.execute("""
        DELETE FROM employees
        WHERE employee_id = %s
        AND employee_id LIKE 'HR%'
    """, (employee_id,))

    connection.commit()
    cursor.close()

    return {
        "message": "HR deleted successfully",
        "deleted_hr_id": employee_id,
        "department_id": department_id,
        "employees_in_department": "unchanged"
    }


#TOTAL DASHBOARD

def get_employee_report_service():

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            COUNT(*) AS total_employees,
            SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) AS active_employees,
            SUM(CASE WHEN status = 'Resigned' THEN 1 ELSE 0 END) AS resigned_employees
        FROM employees
    """)

    summary = cursor.fetchone()

    cursor.close()

    return {
        "total_employees": summary["total_employees"] or 0,
        "active_employees": summary["active_employees"] or 0,
        "resigned_employees": summary["resigned_employees"] or 0
    }


def get_department_report_service():

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            d.department_id,
            d.department_name,
            COUNT(e.employee_id) AS total_employees,
            SUM(
                CASE
                    WHEN e.status = 'Active' THEN 1
                    ELSE 0
                END
            ) AS active_employees,
            SUM(
                CASE
                    WHEN e.status = 'Resigned' THEN 1
                    ELSE 0
                END
            ) AS resigned_employees
        FROM departments d
        LEFT JOIN employees e
            ON d.department_id = e.department_id
        GROUP BY
            d.department_id,
            d.department_name
        ORDER BY d.department_name ASC
    """)

    departments = cursor.fetchall()

    cursor.close()

    for department in departments:
        department["total_employees"] = (
            department["total_employees"] or 0
        )
        department["active_employees"] = (
            department["active_employees"] or 0
        )
        department["resigned_employees"] = (
            department["resigned_employees"] or 0
        )

    return {
        "departments": departments
    }


def get_attendance_report_service():

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            COUNT(*) AS total_records,
            SUM(
                CASE
                    WHEN status = 'Present' THEN 1
                    ELSE 0
                END
            ) AS present,
            SUM(
                CASE
                    WHEN status = 'Absent' THEN 1
                    ELSE 0
                END
            ) AS absent,
            SUM(
                CASE
                    WHEN status = 'Leave' THEN 1
                    ELSE 0
                END
            ) AS leave
        FROM attendance
    """)

    summary = cursor.fetchone()

    cursor.close()

    total_records = summary["total_records"] or 0
    present = summary["present"] or 0

    if total_records > 0:
        attendance_percentage = round(
            (present / total_records) * 100,
            2
        )
    else:
        attendance_percentage = 0

    return {
        "total_records": total_records,
        "present": present,
        "absent": summary["absent"] or 0,
        "leave": summary["leave"] or 0,
        "attendance_percentage": attendance_percentage
    }


def get_leave_report_service():

    cursor = connection.cursor(dictionary=True)

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

    summary = cursor.fetchone()

    cursor.execute("""
        SELECT
            COUNT(*) AS approved_requests,
            COALESCE(
                SUM(
                    DATEDIFF(to_date, from_date) + 1
                ),
                0
            ) AS approved_leave_days
        FROM leave_requests
        WHERE status = 'Approved'
    """)

    approved_summary = cursor.fetchone()

    cursor.close()

    return {
        "total_requests": summary["total_requests"] or 0,
        "pending": summary["pending"] or 0,
        "approved": summary["approved"] or 0,
        "rejected": summary["rejected"] or 0,
        "approved_leave_days": (
            approved_summary["approved_leave_days"] or 0
        )
    }


def get_performance_report_service():

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            COUNT(manager_rating) AS rated_employees,
            ROUND(AVG(manager_rating), 2) AS average_rating,
            MAX(manager_rating) AS highest_rating,
            MIN(manager_rating) AS lowest_rating
        FROM employees
        WHERE manager_rating IS NOT NULL
    """)

    summary = cursor.fetchone()

    cursor.execute("""
        SELECT
            e.department_id,
            d.department_name,
            COUNT(e.employee_id) AS rated_employees,
            ROUND(AVG(e.manager_rating), 2) AS average_rating
        FROM employees e
        LEFT JOIN departments d
            ON e.department_id = d.department_id
        WHERE e.manager_rating IS NOT NULL
        GROUP BY
            e.department_id,
            d.department_name
        ORDER BY average_rating DESC
    """)

    departments = cursor.fetchall()

    cursor.close()

    return {
        "summary": {
            "rated_employees": summary["rated_employees"] or 0,
            "average_rating": summary["average_rating"] or 0,
            "highest_rating": summary["highest_rating"] or 0,
            "lowest_rating": summary["lowest_rating"] or 0
        },
        "department_statistics": departments
    }


def get_salary_report_service():

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            COUNT(base_salary) AS employees_with_salary,
            ROUND(AVG(base_salary), 2) AS average_salary,
            MIN(base_salary) AS minimum_salary,
            MAX(base_salary) AS maximum_salary,
            ROUND(SUM(base_salary), 2) AS total_salary
        FROM employees
        WHERE base_salary IS NOT NULL
    """)

    summary = cursor.fetchone()

    cursor.execute("""
        SELECT
            d.department_id,
            d.department_name,
            COUNT(e.employee_id) AS employees,
            ROUND(AVG(e.base_salary), 2) AS average_salary,
            MIN(e.base_salary) AS minimum_salary,
            MAX(e.base_salary) AS maximum_salary
        FROM employees e
        LEFT JOIN departments d
            ON e.department_id = d.department_id
        WHERE e.base_salary IS NOT NULL
        GROUP BY
            d.department_id,
            d.department_name
        ORDER BY average_salary DESC
    """)

    departments = cursor.fetchall()

    cursor.close()

    return {
        "summary": {
            "employees_with_salary": (
                summary["employees_with_salary"] or 0
            ),
            "average_salary": summary["average_salary"] or 0,
            "minimum_salary": summary["minimum_salary"] or 0,
            "maximum_salary": summary["maximum_salary"] or 0,
            "total_salary": summary["total_salary"] or 0
        },
        "department_statistics": departments
    }
