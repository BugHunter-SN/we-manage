from fastapi import APIRouter, Request, Depends, UploadFile, File, HTTPException, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import Employee, EmployeeCreate, EmployeeUpdate
from fastapi.templating import Jinja2Templates
import os
from pathlib import Path
import math

router = APIRouter()
templates = Jinja2Templates(directory="./user_demo_project/employee_repo/templates")

# Directory to store uploaded images
UPLOAD_DIR = "./employee_repo/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ------------------- ROUTES -------------------

# Fix the path - use absolute path to be safe
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "employee_repo" / "templates"))

@router.get("/", response_class=HTMLResponse)
def read_employees(
    request: Request, 
    page: int = Query(1, ge=1, description="Page number"), 
    per_page: int = Query(5, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    # Calculate offset
    offset = (page - 1) * per_page
    
    # Get total count of active employees
    total_employees = db.query(func.count(Employee.id)).filter(Employee.is_active == True).scalar()
    
    # Get employees for current page
    employees = (
        db.query(Employee)
        .filter(Employee.is_active == True)
        .offset(offset)
        .limit(per_page)
        .all()
    )
    
    # Calculate pagination info
    total_pages = math.ceil(total_employees / per_page) if total_employees > 0 else 1
    has_prev = page > 1
    has_next = page < total_pages
    
    # Calculate page range for pagination display
    start_page = max(1, page - 2)
    end_page = min(total_pages, page + 2)
    
    pagination_info = {
        'current_page': page,
        'per_page': per_page,
        'total_employees': total_employees,
        'total_pages': total_pages,
        'has_prev': has_prev,
        'has_next': has_next,
        'prev_page': page - 1 if has_prev else None,
        'next_page': page + 1 if has_next else None,
        'start_page': start_page,
        'end_page': end_page,
        'page_range': range(start_page, end_page + 1)
    }
    
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "employees": employees,
            "pagination": pagination_info
        }
    )


@router.get("/details/{employee_id}", response_class=HTMLResponse)
def employee_details(request: Request, employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id, Employee.is_active == True).first()
    if not employee:
        return templates.TemplateResponse("not_found.html", {"request": request, "employee": None})
    return templates.TemplateResponse("details.html", {"request": request, "employee": employee})


@router.get("/add", response_class=HTMLResponse)
def add_employee_form(request: Request):
    return templates.TemplateResponse("add_employee.html", {"request": request})


@router.post("/add")
async def add_employee(
    request: Request,
    employee: EmployeeCreate = Depends(EmployeeCreate.as_form),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    image_url = None
    if image and image.filename:
        image_path = os.path.join(UPLOAD_DIR, image.filename)
        with open(image_path, "wb") as f:
            f.write(await image.read())
        image_url = f"/static/uploads/{image.filename}"

    new_employee = Employee(
        first_name=employee.first_name,
        last_name=employee.last_name,
        email=employee.email,
        salary=employee.salary,
        image_url=image_url
    )
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return RedirectResponse("/", status_code=303)


@router.get("/edit/{employee_id}", response_class=HTMLResponse)
def edit_employee_form(request: Request, employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
         return templates.TemplateResponse("not_found.html", {"request": request, "employee": employee})
    return templates.TemplateResponse("edit_employee.html", {"request": request, "employee": employee})


@router.post("/edit/{employee_id}")
async def edit_employee(
    request: Request,
    employee_id: int,
    employee: EmployeeUpdate = Depends(EmployeeUpdate.as_form),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    if employee.first_name is not None:
        db_employee.first_name = employee.first_name
    if employee.last_name is not None:
        db_employee.last_name = employee.last_name
    if employee.email is not None:
        db_employee.email = employee.email
    if employee.salary is not None:
        db_employee.salary = employee.salary

    if image and image.filename:
        image_path = os.path.join(UPLOAD_DIR, image.filename)
        with open(image_path, "wb") as f:
            f.write(await image.read())
        db_employee.image_url = f"/static/uploads/{image.filename}"

    db.commit()
    db.refresh(db_employee)
    return RedirectResponse("/", status_code=303)


@router.post("/deactivate/{employee_id}")
def deactivate_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db_employee.is_active = False
    db.commit()
    return RedirectResponse("/", status_code=303)