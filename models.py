# from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Boolean, JSON, Float
# from sqlalchemy.orm import relationship
# from datetime import datetime
# from pydantic import BaseModel, EmailStr
# from typing import Optional, Dict
# from database import Base  

# ----------------------
# SQLAlchemy Models
# ----------------------

# class Company(Base):
#     __tablename__ = "companies"

#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     registration_number = Column(String, nullable=True)
#     timezone = Column(String, default="Africa/Monrovia")
#     currency = Column(String, default="LRD")
#     country = Column(String, default="Liberia")

#     employees = relationship("Employee", back_populates="company")
#     compliance_records = relationship("ComplianceRecord", back_populates="company")
#     payroll_periods = relationship("PayrollPeriod", back_populates="company")


# class Employee(Base):
#     __tablename__ = "employees"

#     id = Column(Integer, primary_key=True)
#     company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
#     first_name = Column(String, nullable=False)
#     last_name = Column(String, nullable=False)
#     email = Column(String, nullable=True)
#     salary = Column(Float, default=0.0)
#     image_url = Column(String, nullable=True)
#     is_active = Column(Boolean, default=True)
#     national_id = Column(String, nullable=True)
#     dob = Column(Date, nullable=True)
#     phone = Column(String, nullable=True)
#     hire_date = Column(Date, nullable=True)
#     job_title = Column(String, nullable=True)
#     bank_account = Column(String, nullable=True)
#     momo_number = Column(String, nullable=True)

#     company = relationship("Company", back_populates="employees")
#     attendances = relationship("Attendance", back_populates="employee")
#     leave_requests = relationship("LeaveRequest", back_populates="employee")
#     payslips = relationship("Payslip", back_populates="employee")
#     payroll_transactions = relationship("PayrollTransaction", back_populates="employee")


# class Attendance(Base):
#     __tablename__ = "attendances"

#     id = Column(Integer, primary_key=True)
#     employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
#     date = Column(Date, nullable=False)
#     clock_in = Column(DateTime, default=None)
#     clock_out = Column(DateTime, default=None)
#     source = Column(String, default="manual")
#     gps = Column(String, nullable=True)
#     status = Column(String, default="present")
#     synced = Column(Boolean, default=False)

#     employee = relationship("Employee", back_populates="attendances")


# class LeaveRequest(Base):
#     __tablename__ = "leave_requests"

#     id = Column(Integer, primary_key=True)
#     employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
#     leave_type = Column(String, nullable=False)
#     start_date = Column(Date, nullable=False)
#     end_date = Column(Date, nullable=False)
#     status = Column(String, default="pending")
#     approver_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
#     created_at = Column(DateTime, default=datetime.utcnow)

#     employee = relationship("Employee", back_populates="leave_requests")


# class PayrollPeriod(Base):
#     __tablename__ = "payroll_periods"

#     id = Column(Integer, primary_key=True)
#     company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
#     start_date = Column(Date, nullable=False)
#     end_date = Column(Date, nullable=False)
#     processed_at = Column(DateTime, default=None)
#     status = Column(String, default="pending")
#     total_gross = Column(Float, default=0.0)
#     total_net = Column(Float, default=0.0)

#     company = relationship("Company", back_populates="payroll_periods")
#     payslips = relationship("Payslip", back_populates="payroll_period")
#     payroll_transactions = relationship("PayrollTransaction", back_populates="payroll_period")


# class Payslip(Base):
#     __tablename__ = "payslips"

#     id = Column(Integer, primary_key=True)
#     payroll_period_id = Column(Integer, ForeignKey("payroll_periods.id"), nullable=False)
#     employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
#     gross_pay = Column(Float, nullable=False, default=0.0)
#     deductions_json = Column(JSON, default={})
#     net_pay = Column(Float, nullable=False, default=0.0)
#     pdf_path = Column(String, nullable=True)

#     payroll_period = relationship("PayrollPeriod", back_populates="payslips")
#     employee = relationship("Employee", back_populates="payslips")


# class PayrollTransaction(Base):
#     __tablename__ = "payroll_transactions"

#     id = Column(Integer, primary_key=True)
#     payroll_period_id = Column(Integer, ForeignKey("payroll_periods.id"), nullable=False)
#     employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
#     amount = Column(Float, nullable=False)
#     method = Column(String, default="momo")
#     status = Column(String, default="pending")
#     external_ref = Column(String, nullable=True)

#     payroll_period = relationship("PayrollPeriod", back_populates="payroll_transactions")
#     employee = relationship("Employee", back_populates="payroll_transactions")


# class ComplianceRecord(Base):
#     __tablename__ = "compliance_records"

#     id = Column(Integer, primary_key=True)
#     company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
#     period = Column(String, nullable=False)
#     type = Column(String, nullable=False)
#     payload_json = Column(JSON, default={})
#     generated_at = Column(DateTime, default=datetime.utcnow)
#     submitted_at = Column(DateTime, default=None)

#     company = relationship("Company", back_populates="compliance_records")


# # ----------------------
# # Pydantic Schemas with as_form
# # ----------------------

