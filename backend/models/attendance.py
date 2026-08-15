from pydantic import BaseModel
from datetime import date, time
from typing import Optional


class Attendance(BaseModel):
    employee_id: str
    attendance_date: date
    check_in: Optional[time] = None
    check_out: Optional[time] = None
    status: str