from database import connection
from models.employee import Employee
from security.password import hash_password


def add_employee_service(employee: Employee):

    cursor = connection.cursor()

    # Generate Employee ID 
    cursor.execute("SELECT COUNT(*) FROM employees")
    count = cursor.fetchone()[0]
    employee_id = f"EMP{1001 + count}"

    cursor.execute(
        """
        INSERT INTO employees
        (
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
            manager_rating,
            attendance_percentage,
            leave_balance,
            status
        )

        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s,%s,%s,%s
        )
        """,
        (
            employee_id,
            employee.first_name,
            employee.last_name,
            employee.email,
            employee.phone,
            employee.gender,
            employee.dob,
            employee.joining_date,
            employee.department_id,
            employee.designation,
            employee.education,
            employee.skills,
            employee.base_salary,
            employee.manager_rating,
            employee.attendance_percentage,
            employee.leave_balance,
            "Active"
        )
    )

    default_password = "Welcome@123"

    hashed_password = hash_password(default_password)

    cursor.execute(
        """
        INSERT INTO users
        (
            username,
            password_hash,
            role,
            employee_id
        )

        VALUES(%s,%s,%s,%s)
        """,
        (
            employee_id,
            hashed_password,
            "Employee",
            employee_id
        )
    )

    connection.commit()
    cursor.close()

    return {
        "message": "Employee added successfully",
        "employee_id": employee_id
    }


def get_all_employees_service():

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM employees
        WHERE status='Active'
        """
    )

    employees = cursor.fetchall()

    cursor.close()

    return employees


def get_employee_service(employee_id: str):

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM employees
        WHERE employee_id=%s
        """,
        (employee_id,)
    )

    employee = cursor.fetchone()

    cursor.close()

    return employee


def update_employee_service(employee_id: str, employee: Employee):

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE employees
        SET
            first_name=%s,
            last_name=%s,
            email=%s,
            phone=%s,
            gender=%s,
            dob=%s,
            joining_date=%s,
            department_id=%s,
            designation=%s,
            education=%s,
            skills=%s,
            base_salary=%s,
            manager_rating=%s,
            attendance_percentage=%s,
            leave_balance=%s
        WHERE employee_id=%s
        """,
        (
            employee.first_name,
            employee.last_name,
            employee.email,
            employee.phone,
            employee.gender,
            employee.dob,
            employee.joining_date,
            employee.department_id,
            employee.designation,
            employee.education,
            employee.skills,
            employee.base_salary,
            employee.manager_rating,
            employee.attendance_percentage,
            employee.leave_balance,
            employee_id
        )
    )

    connection.commit()

    cursor.close()

    return {
        "message": "Employee updated successfully"
    }


def delete_employee_service(employee_id: str):

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE employees
        SET status=%s
        WHERE employee_id=%s
        """,
        (
            "Resigned",
            employee_id
        )
    )

    connection.commit()

    cursor.close()

    return {
        "message": "Employee marked as resigned successfully"
    }