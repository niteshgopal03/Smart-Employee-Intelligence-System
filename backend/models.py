from pydantic import BaseModel, EmailStr
from datetime import date

class Employee(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    gender: str
    dob: date
    joining_date: date
    department_id: int
    designation: str
    education: str
    skills: str
    base_salary: float
    manager_rating: float
    attendance_percentage: float
    leave_balance: int