from pydantic import BaseModel, Field


class PerformanceUpdate(BaseModel):
    manager_rating: float = Field(..., ge=1, le=5)
