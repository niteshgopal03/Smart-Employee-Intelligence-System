from pydantic import BaseModel


class SalaryPredictionRequest(BaseModel):
    education: str
    experience_years: int
    department: str
    designation: str
    skills_count: int
    manager_rating: float
    attendance_percentage: float


class PromotionPredictionRequest(BaseModel):
    education: str
    experience_years: int
    department: str
    designation: str
    skills_count: int
    manager_rating: float
    attendance_percentage: float
    leave_balance: int


class AttritionPredictionRequest(BaseModel):
    education: str
    experience_years: int
    department: str
    designation: str
    base_salary: float
    manager_rating: float
    attendance_percentage: float
    leave_balance: int
    absence_count: int
    leave_request_count: int

class EmployeeAIPredictionRequest(BaseModel):
    employee_id: str    