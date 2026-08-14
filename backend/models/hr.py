from pydantic import BaseModel
from datetime import date


class HR(BaseModel):

    first_name: str
    last_name: str

    email: str

    phone: str

    gender: str

    dob: date

    joining_date: date

    department_id: int

    designation: str

    education: str

    skills: str

    base_salary: float