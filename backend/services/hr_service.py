from database import connection
from security.password import hash_password


def generate_hr_id(department_id: int):

    cursor = connection.cursor()

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

    
    cursor.execute("""
        DELETE FROM users
        WHERE employee_id = %s
        AND role = 'HR'
    """, (employee_id,))


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