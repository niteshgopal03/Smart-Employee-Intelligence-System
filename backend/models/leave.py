from pydantic import BaseModel
from datetime import date


class LeaveRequest(BaseModel):

    from_date: date
    to_date: date
    reason: str