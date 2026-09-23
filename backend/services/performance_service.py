from fastapi import HTTPException

from database import connection


def update_manager_rating(
    employee_id: str,
    manager_rating: float
):

    cursor = connection.cursor(dictionary=True)

    # Check employee
    cursor.execute(
        """
        SELECT employee_id, first_name, last_name
        FROM employees
        WHERE employee_id=%s
        AND status='Active'
        """,
        (employee_id,)
    )

    employee = cursor.fetchone()

    if employee is None:

        cursor.close()

        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    # Update rating
    cursor.execute(
        """
        UPDATE employees
        SET manager_rating=%s
        WHERE employee_id=%s
        """,
        (manager_rating, employee_id)
    )

    connection.commit()

    cursor.close()

    return {
        "message": "Manager rating updated successfully",
        "employee_id": employee_id,
        "employee_name": (
            employee["first_name"]
            + " "
            + employee["last_name"]
        ),
        "manager_rating": manager_rating
    }


def get_manager_rating(employee_id: str):

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            employee_id,
            first_name,
            last_name,
            manager_rating
        FROM employees
        WHERE employee_id=%s
        """,
        (employee_id,)
    )

    employee = cursor.fetchone()

    cursor.close()

    if employee is None:

        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return {
        "employee_id": employee["employee_id"],
        "employee_name": (
            employee["first_name"]
            + " "
            + employee["last_name"]
        ),
        "manager_rating": employee["manager_rating"]
    }

def get_performance_dashboard_service():

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            p.performance_id,
            p.employee_id,
            e.first_name,
            e.last_name,
            p.review_period,
            p.productivity_score,
            p.quality_score,
            p.teamwork_score,
            p.innovation_score,
            p.manager_rating,
            p.overall_score
        FROM performance p
        JOIN employees e
            ON p.employee_id = e.employee_id
        ORDER BY p.overall_score DESC
    """)

    records = cursor.fetchall()

    cursor.close()

    total_records = len(records)

    if total_records == 0:
        return {
            "summary": {
                "total_records": 0,
                "average_overall_score": 0
            },
            "employees": []
        }

    total_score = 0

    employees = []

    for record in records:

        if record["overall_score"] is not None:
            total_score += float(record["overall_score"])

        employees.append({
            "performance_id": record["performance_id"],
            "employee_id": record["employee_id"],
            "first_name": record["first_name"],
            "last_name": record["last_name"],
            "review_period": record["review_period"],
            "productivity_score": record["productivity_score"],
            "quality_score": record["quality_score"],
            "teamwork_score": record["teamwork_score"],
            "innovation_score": record["innovation_score"],
            "manager_rating": record["manager_rating"],
            "overall_score": record["overall_score"]
        })

    average_score = round(
        total_score / total_records,
        2
    )

    return {
        "summary": {
            "total_records": total_records,
            "average_overall_score": average_score
        },
        "employees": employees
    }