# class EmployeeBase(BaseModel):
#     first_name: str
#     last_name: str
#     email: Optional[EmailStr] = None
#     salary: Optional[float] = 0.0
#     image_url: Optional[str] = None

# class EmployeeCreate(EmployeeBase):
#     @classmethod
#     def as_form(cls,
#                 first_name: str = None,
#                 last_name: str = None,
#                 email: str = None,
#                 salary: float = 0.0,
#                 image_url: Optional[str] = None):
#         return cls(first_name=first_name, last_name=last_name, email=email, salary=salary, image_url=image_url)

# class EmployeeUpdate(BaseModel):
#     first_name: Optional[str] = None
#     last_name: Optional[str] = None
#     email: Optional[EmailStr] = None
#     salary: Optional[float] = None
#     image_url: Optional[str] = None


# class AttendanceBase(BaseModel):
#     date: datetime
#     clock_in: Optional[datetime] = None
#     clock_out: Optional[datetime] = None
#     source: Optional[str] = "manual"

# class AttendanceCreate(AttendanceBase):
#     employee_id: int
#     @classmethod
#     def as_form(cls,
#                 employee_id: int,
#                 date: datetime,
#                 clock_in: Optional[datetime] = None,
#                 clock_out: Optional[datetime] = None,
#                 source: Optional[str] = "manual"):
#         return cls(employee_id=employee_id, date=date, clock_in=clock_in, clock_out=clock_out, source=source)


# class LeaveRequestBase(BaseModel):
#     leave_type: str
#     start_date: datetime
#     end_date: datetime

# class LeaveRequestCreate(LeaveRequestBase):
#     employee_id: int
#     @classmethod
#     def as_form(cls,
#                 employee_id: int,
#                 leave_type: str,
#                 start_date: datetime,
#                 end_date: datetime):
#         return cls(employee_id=employee_id, leave_type=leave_type, start_date=start_date, end_date=end_date)


# class PayrollPeriodBase(BaseModel):
#     start_date: datetime
#     end_date: datetime

# class PayrollPeriodCreate(PayrollPeriodBase):
#     company_id: int
#     @classmethod
#     def as_form(cls,
#                 company_id: int,
#                 start_date: datetime,
#                 end_date: datetime):
#         return cls(company_id=company_id, start_date=start_date, end_date=end_date)


# class PayslipBase(BaseModel):
#     gross_pay: float
#     net_pay: float
#     deductions_json: Optional[Dict] = {}

# class PayslipCreate(PayslipBase):
#     payroll_period_id: int
#     employee_id: int
#     @classmethod
#     def as_form(cls,
#                 payroll_period_id: int,
#                 employee_id: int,
#                 gross_pay: float,
#                 net_pay: float,
#                 deductions_json: Optional[Dict] = {}):
#         return cls(payroll_period_id=payroll_period_id, employee_id=employee_id, gross_pay=gross_pay, net_pay=net_pay, deductions_json=deductions_json)


# class PayrollTransactionBase(BaseModel):
#     amount: float
#     method: Optional[str] = "momo"

# class PayrollTransactionCreate(PayrollTransactionBase):
#     payroll_period_id: int
#     employee_id: int
#     @classmethod
#     def as_form(cls,
#                 payroll_period_id: int,
#                 employee_id: int,
#                 amount: float,
#                 method: Optional[str] = "momo"):
#         return cls(payroll_period_id=payroll_period_id, employee_id=employee_id, amount=amount, method=method)


# class ComplianceRecordBase(BaseModel):
#     period: str
#     type: str
#     payload_json: Optional[Dict] = {}

# class ComplianceRecordCreate(ComplianceRecordBase):
#     company_id: int
#     @classmethod
#     def as_form(cls,
#                 company_id: int,
#                 period: str,
#                 type: str,
#                 payload_json: Optional[Dict] = {}):
#         return cls(company_id=company_id, period=period, type=type, payload_json=payload_json)





from sqlalchemy import Column, Integer, String, Float, Boolean
from fastapi import Form
from typing import Optional
from database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    salary = Column(Float, nullable=True)
    image_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

# Helper classes for form validation in FastAPI
class EmployeeCreate:
    def __init__(
        self,
        first_name: str = Form(...),
        last_name: str = Form(...),
        email: str = Form(...),
        salary: float = Form(...),
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.salary = salary

    @classmethod
    def as_form(
        cls,
        first_name: str = Form(...),
        last_name: str = Form(...),
        email: str = Form(...),
        salary: float = Form(...),
    ):
        return cls(first_name, last_name, email, salary)
# help(Employee)
class EmployeeUpdate:
    def __init__(
        self,
        first_name: Optional[str] = Form(None),
        last_name: Optional[str] = Form(None),
        email: Optional[str] = Form(None),
        salary: Optional[float] = Form(None),
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.salary = salary

    @classmethod
    def as_form(
        cls,
        first_name: Optional[str] = Form(None),
        last_name: Optional[str] = Form(None),
        email: Optional[str] = Form(None),
        salary: Optional[float] = Form(None),
    ):
        return cls(first_name, last_name, email, salary)
