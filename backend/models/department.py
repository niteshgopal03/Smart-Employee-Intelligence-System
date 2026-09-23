from pydantic import BaseModel


class DepartmentCreate(BaseModel):
    department_name: str
    description: str | None = None


class DepartmentUpdate(BaseModel):
    department_name: str
    description: str | None = None