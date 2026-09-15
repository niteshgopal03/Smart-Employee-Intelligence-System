from database import connection
from models.employee import Employee
from security.password import hash_password


def generate_employee_id(department_id: int):

    cursor = connection.cursor()

    prefix = f"EMP{department_id}"

    cursor.execute("""
        SELECT employee_id
        FROM employees
        WHERE employee_id LIKE %s
        ORDER BY CAST(SUBSTRING(employee_id, 5) AS UNSIGNED) DESC
        LIMIT 1
    """, (prefix + "%",))

    result = cursor.fetchone()

    if not result:
        employee_id = f"{prefix}001"
    else:
        last_id = result[0]

        number = int(last_id[3:])

        employee_id = f"EMP{number + 1}"

    cursor.close()

    return employee_id



def add_employee_service(employee):

    cursor = connection.cursor(dictionary=True)

  
    cursor.execute("""
        SELECT department_id, department_name
        FROM departments
        WHERE department_id = %s
    """, (employee.department_id,))

    department = cursor.fetchone()

    if not department:
        cursor.close()
        return {
            "message": "Department not found"
        }

    employee_id = generate_employee_id(employee.department_id)

   
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
        employee.base_salary
    ))

    
    default_password = "Welcome@123"
    password_hash = hash_password(default_password)

    cursor.execute("""
        INSERT INTO users (
            username,
            password_hash,
            role,
            employee_id,
            status
        )
        VALUES (
            %s, %s, 'Employee', %s, 'Active'
        )
    """, (
        employee_id,
        password_hash,
        employee_id
    ))

    connection.commit()
    cursor.close()

    return {
        "message": "Employee added successfully",
        "employee_id": employee_id,
        "username": employee_id,
        "temporary_password": default_password,
        "department_id": employee.department_id,
        "department_name": department["department_name"]
    }



def get_all_employees_service():

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM employees
        WHERE status='Active'
        ORDER BY employee_id
    """)

    employees = cursor.fetchall()

    cursor.close()

    return employees



def get_employee_service(employee_id: str):

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM employees
        WHERE employee_id=%s
    """,
    (employee_id,)
    )

    employee = cursor.fetchone()

    cursor.close()

    if employee is None:
        return {
            "message": "Employee Not Found"
        }

    return employee


def update_employee_service(employee_id: str, employee: Employee):

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM employees
        WHERE employee_id=%s
    """,
    (employee_id,)
    )

    existing_employee = cursor.fetchone()

    if existing_employee is None:

        cursor.close()

        return {
            "message": "Employee Not Found"
        }

    cursor.execute("""
        UPDATE employees

        SET

        first_name=%s,
        last_name=%s,
        email=%s,
        phone=%s,
        department_id=%s,
        designation=%s,
        education=%s,
        skills=%s,
        base_salary=%s

        WHERE employee_id=%s
    """,
    (
        employee.first_name,
        employee.last_name,
        employee.email,
        employee.phone,
        employee.department_id,
        employee.designation,
        employee.education,
        employee.skills,
        employee.base_salary,
        employee_id
    ))

    connection.commit()

    cursor.close()

    return {
        "message": "Employee Updated Successfully"
    }


def delete_employee_service(employee_id: str):

    cursor = connection.cursor(dictionary=True)

    # Check employee exists
    cursor.execute("""
        SELECT employee_id, status
        FROM employees
        WHERE employee_id = %s
    """, (employee_id,))

    employee = cursor.fetchone()

    if not employee:
        cursor.close()
        return {
            "message": "Employee not found"
        }

    if employee["status"] == "Resigned":
        cursor.close()
        return {
            "message": "Employee is already resigned"
        }


    cursor.execute("""
        UPDATE employees
        SET status = 'Resigned'
        WHERE employee_id = %s
    """, (employee_id,))

    
    cursor.execute("""
        UPDATE users
        SET status = 'Inactive'
        WHERE employee_id = %s
        AND role = 'Employee'
    """, (employee_id,))

    connection.commit()
    cursor.close()

    return {
        "message": "Employee deleted successfully",
        "employee_id": employee_id,
        "status": "Resigned",
        "login_status": "Inactive"
    }

def get_my_employee_service(employee_id: str):

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
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
        FROM employees
        WHERE employee_id = %s
    """, (employee_id,))

    employee = cursor.fetchone()

    cursor.close()

    if employee is None:
        return {
            "message": "Employee profile not found"
        }

    return employee


def search_employees_service(search: str):

    cursor = connection.cursor(dictionary=True)

    search_value = f"%{search}%"

    cursor.execute("""
        SELECT
            employee_id,
            first_name,
            last_name,
            email,
            phone,
            department_id,
            designation,
            status
        FROM employees
        WHERE employee_id LIKE %s
           OR first_name LIKE %s
           OR last_name LIKE %s
           OR email LIKE %s
        ORDER BY first_name ASC, last_name ASC
    """, (
        search_value,
        search_value,
        search_value,
        search_value
    ))

    employees = cursor.fetchall()

    cursor.close()

    return employees