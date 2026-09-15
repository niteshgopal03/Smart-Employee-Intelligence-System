from pathlib import Path
from fastapi import HTTPException
from datetime import date
from database import connection
import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_DIR = BASE_DIR / "ml_models"

salary_model = joblib.load(
    MODEL_DIR / "salary_model.pkl"
)

promotion_model = joblib.load(
    MODEL_DIR / "promotion_model.pkl"
)

attrition_model = joblib.load(
    MODEL_DIR / "attrition_model.pkl"
)

def calculate_experience(joining_date):

    today = date.today()

    experience = (
        today.year - joining_date.year
        - (
            (today.month, today.day)
            < (joining_date.month, joining_date.day)
        )
    )

    return max(experience, 0)


def calculate_skills_count(skills):

    if not skills:
        return 0

    return len([
        skill.strip()
        for skill in skills.split(",")
        if skill.strip()
    ])


def get_employee_for_ai(employee_id):

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            e.employee_id,
            e.education,
            e.joining_date,
            e.department_id,
            e.designation,
            e.skills,
            e.base_salary,
            e.manager_rating,
            e.attendance_percentage,
            e.leave_balance,
            d.department_name
        FROM employees e
        JOIN departments d
            ON e.department_id = d.department_id
        WHERE e.employee_id = %s
        AND e.status = 'Active'
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

    return employee

def get_attendance_features(employee_id):

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            COUNT(*) AS total_days,
            SUM(
                CASE
                    WHEN status='Present' THEN 1
                    ELSE 0
                END
            ) AS present_days,
            SUM(
                CASE
                    WHEN status='Absent' THEN 1
                    ELSE 0
                END
            ) AS absent_days,
            SUM(
                CASE
                    WHEN status='Leave' THEN 1
                    ELSE 0
                END
            ) AS leave_days
        FROM attendance
        WHERE employee_id=%s
        """,
        (employee_id,)
    )

    result = cursor.fetchone()
    cursor.close()

    if result is None or result["total_days"] == 0:
        raise HTTPException(
            status_code=400,
            detail="No attendance records found for employee"
        )

    total_days = result["total_days"]
    present_days = result["present_days"] or 0
    absent_days = result["absent_days"] or 0
    leave_days = result["leave_days"] or 0

    attendance_percentage = (
        present_days / total_days
    ) * 100

    return {
        "total_days": total_days,
        "present_days": present_days,
        "absent_days": absent_days,
        "leave_days": leave_days,
        "attendance_percentage": round(
            attendance_percentage,
            2
        ),
        "absence_count": absent_days
    }

def get_leave_features(employee_id):

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            COUNT(*) AS leave_request_count
        FROM leave_requests
        WHERE employee_id=%s
        """,
        (employee_id,)
    )

    result = cursor.fetchone()
    cursor.close()

    return {
        "leave_request_count": (
            result["leave_request_count"] or 0
        )
    }

def predict_salary_for_employee(employee_id):

    employee = get_employee_for_ai(employee_id)

    experience_years = calculate_experience(
        employee["joining_date"]
    )

    skills_count = calculate_skills_count(
        employee["skills"]
    )

    required_fields = [
        "education",
        "department_name",
        "designation",
        "manager_rating"
    ]

    missing_fields = [
        field
        for field in required_fields
        if employee[field] is None
    ]

    if missing_fields:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Employee data is incomplete for AI prediction",
                "missing_fields": missing_fields
            }
        )

    attendance = get_attendance_features(employee_id)

    input_data = pd.DataFrame([{
        "education": employee["education"],
        "experience_years": experience_years,
        "department": employee["department_name"],
        "designation": employee["designation"],
        "skills_count": skills_count,
        "manager_rating": float(
            employee["manager_rating"]
        ),
        "attendance_percentage": attendance[
            "attendance_percentage"
        ]
    }])

    prediction = salary_model.predict(
        input_data
    )[0]

    return {
        "employee_id": employee_id,
        "predicted_salary": round(
            float(prediction),
            2
        )
    }


