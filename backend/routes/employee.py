from fastapi import APIRouter, HTTPException
from models import Employee
from database import connection

router = APIRouter()


@router.post("/employee/add")
def add_employee(employee: Employee):

    cursor = connection.cursor()

    try:
        # Check if email already exists
        cursor.execute(
            "SELECT email FROM employees WHERE email = %s",
            (employee.email,)
        )

        if cursor.fetchone():
            raise HTTPException(
                status_code=400,
                detail="Email already exists."
            )

        # Generate Employee ID (Learning Version)
        cursor.execute("SELECT COUNT(*) FROM employees")
        count = cursor.fetchone()[0]
        employee_id = f"EMP{1001 + count}"

        # Insert employee
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

        # Create login
        cursor.execute(
            """
            INSERT INTO users
            (
                username,
                password_hash,
                role,
                employee_id
            )

            VALUES
            (%s,%s,%s,%s)
            """,
            (
                employee_id,
                "TEMP_HASH",
                "Employee",
                employee_id
            )
        )

        connection.commit()

        return {
            "message": "Employee added successfully",
            "employee_id": employee_id
        }

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()

#VIEW EMPLOYEE
@router.get("/employees")
def get_all_employees():

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM employees
    """)

    employees = cursor.fetchall()

    cursor.close()

    return employees
#SEARCH EMPLOYEES

@router.get("/employee/{employee_id}")
def get_employee(employee_id: str):

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

#UPDATE EMPLYEE
@router.put("/employee/update/{employee_id}")
def update_employee(employee_id: str, employee: Employee):

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
 #DELETE EMPLOYEE 

@router.delete("/employee/delete/{employee_id}")
def delete_employee(employee_id: str):

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