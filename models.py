from pydantic import BaseModel, validator
from decimal import Decimal
from typing import Optional
from fastapi import Form
import inspect

class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    salary: float
           
    @validator('salary', pre=True)
    def convert_salary(cls, v):
        if isinstance(v, Decimal):
            return float(v)
        return v
    
    @classmethod
    def as_form(
        cls,
        first_name: str = Form(...),
        last_name: str = Form(...),
        email: str = Form(...),
        salary: float = Form(...),
    ):
        return cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
            salary=salary
        )

class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    salary: Optional[float] = None
           
    @validator('salary', pre=True)
    def convert_salary(cls, v):
        if v is not None and isinstance(v, Decimal):
            return float(v)
        return v
    
    @classmethod
    def as_form(
        cls,
        first_name: Optional[str] = Form(None),
        last_name: Optional[str] = Form(None),
        email: Optional[str] = Form(None),
        salary: Optional[float] = Form(None),
    ):
        return cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
            salary=salary
        )