def predict_promotion_for_employee(employee_id):

    employee = get_employee_for_ai(employee_id)

    required_fields = [
        "education",
        "joining_date",
        "department_name",
        "designation",
        "manager_rating"
    ]

    missing_fields = [
        field
        for field in required_fields
        if employee[field] is None
    ]

    if missing_fields:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Employee data is incomplete for promotion prediction",
                "missing_fields": missing_fields
            }
        )

    attendance = get_attendance_features(employee_id)

    experience_years = calculate_experience(
        employee["joining_date"]
    )

    skills_count = calculate_skills_count(
        employee["skills"]
    )

    leave_balance = (
        int(employee["leave_balance"])
        if employee["leave_balance"] is not None
        else 0
    )

    input_data = pd.DataFrame([{
        "education": employee["education"],
        "experience_years": experience_years,
        "department": employee["department_name"],
        "designation": employee["designation"],
        "skills_count": skills_count,
        "manager_rating": float(
            employee["manager_rating"]
        ),
        "attendance_percentage": attendance[
            "attendance_percentage"
        ],
        "leave_balance": leave_balance
    }])

    prediction = int(
        promotion_model.predict(input_data)[0]
    )

    probability = float(
        promotion_model.predict_proba(input_data)[0][1]
    )

    if prediction == 1:
        status = "Likely"
        confidence = probability * 100
    else:
        status = "Unlikely"
        confidence = (1 - probability) * 100

    reasons = []

    if experience_years >= 5:
        reasons.append(
            f"{experience_years} years of experience supports promotion readiness."
        )
    elif experience_years < 3:
        reasons.append(
            f"{experience_years} years of experience may be limited for promotion."
        )

    if employee["manager_rating"] >= 4:
        reasons.append(
            f"Manager rating of {employee['manager_rating']}/5 indicates strong performance."
        )
    elif employee["manager_rating"] < 3:
        reasons.append(
            f"Manager rating of {employee['manager_rating']}/5 may reduce promotion readiness."
        )

    if attendance["attendance_percentage"] >= 90:
        reasons.append(
            f"Attendance of {attendance['attendance_percentage']}% shows good attendance."
        )
    elif attendance["attendance_percentage"] < 80:
        reasons.append(
            f"Attendance of {attendance['attendance_percentage']}% is relatively low."
        )

    if skills_count >= 6:
        reasons.append(
            f"{skills_count} recorded skills indicate a strong skill profile."
        )
    elif skills_count <= 2:
        reasons.append(
            f"Only {skills_count} recorded skills; skill development may help."
        )

    if employee["education"] in ["Master", "PhD"]:
        reasons.append(
            f"{employee['education']} qualification supports career progression."
        )

    if employee["leave_balance"] is not None and leave_balance < 5:
        reasons.append(
            f"Low leave balance of {leave_balance} days."
        )

    if not reasons:
        reasons.append(
            "Current employee indicators do not show major promotion factors."
        )

    return {
        "employee_id": employee_id,
        "promotion_prediction": status,
        "confidence": round(confidence, 2),
        "reasons": reasons,
        "employee_features": {
            "experience_years": experience_years,
            "skills_count": skills_count,
            "manager_rating": float(
                employee["manager_rating"]
            ),
            "attendance_percentage": attendance[
                "attendance_percentage"
            ],
            "leave_balance": leave_balance
        }
    }

def predict_attrition_for_employee(employee_id):

    employee = get_employee_for_ai(employee_id)

    required_fields = [
        "education",
        "joining_date",
        "department_name",
        "designation",
        "base_salary",
        "manager_rating"
    ]

    missing_fields = [
        field
        for field in required_fields
        if employee[field] is None
    ]

    if missing_fields:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Employee data is incomplete for attrition prediction",
                "missing_fields": missing_fields
            }
        )

    attendance = get_attendance_features(
        employee_id
    )

    leave = get_leave_features(
        employee_id
    )

    experience_years = calculate_experience(
        employee["joining_date"]
    )

    leave_balance = (
        int(employee["leave_balance"])
        if employee["leave_balance"] is not None
        else 0
    )

    input_data = pd.DataFrame([{
        "education": employee["education"],
        "experience_years": experience_years,
        "department": employee["department_name"],
        "designation": employee["designation"],
        "base_salary": float(
            employee["base_salary"]
        ),
        "manager_rating": float(
            employee["manager_rating"]
        ),
        "attendance_percentage": attendance[
            "attendance_percentage"
        ],
        "leave_balance": leave_balance,
        "absence_count": attendance[
            "absence_count"
        ],
        "leave_request_count": leave[
            "leave_request_count"
        ]
    }])

    probability = float(
        attrition_model.predict_proba(
            input_data
        )[0][1]
    )

    if probability >= 0.70:
        risk = "High Risk"
    elif probability >= 0.40:
        risk = "Medium Risk"
    else:
        risk = "Low Risk"

    reasons = []

    if employee["manager_rating"] < 3:
        reasons.append(
            f"Manager rating of {employee['manager_rating']}/5 is relatively low."
        )

    if attendance["attendance_percentage"] < 85:
        reasons.append(
            f"Attendance of {attendance['attendance_percentage']}% is relatively low."
        )

    if attendance["absence_count"] >= 10:
        reasons.append(
            f"{attendance['absence_count']} absences indicate increased absence activity."
        )

    if leave["leave_request_count"] >= 8:
        reasons.append(
            f"{leave['leave_request_count']} leave requests indicate higher leave activity."
        )

    if experience_years < 2:
        reasons.append(
            "Short tenure may increase early-stage attrition risk."
        )

    if not reasons:
        reasons.append(
            "Current employee indicators do not show major attrition risk factors."
        )

    confidence = max(
        probability,
        1 - probability
    ) * 100

    return {
        "employee_id": employee_id,
        "attrition_risk": risk,
        "high_risk_probability": round(
            probability * 100,
            2
        ),
        "confidence": round(
            confidence,
            2
        ),
        "reasons": reasons,
        "employee_features": {
            "experience_years": experience_years,
            "manager_rating": float(
                employee["manager_rating"]
            ),
            "attendance_percentage": attendance[
                "attendance_percentage"
            ],
            "absence_count": attendance[
                "absence_count"
            ],
            "leave_balance": leave_balance,
            "leave_request_count": leave[
                "leave_request_count"
            ],
            "base_salary": float(
                employee["base_salary"]
            )
        }
    }